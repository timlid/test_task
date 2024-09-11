from repository import AchievementRepository

class AchievementService():
    def __init__(self) -> None:
        self.repo = AchievementRepository()

    def create_achievement(self, data: dict):
        self.repo.insert_one(data)