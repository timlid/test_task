from database.database import db
from sqlalchemy import Integer, Column, String, TIMESTAMP, CheckConstraint
from sqlalchemy_serializer import SerializerMixin
import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    language = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.timezone.utc)
    updated_at = Column(TIMESTAMP, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    achievements = db.relationship('Achievement', secondary='user_achievements', 
                                   backref=db.backref('users', lazy='dynamic'))
    
    def __str__(self) -> str:
        return f'User : {self.username}'