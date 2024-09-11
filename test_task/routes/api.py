from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import select, func
from loguru import logger

from database import db
from service import UserService, AchievementService, UserAchievementService
from database.models import User, Achievement, UserAchievement


api = Blueprint('api', __name__)

api_version = 'v1'

@api.route(f"/api/{api_version}/users/", methods=['POST'])
def create_user():
    logger.debug('create user')
    data = request.json

    UserService().create_user(data)

    return make_response('', 201)

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

        AchievementService().create_achievement(data)

        return make_response('', 201)

    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500
    
@api.route(f"/api/{api_version}/user_achievements/", methods=['POST'])
def attach_achievement():
    logger.debug('attach achievement')
    try:
        data = request.json

        UserAchievementService().attach_achievement(data)

        return make_response('', 201)
    
    except Exception as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 500

@api.route(f"/api/{api_version}/users/<string:username>/achievement/", methods=['GET'])
def get_users_achivement(username):
    logger.debug('get achievements for users')

    try:
        result = UserService().get_users_achievement(username)

        return jsonify(result), 200
    except Exception as err:
        logger.error(err)

@api.route(f"/api/{api_version}/stats/max_achievements/")
def get_user_with_max_achievements():
    logger.debug('get user with max achivements')

    result = UserService().get_user_with_max_achievements()

    return jsonify(result), 200

@api.route(f"/api/{api_version}/stats/max_points/")
def get_user_with_max_points():
    logger.debug('get user with max points')

    result = UserService().get_user_with_max_points()

    return jsonify(result), 200

@api.route(f"/api/{api_version}/stats/max_min_difference/")
def get_user_with_min_max_difference():
    logger.debug('get user with max and min difference')

    result = UserService().get_user_with_min_max_difference()

    return jsonify(result), 200

@api.route(f"/api/{api_version}/stats/streak_achievements/")
def get_user_with_streak_achievements():
    logger.debug('get user with streak')

    result = UserService().get_user_with_streak_achievements()

    return jsonify(result), 200