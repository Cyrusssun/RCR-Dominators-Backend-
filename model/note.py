from sqlalchemy import Column, String, Integer, Text
from datetime import datetime
import random, string

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import app, db


class Note(db.Model):
    __tablename__ = 'notes'

    id         = Column(Integer, primary_key=True)
    author     = Column(String(100), nullable=False, default='Anonymous')
    content    = Column(Text, nullable=False)
    image_data = Column(Text, nullable=True)   # base64 encoded image
    image_type = Column(String(30), nullable=True)  # e.g. 'image/jpeg'
    likes      = Column(Integer, nullable=False, default=0)
    created_at = Column(String(50), nullable=False)

    def __init__(self, author, content, image_data=None, image_type=None):
        self.author     = author or 'Anonymous'
        self.content    = content
        self.image_data = image_data
        self.image_type = image_type
        self.likes      = 0
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id':         self.id,
            'author':     self.author,
            'content':    self.content,
            'image_data': self.image_data,
            'image_type': self.image_type,
            'likes':      self.likes,
            'created_at': self.created_at,
        }

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
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


def initNotes():
    with app.app_context():
        db.create_all()
        # No sample data needed