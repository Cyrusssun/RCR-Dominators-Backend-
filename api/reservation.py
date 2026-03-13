from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime, date

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import db
from model.reservation import Reservation, booked_seats

# ── PMRR schedule data ───────────────────────────────────────────────────────
EXPLICIT_SUNDAYS = {
    '2026-03-08': None,
    '2026-03-15': 'Cable Car',   '2026-03-22': 'Speeder',
    '2026-03-29': 'Cable Car',
    '2026-04-05': 'Cable Car',   '2026-04-12': None,
    '2026-04-19': 'Cable Car',   '2026-04-26': 'Speeder',
    '2026-05-03': 'Cable Car',   '2026-05-10': None,
    '2026-05-17': 'Cable Car',   '2026-05-24': 'Speeder',
    '2026-05-31': 'Cable Car',
}

SAT_TIMES = ['10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45',
             '12:00','12:15','12:30','12:45','13:00','13:15','13:30','13:45']
SUN_TIMES = ['11:00','11:20','11:40','12:00','12:20','12:40','13:00','13:20','13:45']


def get_day_schedule(date_str):
    """Returns schedule dict or None if no operation."""
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

    dow = d.weekday()  # 0=Mon … 5=Sat, 6=Sun

    if dow == 5:  # Saturday
        return {'train_type': 'Steam Locomotive', 'times': SAT_TIMES, 'capacity': 65}

    if dow == 6:  # Sunday
        if date_str in EXPLICIT_SUNDAYS:
            train_type = EXPLICIT_SUNDAYS[date_str]
            if train_type is None:
                return None
            return {'train_type': train_type, 'times': SUN_TIMES, 'capacity': 30}
        if 8 <= d.day <= 14:  # 2nd Sunday default
            return None
        return {'train_type': 'Cable Car', 'times': SUN_TIMES, 'capacity': 30}

    return None  # Weekday


# ── Blueprint setup ──────────────────────────────────────────────────────────
reservation_bp = Blueprint('reservation', __name__)
reservation_api = Api(reservation_bp)


class ScheduleAPI(Resource):
    def get(self):
        date_str = request.args.get('date', date.today().isoformat())
        sched = get_day_schedule(date_str)

        if sched is None:
            return {'date': date_str, 'operating': False, 'rides': []}, 200

        rides = []
        for t in sched['times']:
            booked    = booked_seats(date_str, t)
            available = sched['capacity'] - booked
            rides.append({
                'time':       t,
                'train_type': sched['train_type'],
                'capacity':   sched['capacity'],
                'booked':     booked,
                'available':  available,
                'status':     'full' if available == 0 else 'available'
            })

        return {
            'date':       date_str,
            'operating':  True,
            'train_type': sched['train_type'],
            'rides':      rides
        }, 200


class ReservationListAPI(Resource):
    def get(self):
        """List all reservations (admin use)."""
        all_res = db.session.query(Reservation).order_by(
            Reservation.date, Reservation.time
        ).all()
        return [r.to_dict() for r in all_res], 200

    def post(self):
        """Create a new reservation."""
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400

        required = ['date', 'time', 'train_type', 'first_name', 'last_name',
                    'email', 'phone', 'adults', 'children', 'infants']
        for field in required:
            if field not in data:
                return {'error': f'Missing field: {field}'}, 400

        date_str    = data['date']
        time_str    = data['time']
        adults      = int(data['adults'])
        children    = int(data['children'])
        infants     = int(data['infants'])
        total_seats = adults + children

        if adults < 1:
            return {'error': 'At least 1 adult required'}, 400

        # Validate ride exists
        sched = get_day_schedule(date_str)
        if sched is None or time_str not in sched['times']:
            return {'error': 'Invalid date or departure time'}, 400

        # Check seat availability
        already_booked = booked_seats(date_str, time_str)
        remaining = sched['capacity'] - already_booked
        if total_seats > remaining:
            return {
                'error':     'Not enough seats available',
                'available': remaining,
                'requested': total_seats
            }, 409

        # Create and save
        reservation = Reservation(
            date       = date_str,
            time       = time_str,
            train_type = data['train_type'],
            first_name = data['first_name'],
            last_name  = data['last_name'],
            email      = data['email'],
            phone      = data['phone'],
            adults     = adults,
            children   = children,
            infants    = infants
        )

        result = reservation.create()
        if not result:
            return {'error': 'Failed to save reservation'}, 500

        return {
            'confirm_code':          result.confirm_code,
            'date':                  result.date,
            'time':                  result.time,
            'train_type':            result.train_type,
            'name':                  f"{result.first_name} {result.last_name}",
            'adults':                result.adults,
            'children':              result.children,
            'infants':               result.infants,
            'total_seats':           result.total_seats,
            'total_price':           result.total_price,
            'seats_remaining_after': remaining - result.total_seats
        }, 201


class ReservationDetailAPI(Resource):
    def get(self, code):
        """Look up a reservation by confirmation code."""
        r = db.session.query(Reservation).filter_by(
            confirm_code=code.upper()
        ).first()
        if not r:
            return {'error': 'Reservation not found'}, 404
        return r.to_dict(), 200


reservation_api.add_resource(ScheduleAPI,          '/api/schedule')
reservation_api.add_resource(ReservationListAPI,   '/api/reservations')
reservation_api.add_resource(ReservationDetailAPI, '/api/reservations/<string:code>') 