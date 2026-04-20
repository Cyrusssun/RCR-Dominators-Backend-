from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

class RailroadUser(db.Model):
    __tablename__ = 'railroad_users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email.lower()
        # 使用 pbkdf2:sha256 代替 scrypt（兼容 Python 3.9）
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.created_at = datetime.now().isoformat()
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def update_password(self, new_password):
        self.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }

def initRailroadUsers():
    """初始化铁路用户表"""
    db.create_all()