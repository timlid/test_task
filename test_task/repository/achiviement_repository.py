from sqlalchemy import func
from loguru import logger

from database.models import Achievement, AchievementTranslate
from database import db

class AchievementRepository:
    def __init__(self) -> None:
        self.model = Achievement
        self.db = db

    def insert_one(self, data: dict) -> None:
        try:
            new_achievement = Achievement(
                achievement_point = data.get('achievement_point'),
                created_at = func.now(),
                updated_at = func.now(),
            )

            self.db.session.add(new_achievement)
            self.db.session.commit()
            
            for achievement in data['achievement_translation']:
                new_achievement_translation = AchievementTranslate(
                    achievement_id = new_achievement.achievement_id,
                    achievement_name = achievement.get('achievement_name'),
                    achievement_description = achievement.get('achievement_description'),
                    achievement_language = achievement.get('achievement_language'),
                    created_at = func.now(),
                    updated_at = func.now()
                )

                self.db.session.add(new_achievement_translation)
                self.db.session.commit()    
                
        except Exception as err:
            logger.debug(err)
            self.db.session.rollback()