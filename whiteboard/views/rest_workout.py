# -*- coding: utf-8 -*-
import json

from flask import Response
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

import whiteboard.logger as logger
from whiteboard.controller import token_required
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout

parser = reqparse.RequestParser()
parser.add_argument(
    "name", required=True, location="json", help="Workout name cannot be parsed."
)
parser.add_argument(
    "description",
    required=True,
    location="json",
    help="Workout description name cannot be parsed.",
)
parser.add_argument(
    "user_id", required=True, location="json", help="Workout user id cannot be parsed."
)
parser.add_argument(
    "datetime",
    required=False,
    location="json",
    help="Workout datetime cannot be parsed.",
)


class WorkoutList(Resource):

    # Decorators that will be added to all method functions in resource.
    decorators = [token_required]

    def get(self, user):
        logger.debug("Getting workouts.")
        try:
            # @todo: pass right user_id
            workouts = Workout.list(user_id=user.user_id)
        except (NotFoundError, InvalidAttributeError) as e:
            logger.debug(str(e))
            return {"type": "error", "message": str(e)}, 404

        return Response(
            response=json.dumps([workout.__dict__ for workout in workouts]),
            mimetype="application/json",
            status=200,
        )

    def post(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return {"type": "error", "message": "Missing arguments in payload."}, 400

        # datetime is an optional argument
        if args["datetime"]:
            _workout = Workout(
                workout_id=None,
                user_id=args["user_id"],
                name=args["name"],
                description=args["description"],
                datetime=args["datetime"],
            )
        else:
            _workout = Workout(
                workout_id=None,
                user_id=args["user_id"],
                name=args["name"],
                description=args["description"],
            )

        try:
            result = _workout.add()
        except InvalidAttributeError as e:
            return {"type": "error", "message": str(e)}, 400
        except NotFoundError as e:
            return {"type": "error", "message": str(e)}, 404

        if not result:
            return {"type": "error", "message": "Something went wrong."}, 400

        return {"type": "success", "message": "Workout successfully added."}, 201


class WorkoutEnty(Resource):

    # Decorators that will be added to all method functions in resource.
    decorators = [token_required]

    def get(self, workout_id):
        # @todo: pass user_id
        _workout = Workout(workout_id)
        try:
            workout = _workout.get()
        except NotFoundError as e:
            return {"type": "error", "message": str(e)}, 404

        return Response(
            response=workout.to_json(), mimetype="application/json", status=200
        )

    def put(self, workout_id):
        # @todo: pass user_id
        try:
            args = parser.parse_args()
        except BadRequest:
            return {"type": "error", "message": "Missing arguments in payload."}, 400

        # datetime is an optional argument
        if args["datetime"]:
            _workout = Workout(
                workout_id=workout_id,
                user_id=args["user_id"],
                name=args["name"],
                description=args["description"],
                datetime=args["datetime"],
            )
        else:
            _workout = Workout(
                workout_id=workout_id,
                user_id=args["user_id"],
                name=args["name"],
                description=args["description"],
            )

        try:
            result = _workout.update()
        except InvalidAttributeError as e:
            return {"type": "error", "message": str(e)}, 400
        except NotFoundError as e:
            return {"type": "error", "message": str(e)}, 404

        if not result:
            return {"type": "error", "message": "Something went wrong."}, 400

        return {"type": "success", "message": "Workout successfully updated."}, 200

    def delete(self, workout_id):
        user_id = 1  # @todo: get the right user id
        _workout = Workout(workout_id=workout_id, user_id=user_id)

        try:
            result = _workout.remove()
        except InvalidAttributeError as e:
            return {"type": "error", "message": str(e)}, 400
        except NotFoundError as e:
            return {"type": "error", "message": str(e)}, 404

        if not result:
            return {"type": "error", "message": "Something went wrong."}, 400

        return {"type": "success", "message": "Workout successfully removed."}
