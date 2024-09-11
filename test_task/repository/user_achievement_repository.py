from sqlalchemy import select, func

from database import UserAchievement, db, User, AchievementTranslate

class UserAchievementRepository():
    def __init__(self) -> None:
        self.model = UserAchievement
        self.db = db

    def attach_one(self, data: dict):
        user_id = select(User).where(User.username == data['username'])
        achievement_id = select(AchievementTranslate).where(AchievementTranslate.achievement_name == data['achievement_name'])

        user_result = db.session.execute(user_id)
        achievement_result = db.session.execute(achievement_id)

        new_user_achievement = UserAchievement(
            user_id=user_result.first()[0].to_dict()['user_id'],
            achievement_id=achievement_result.first()[0].to_dict()['achievement_id'],
            created_at=func.now(),
            updated_at=func.now()
        )

        db.session.add(new_user_achievement)
        db.session.commit()