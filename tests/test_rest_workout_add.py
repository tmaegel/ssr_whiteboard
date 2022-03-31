# -*- coding: utf-8 -*-
import json

import pytest


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_rest_add_workout__valid_user_id(workout_post, workout_dict, user_id):
    response = workout_post(workout_data=workout_dict)
    assert response.status == "201 CREATED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "success"
    assert json_resp["message"] == "Workout successfully added."


# @todo
def test_rest_update_workout__valid_name(workout_post, workout_dict):
    pass


# @todo
def test_rest_update_workout__valid_description(workout_post, workout_dict):
    pass


@pytest.mark.parametrize(
    ("datetime"),
    (
        (123),
        ("123"),
    ),
)
def test_rest_update_workout__valid_datetime(workout_post, workout_dict, datetime):
    workout = workout_dict
    workout["datetime"] = datetime
    response = workout_post(workout_data=workout)
    assert response.status == "201 CREATED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "success"
    assert json_resp["message"] == "Workout successfully added."


def test_rest_update_workout__valid_empty_datetime(workout_post, workout_dict):
    workout = workout_dict
    del workout["datetime"]
    response = workout_post(workout_data=workout)
    assert response.status == "201 CREATED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "success"
    assert json_resp["message"] == "Workout successfully added."


@pytest.mark.parametrize(
    ("user_id"),
    (
        (-1),
        ("1.0"),
        (None),
        ("abc"),
        (True),
        (False),
    ),
)
def test_rest_add_workout__invalid_user(workout_post, workout_dict, user_id):
    workout = workout_dict
    workout["user_id"] = user_id
    response = workout_post(workout_data=workout)
    assert response.status == "400 BAD REQUEST"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Invalid user id."


@pytest.mark.parametrize(
    ("user_id"),
    (
        (0),
        (99999),
    ),
)
def test_rest_add_workout__not_found_user(workout_post, workout_dict, user_id):
    workout = workout_dict
    workout["user_id"] = user_id
    response = workout_post(workout_data=workout)
    assert response.status == "404 NOT FOUND"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == (f"User with id or name {user_id} does not exist.")


def test_rest_add_workout__invalid_empty_user(workout_post, workout_dict):
    workout = workout_dict
    del workout["user_id"]
    response = workout_post(workout_data=workout)
    assert response.status == "400 BAD REQUEST"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Missing arguments in payload."


# @todo
def test_rest_add_workout__invalid_name(workout_post, workout_dict):
    pass


def test_rest_add_workout__invalid_empty_name(workout_post, workout_dict):
    workout = workout_dict
    del workout["name"]
    response = workout_post(workout_data=workout)
    assert response.status == "400 BAD REQUEST"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Missing arguments in payload."


# @todo
def test_rest_add_workout__invalid_description(workout_post, workout_dict):
    pass


def test_rest_add_workout__invalid_empty_description(workout_post, workout_dict):
    workout = workout_dict
    del workout["description"]
    response = workout_post(workout_data=workout)
    assert response.status == "400 BAD REQUEST"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Missing arguments in payload."


@pytest.mark.parametrize(
    ("datetime"),
    (
        (-1),
        (True),
        ([]),
        ("abc"),
        ("123.45"),
        (123.45),
    ),
)
def test_rest_add_workout__invalid_datetime(workout_post, workout_dict, datetime):
    workout = workout_dict
    workout["datetime"] = datetime
    response = workout_post(workout_data=workout)
    assert response.status == "400 BAD REQUEST"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Invalid workout datetime."


def test_rest_add_workout__unauthorized(workout_post_no_auth, workout_dict):
    response = workout_post_no_auth(workout_data=workout_dict)
    assert response.status == "401 UNAUTHORIZED"
    assert response.headers["Content-Type"] == "application/json"
    json_resp = json.loads(response.data.decode("utf-8"))
    assert json_resp["type"] == "error"
    assert json_resp["message"] == "Authorization required."
