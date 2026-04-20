# model/volunteer.py
from __init__ import db
from datetime import datetime
import random
import string

class VolunteerShift(db.Model):
    __tablename__ = 'volunteer_shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    time_start = db.Column(db.String(5), nullable=False)  # HH:MM
    time_end = db.Column(db.String(5), nullable=False)
    train_type = db.Column(db.String(50), nullable=False)  # steam, cable, speeder
    max_volunteers = db.Column(db.Integer, default=4)
    
    # Relationships
    assignments = db.relationship('VolunteerAssignment', backref='shift', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'time_start': self.time_start,
            'time_end': self.time_end,
            'train_type': self.train_type,
            'max_volunteers': self.max_volunteers,
            'current_volunteers': len(self.assignments),
            'slots_available': self.max_volunteers - len(self.assignments),
            'volunteers': [a.to_dict() for a in self.assignments]
        }

class VolunteerAssignment(db.Model):
    __tablename__ = 'volunteer_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('volunteer_shifts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    job = db.Column(db.String(50), nullable=False)  # Conductor, Ticket Taker, Safety, Engineer
    signed_up_at = db.Column(db.String(50), default=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'job': self.job,
            'signed_up_at': self.signed_up_at
        }

class VolunteerJob(db.Model):
    __tablename__ = 'volunteer_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_name': self.job_name,
            'description': self.description
        }
