# api/volunteer_api.py
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from __init__ import db
from model.volunteer import VolunteerShift, VolunteerAssignment, VolunteerJob
from datetime import datetime

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/api')
volunteer_api = Api(volunteer_bp)

class ShiftListAPI(Resource):
    def get(self):
        """Get all volunteer shifts"""
        date_filter = request.args.get('date')
        train_type = request.args.get('train_type')
        
        query = VolunteerShift.query
        if date_filter:
            query = query.filter_by(date=date_filter)
        if train_type:
            query = query.filter_by(train_type=train_type)
        
        shifts = query.order_by(VolunteerShift.date, VolunteerShift.time_start).all()
        return jsonify([s.to_dict() for s in shifts])

    def post(self):
        """Create a new volunteer shift (admin only)"""
        data = request.get_json()
        
        required = ['date', 'time_start', 'time_end', 'train_type']
        for field in required:
            if field not in data:
                return {'error': f'Missing field: {field}'}, 400
        
        shift = VolunteerShift(
            date=data['date'],
            time_start=data['time_start'],
            time_end=data['time_end'],
            train_type=data['train_type'],
            max_volunteers=data.get('max_volunteers', 4)
        )
        
        db.session.add(shift)
        db.session.commit()
        
        return shift.to_dict(), 201

class ShiftDetailAPI(Resource):
    def get(self, shift_id):
        shift = VolunteerShift.query.get(shift_id)
        if not shift:
            return {'error': 'Shift not found'}, 404
        return shift.to_dict()
    
    def delete(self, shift_id):
        shift = VolunteerShift.query.get(shift_id)
        if not shift:
            return {'error': 'Shift not found'}, 404
        db.session.delete(shift)
        db.session.commit()
        return {'message': 'Shift deleted'}, 200

class AssignmentAPI(Resource):
    def post(self, shift_id):
        """Sign up for a volunteer shift"""
        shift = VolunteerShift.query.get(shift_id)
        if not shift:
            return {'error': 'Shift not found'}, 404
        
        data = request.get_json()
        required = ['name', 'email', 'job']
        for field in required:
            if field not in data:
                return {'error': f'Missing field: {field}'}, 400
        
        # Check if shift is full
        if len(shift.assignments) >= shift.max_volunteers:
            return {'error': 'Shift is full'}, 409
        
        # Check if already signed up
        existing = VolunteerAssignment.query.filter_by(
            shift_id=shift_id,
            email=data['email']
        ).first()
        if existing:
            return {'error': 'Already signed up for this shift'}, 409
        
        assignment = VolunteerAssignment(
            shift_id=shift_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            job=data['job']
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return assignment.to_dict(), 201
    
    def delete(self, shift_id):
        """Cancel volunteer sign-up"""
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return {'error': 'Email required'}, 400
        
        assignment = VolunteerAssignment.query.filter_by(
            shift_id=shift_id,
            email=email
        ).first()
        
        if not assignment:
            return {'error': 'Sign-up not found'}, 404
        
        db.session.delete(assignment)
        db.session.commit()
        
        return {'message': 'Cancelled successfully'}, 200

class JobListAPI(Resource):
    def get(self):
        jobs = VolunteerJob.query.all()
        return jsonify([j.to_dict() for j in jobs])
    
    def post(self):
        data = request.get_json()
        job = VolunteerJob(
            job_name=data['job_name'],
            description=data.get('description', '')
        )
        db.session.add(job)
        db.session.commit()
        return job.to_dict(), 201

# Register resources
volunteer_api.add_resource(ShiftListAPI, '/volunteer/shifts')
volunteer_api.add_resource(ShiftDetailAPI, '/volunteer/shifts/<int:shift_id>')
volunteer_api.add_resource(AssignmentAPI, '/volunteer/shifts/<int:shift_id>/signup')
volunteer_api.add_resource(JobListAPI, '/volunteer/jobs')
