# -*- coding: utf-8 -*-
import json
import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), (2),
))
def test_rest_get_workout__valid(workout_get, workout_id):
    response = workout_get(workout_id)
    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('workout_id', 'user_id', 'name', 'description', 'datetime'):
        assert attr in json_resp


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_rest_get_workout__not_found_workout(workout_get, workout_id):
    response = workout_get(workout_id)
    assert response.status == '404 NOT FOUND'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == (
        f'Workout with id {workout_id} does not exist.')


def test_rest_get_workout_list__valid(workout_list_get):
    response = workout_list_get
    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    assert len(json_resp) > 0
    for attr in ('workout_id', 'user_id', 'name', 'description', 'datetime'):
        assert attr in json_resp[0]
