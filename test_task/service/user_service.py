from repository import UserRepository, DatabaseRequestError
from flask import jsonify

class UserError(Exception):
    def __init__(self, error_message: str, username: str) -> None:
        self.error_message = error_message
        self.username = username


class CreateUserError(UserError):
    def __init__(self, error_message: str, username: str) -> None:
        super().__init__(error_message, username)

    def __str__(self) -> str:
        return f"create user ({self.username}) error: {self.error_message}"


class GetUserError(Exception):
    def __init__(self, error_message: str, username: str) -> None:
        super().__init__(error_message, username)

    def __str__(self) -> str:
        return f"get user ({self.username}) error: {self.error_message}"


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    def get_user_by_username(self, username: str):
        try:
            return self.repo.find_one({"username": username})
        except DatabaseRequestError as err:
            raise GetUserError(err)
    
    def create_user(self, data: dict):
        try:
            if data['user_language'] not in ['en', 'ru']:
                return jsonify({
                    "message": "Доступно только два языка en и ru"
                })

            return self.repo.insert_one(data)

        except DatabaseRequestError as err:
            raise CreateUserError(err)
        
    def get_users_achievement(self, username: str) -> dict:
        try:
            result = self.repo.find_one_with_relation({"username": username})
            achievements_list = [{
                "username": user.username,
                "user_language": user.user_language,
                "achievement_name": translation.achievement_name,
                "achievement_point": achievement.achievement_point,
                "achievement_description": translation.achievement_description,
                "awarded_at": achievement.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for achievement, translation, user in result]
            return achievements_list
        except DatabaseRequestError as err:
            raise GetUserError(err)
        
    def get_user_with_max_achievements(self) -> dict:
        return self.repo.find_max_count_achievements()
    
    def get_user_with_max_points(self) -> dict:
        return self.repo.find_max_count_points()
    
    def get_user_with_min_max_difference(self) -> dict:
        return self.repo.find_mix_max_difference()
    
    def get_user_with_streak_achievements(self) -> dict:
        return self.repo.find_streak_with_achievement()