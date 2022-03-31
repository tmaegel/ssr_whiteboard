# -*- coding: utf-8 -*-
import json

import pytest


@pytest.mark.parametrize(
    ("workout_id"),
    (
        (1),
        (2),
    ),
)
def test_rest_get_workout__valid(workout_get, workout_id):
    response = workout_get(workout_id)
    assert response.status == "200 OK"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    for attr in ("workout_id", "user_id", "name", "description", "datetime"):
        assert attr in json_resp


@pytest.mark.parametrize(
    ("workout_id"),
    (
        (0),
        (99999),
    ),
)
def test_rest_get_workout__not_found_workout(workout_get, workout_id):
    response = workout_get(workout_id)
    assert response.status == "404 NOT FOUND"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == (f"Workout with id {workout_id} does not exist.")


# @todo
def test_rest_get_workout__invalid_user(workout_get):
    pass


def test_rest_get_workout__unauthorized(workout_get_no_auth):
    response = workout_get_no_auth(1)
    assert response.status == "401 UNAUTHORIZED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Authorization required."


def test_rest_get_workout_list__valid(workout_list_get):
    response = workout_list_get
    assert response.status == "200 OK"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert len(json_resp) > 0
    for attr in ("workout_id", "user_id", "name", "description", "datetime"):
        assert attr in json_resp[0]


# @todo
def test_rest_get_workout_list__invalid_user(workout_list_get):
    pass


def test_rest_get_workout_list__unauthorized(workout_list_get_no_auth):
    response = workout_list_get_no_auth
    assert response.status == "401 UNAUTHORIZED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Authorization required."
