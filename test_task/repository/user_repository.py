from sqlalchemy import select, and_, func, desc
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
        logger.debug(data)
        try:
            new_user = User(
                username=data.get('username'),
                user_language=data.get('user_language'),
                created_at=func.now(),
                updated_at=func.now()
            )

            self.db.session.add(new_user)
            self.db.session.commit()

            return new_user
    
        except Exception as err:
            logger.error(err)
            raise DatabaseRequestError(err)
        
    def find_one_with_relation(self, data: dict) -> dict:
        user = self.find_one(data)

        user_achievements = db.session.query(Achievement, AchievementTranslate, User)\
            .join(Achievement, AchievementTranslate.achievement_id == Achievement.achievement_id)\
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.achievement_id)\
            .join(User, User.user_id == UserAchievement.user_id)\
            .filter(UserAchievement.user_id == user.to_dict()['user_id'], AchievementTranslate.achievement_language == user.user_language)\
            .all()
        
        return user_achievements
    
    def find_max_count_achievements(self) -> dict:
        user = db.session.query(
            User, func.count(UserAchievement.achievement_id).label('total_achievements')
        ).join(UserAchievement).group_by(User.user_id).order_by(desc('total_achievements')).first()

        return {
            "user_id": user[0].user_id,
            "username": user[0].username,
            "total_achievements": user[1]
            }

    def find_max_count_points(self) -> dict:
        user = db.session.query(
            User, func.sum(Achievement.achievement_point).label('total_points')
        )\
        .join(UserAchievement, User.user_id == UserAchievement.user_id)\
        .join(Achievement, Achievement.achievement_id == UserAchievement.achievement_id)\
        .group_by(User.user_id).order_by(desc('total_points'))\
        .first()

        return {
            "user_id": user[0].user_id,
            "username": user[0].username,
            "total_points": user[1]
        }
    
    def find_mix_max_difference(self) -> dict:
        user_points = db.session.query(
            User.user_id, User.username, func.sum(Achievement.achievement_point).label('total_points')
        )\
        .join(UserAchievement, User.user_id == UserAchievement.user_id)\
        .join(Achievement, Achievement.achievement_id == UserAchievement.achievement_id)\
        .group_by(User.user_id).all()

        users_data = [
            {
                "user_id": user_id,
                "username": username,
                "total_points": total_points
            }
            for user_id, username, total_points in user_points
        ]

        sorted_users = sorted(users_data, key=lambda x: x['total_points'])

        max_diff = sorted_users[-1]['total_points'] - sorted_users[0]['total_points']
        return {
                "max_difference": max_diff,
                "users_with_max_difference": {
                    "max_points_user": sorted_users[-1],
                    "min_points_user": sorted_users[0]
                }
        }
    
    def find_streak_with_achievement(self):
        users_with_streak = db.session.query(
            User.user_id, User.username
        ).join(UserAchievement).group_by(User.user_id).having(
            func.count(func.distinct(func.date(UserAchievement.created_at))) >= 7
        ).all()

        result = [{
            "user_id": user.user_id,
            "username": user.username
        } for user in users_with_streak]

        return result