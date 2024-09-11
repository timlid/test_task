from repository import UserAchievementRepository

class UserAchievementService():
    def __init__(self) -> None:
        self.repo = UserAchievementRepository()

    def attach_achievement(self, data: dict):
        self.repo.attach_one(data)