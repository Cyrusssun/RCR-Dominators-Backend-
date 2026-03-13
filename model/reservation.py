from sqlalchemy import Column, String, Integer, Float
from datetime import datetime
import random, string

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import db


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id           = Column(Integer, primary_key=True)
    confirm_code = Column(String(20),  nullable=False, unique=True)
    date         = Column(String(10),  nullable=False)   # YYYY-MM-DD
    time         = Column(String(5),   nullable=False)   # HH:MM
    train_type   = Column(String(50),  nullable=False)
    first_name   = Column(String(100), nullable=False)
    last_name    = Column(String(100), nullable=False)
    email        = Column(String(200), nullable=False)
    phone        = Column(String(30),  nullable=False)
    adults       = Column(Integer,     nullable=False, default=0)
    children     = Column(Integer,     nullable=False, default=0)
    infants      = Column(Integer,     nullable=False, default=0)
    total_seats  = Column(Integer,     nullable=False)   # adults + children
    total_price  = Column(Float,       nullable=False)
    created_at   = Column(String(50),  nullable=False)

    def __init__(self, date, time, train_type, first_name, last_name,
                 email, phone, adults, children, infants):
        self.date        = date
        self.time        = time
        self.train_type  = train_type
        self.first_name  = first_name
        self.last_name   = last_name
        self.email       = email
        self.phone       = phone
        self.adults      = adults
        self.children    = children
        self.infants     = infants
        self.total_seats = adults + children   # infants don't take seats
        self.total_price = self._calc_price(train_type, adults, children)
        self.confirm_code = self._generate_code()
        self.created_at  = datetime.now().isoformat()

    def _calc_price(self, train_type, adults, children):
        adult_price = 4.0 if 'speeder' in train_type.lower() else 5.0
        return (adults * adult_price) + (children * 2.0)

    def _generate_code(self):
        for _ in range(10):
            code = 'PMR-' + ''.join(random.choices(string.digits, k=6))
            existing = db.session.query(Reservation).filter_by(confirm_code=code).first()
            if not existing:
                return code
        return 'PMR-' + ''.join(random.choices(string.digits, k=9))

    def to_dict(self):
        return {
            "id":           self.id,
            "confirm_code": self.confirm_code,
            "date":         self.date,
            "time":         self.time,
            "train_type":   self.train_type,
            "first_name":   self.first_name,
            "last_name":    self.last_name,
            "email":        self.email,
            "phone":        self.phone,
            "adults":       self.adults,
            "children":     self.children,
            "infants":      self.infants,
            "total_seats":  self.total_seats,
            "total_price":  self.total_price,
            "created_at":   self.created_at
        }

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            return None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def __repr__(self):
        return f'Reservation: {self.confirm_code} | {self.date} {self.time} | {self.first_name} {self.last_name}'


def booked_seats(date_str, time_str):
    """Return total seats already reserved for a specific ride."""
    result = db.session.query(
        db.func.coalesce(db.func.sum(Reservation.total_seats), 0)
    ).filter_by(date=date_str, time=time_str).scalar()
    return int(result)


def initReservations():
    with app.app_context():
        db.create_all()  # 确保 reservations 表存在
        with db.session.no_autoflush:
            if not db.session.query(Reservation).first():
                pass  # No sample data needed