import datetime

from database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

class AchievementTranslate(db.Model, SerializerMixin):
    __tablename__ = 'achievement_translates'

    achievement_translate_id = Column(Integer, primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.achievement_id'), nullable=False)
    achievement_name = Column(String(64), unique=True, nullable=False)
    achievement_description = Column(Text, nullable=False)
    achievement_language = Column(String(16), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.timezone.utc)
    updated_at = Column(TIMESTAMP, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    achievement = db.relationship('Achievement', backref='translations')

    def to_dict(self) -> dict:
        return {
            "achievement_id": self.achievement_id,
            "achievement_name": self.achievement_name,
            "achievement_description": self.achievement_description,
            "achievement_language": self.achievement_language,
        }
