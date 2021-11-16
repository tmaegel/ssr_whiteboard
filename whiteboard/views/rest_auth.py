# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import current_app
from flask_restful import reqparse, Resource
from werkzeug.exceptions import BadRequest
from whiteboard.exceptions import (
    InvalidAttributeError,
    InvalidPasswordError,
    NotFoundError,
)
from whiteboard.models.user import User

import jwt
import whiteboard.logger as logger

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, location='json',
                    help='Username cannot be parsed.')
parser.add_argument('password', required=True, location='json',
                    help='Password cannot be parsed.')


class Login(Resource):

    def post(self):
        token = None

        try:
            args = parser.parse_args()
        except BadRequest:
            return {
                'type': 'error',
                'message': 'Missing arguments in payload.'
            }, 400

        try:
            user = User.authenticate(args['username'], args['password'])
        except InvalidAttributeError as e:
            logger.error(str(e))
            return {'type': 'error', 'message': str(e)}, 400
        except InvalidPasswordError as e:
            logger.error(str(e))
            return {'type': 'error', 'message': str(e)}, 401
        except NotFoundError as e:
            logger.error(str(e))
            return {'type': 'error', 'message': str(e)}, 404

        if user and hasattr(user, 'user_id') and hasattr(user, 'name'):
            payload = {
                'sub': user.user_id,
                'name': user.name,
                'exp': datetime.utcnow() + timedelta(minutes=60)
            }
            token = jwt.encode(
                payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        if not token:
            return {
                'type': 'error',
                'message': 'Something went wrong.'
            }, 400

        return {
            'user_id': user.user_id,
            'name': user.name,
            'token': token
        }, 200
