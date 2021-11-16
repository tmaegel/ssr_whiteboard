# -*- coding: utf-8 -*-
from flask import current_app, request
from functools import wraps
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import User

import jwt
import whiteboard.logger as logger


def token_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        logger.debug('Verifing token.')
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace(
                'Bearer', '').strip()

        if not token:
            logger.error('Authorization required.')
            return {'type': 'error', 'message': 'Authorization required.'}, 401

        try:
            # Decoding the payload to fetch the stored details
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User(data['sub'], data['name'], None).get()
        except (jwt.InvalidTokenError, jwt.DecodeError) as e:
            logger.error(str(e))
            return {'type': 'error', 'message': 'Token is invalid.'}, 401
        except (InvalidAttributeError, NotFoundError) as e:
            logger.error(str(e))
            return {'type': 'error', 'message': str(e)}, 401

        return func(user, *args, **kwargs)

    return _wrapper
