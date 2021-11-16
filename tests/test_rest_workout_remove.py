# -*- coding: utf-8 -*-
import json
import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), (2),
))
def test_rest_remove_workout__valid_workout_id(
        workout_delete, workout_id):
    response = workout_delete(workout_id=workout_id)
    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    assert json_resp['type'] == 'success'
    assert json_resp['message'] == 'Workout successfully removed.'


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_rest_remove_workout__valid_user_id(
        workout_delete, user_id):
    pass


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_rest_remove_workout__not_found_workout(
        workout_delete, workout_id):
    response = workout_delete(workout_id=workout_id)
    assert response.status == '404 NOT FOUND'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == (
        f'Workout with id {workout_id} does not exist.')


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_rest_remove_workout__invalid_user(
        workout_delete, user_id):
    pass


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_rest_remove_workout__not_found_user(
        workout_delete, user_id):
    pass


def test_rest_remove_workout__invalid_empty_user(
        workout_delete):
    pass


def test_rest_remove_workout__unauthorized(workout_delete_no_auth):
    response = workout_delete_no_auth(workout_id=1)
    assert response.status == '401 UNAUTHORIZED'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == 'Authorization required.'
