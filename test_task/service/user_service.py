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
            if data['language'] not in ['en', 'ru']:
                return jsonify({
                    "message": "Доступно только два языка en и ru"
                })

            return self.repo.insert_one(data)

        except DatabaseRequestError as err:
            raise CreateUserError(err)