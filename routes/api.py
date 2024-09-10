from flask import Blueprint, jsonify, request
from database.models import User, Achievement
from database import db
from sqlalchemy import select
from sqlalchemy import func

import datetime 
from loguru import logger

api = Blueprint('api', __name__)

api_version = 'v1'

@api.route(f"/api/{api_version}/users/", methods=['POST'])
def create_user():
    try:
        logger.debug('create user')
        data = request.json

        if data['language'] not in ['en', 'ru']:
            return jsonify({
                "message": "Доступно только два языка en и ru"
            })

        new_user = User(
            username=data['username'],
            language=data['language'],
            created_at=func.now(),
            updated_at=func.now()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
                'message': 'User created successfully',
                'user_id': new_user.user_id,
                'username': new_user.username,
                'language': new_user.language
            }), 201

    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500
    
@api.route(f'/api/{api_version}/users/<string:username>', methods=['GET'])
def get_user_by_username(username: str):
    logger.debug('get user')

    try:
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        logger.debug(result)

        return jsonify(result.one()[0].to_dict())

    except Exception as err:
        logger.error(err)
        return jsonify({
            "error": str(err)
        }), 500
