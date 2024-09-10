from database.database import db
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
import datetime

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.achievement_id'), primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.timezone.utc)
    updated_at = Column(TIMESTAMP, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)
