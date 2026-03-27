from sqlalchemy import Column, String, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import db


class RailroadUser(db.Model):
    __tablename__ = 'railroad_users'

    id         = Column(Integer,     primary_key=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(200), nullable=False, unique=True)
    password   = Column(String(255), nullable=False)
    created_at = Column(String(50),  nullable=False)

    def __init__(self, name, email, password):
        self.name       = name
        self.email      = email.lower()
        self.password   = generate_password_hash(password)
        self.created_at = datetime.now().isoformat()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_password(self, new_password):
        self.password = generate_password_hash(new_password)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'created_at': self.created_at
        }

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception:
            db.session.rollback()
            return None

    def __repr__(self):
        return f'RailroadUser: {self.email}'


def initRailroadUsers():
    with db.session.no_autoflush:
        pass  # No sample data needed
