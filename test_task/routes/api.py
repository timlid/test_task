from flask import Blueprint, jsonify, request
from database.models import User, Achievement, UserAchievement
from sqlalchemy import select, func
from loguru import logger

from database import db
from service import UserService

api = Blueprint('api', __name__)

api_version = 'v1'

@api.route(f"/api/{api_version}/users/", methods=['POST'])
def create_user():
    logger.debug('create user')
    data = request.json

    UserService().create_user(data)

    return jsonify({
            'message': 'User created successfully',
        }), 200

@api.route(f'/api/{api_version}/users/<string:username>', methods=['GET'])
def get_user_by_username(username: str):
    logger.debug('get user')

    result = UserService().get_user_by_username(username)
    json_user = result.to_dict()

    return jsonify(json_user), 200

@api.route(f"/api/{api_version}/achievements/", methods=['POST'])
def create_achievement():
    try:
        logger.debug('create achievement')
        data = request.json

        new_achievement = Achievement(
            achievement_name=data['achievement_name'],
            achievement_description=data['achievement_description'],
            achievement_point=data['achievement_point'],
            created_at=func.now(),
            updated_at=func.now()
        )

        db.session.add(new_achievement)
        db.session.commit()

        return jsonify({
                'message': 'Achievement created successfully',
                'achievement_name': new_achievement.achievement_name,
                'achievement_description': new_achievement.achievement_description,
                'achievement_point': new_achievement.achievement_point
            }), 201

    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500
    
@api.route(f"/api/{api_version}/user_achievements/", methods=['POST'])
def attach_achievement():
    logger.debug('attach achievement')
    try:
        data = request.json

        user_id = select(User).where(User.username == data['username'])
        achievement_id = select(Achievement).where(Achievement.achievement_name == data['achievement_name'])

        user_result = db.session.execute(user_id)
        achievement_result = db.session.execute(achievement_id)

        new_user_achievement = UserAchievement(
            user_id=user_result.one()[0].to_dict()['user_id'],
            achievement_id=achievement_result.one()[0].to_dict()['achievement_id'],
            created_at=func.now(),
            updated_at=func.now()
        )

        db.session.add(new_user_achievement)
        db.session.commit()

        return jsonify({
            "message": "Sucessfuly created",
            "user_id": new_user_achievement.user_id,
            "achievement_id": new_user_achievement.achievement_id
        }), 201
    
    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500