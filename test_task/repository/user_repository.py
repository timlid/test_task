from sqlalchemy import select, and_, func
from loguru import logger


from database import User, UserAchievement, Achievement, AchievementTranslate, db

class DatabaseRequestError(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        return f"database request error: {self.error_message}"


class NoneTypeResult(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        return f"none result in used query: {self.error_message}"


class UserRepository:
    def __init__(self) -> None:
            self.model = User
            self.db = db

    def find_one(self, data: dict):
        try:
            conditions = [getattr(self.model, key) == value for key, value in data.items()]
        
            query = select(self.model).where(and_(*conditions))

            result = self.db.session.execute(query).scalar_one_or_none()

            if result is None:
                raise NoneTypeResult
            
            return result

        except Exception as err:
             logger.error(err)
             raise DatabaseRequestError(err)
        
    def insert_one(self, data: dict):
        try:
            new_user = User(
                username=data.get('username'),
                language=data.get('language'),
                created_at=func.now(),
                updated_at=func.now()
            )

            self.db.session.add(new_user)
            self.db.session.commit()

            return new_user
    
        except Exception as err:
            logger.error(err)
            raise DatabaseRequestError(err)
        
    def find_one_with_relation(self, data: dict):
        user = self.find_one(data)

        user_achievements = db.session.query(Achievement, AchievementTranslate, User)\
            .join(Achievement, AchievementTranslate.achievement_id == Achievement.achievement_id)\
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.achievement_id)\
            .join(User, User.user_id == UserAchievement.user_id)\
            .filter(UserAchievement.user_id == user.to_dict()['user_id'], AchievementTranslate.achievement_language == user.language)\
            .all()
        
        return user_achievements