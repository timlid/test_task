from database.database import db
from sqlalchemy import Column, String, Integer, Text, CheckConstraint, TIMESTAMP

import datetime
from sqlalchemy_serializer import SerializerMixin

class Achievement(db.Model, SerializerMixin):
    __tablename__ = 'achievements'

    achievement_id = Column(Integer, primary_key=True)
    achievement_name = Column(String(64), unique=True, nullable=False)
    achievement_description = Column(Text, nullable=False)
    achievement_point = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.timezone.utc)
    updated_at = Column(TIMESTAMP, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    __table_args__ = (
        CheckConstraint(achievement_point > 0, name='check_points_positive'),
    )