from sqlalchemy import select, and_, func
from loguru import logger


from database import User, db

class DatabaseRequestError(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        return f"database request error: {self.error_message}"


class UserRepository:
    def __init__(self) -> None:
            self.model = User
            self.db = db

    def find_one(self, filter: dict):
        try:
            conditions = [getattr(self.model, key) == value for key, value in filter.items()]
        
            query = select(self.model).where(and_(*conditions))

            result = self.db.session.execute(query).scalar_one_or_none()
            
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