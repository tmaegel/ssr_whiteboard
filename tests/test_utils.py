import pytest
import time
from whiteboard.utils import (
    is_float, is_timestamp, is_datetime, timestamp_to_sec, datetime_to_sec,
    get_format_timestamp
)


# test is_float function with valid values
@pytest.mark.parametrize(('value'), (
    ('99.99'),
    ('9.0'),
    ('99'),
))
def test_valid_float(value):
    assert is_float(value) is True


# test is_float function with invalid values
@pytest.mark.parametrize(('value'), (
    ('99,99'),
    ('-99.99'),
    ('-99'),
    ('abc'),
    (''),
))
def test_invalid_float(value):
    assert is_float(value) is False


# test is_datetime function with valid values
@pytest.mark.parametrize(('value'), (
    ('1.1.2020 20:30'),
    ('10.10.2020 20:30'),
    ('1.10.2020 20:30'),
    ('01.10.2020 20:30'),
    ('10.1.2020 20:30'),
    ('10.01.2020 20:30'),
    ('10.10.2020 2:30'),
    ('10.10.2020 20:3'),
    ('10.10.2020 20:30:45'),
    ('10.10.2020 20:30:4'),
    ('1.1.2020 00:00'),
    ('1.1.2020 00:00:00'),
))
def test_valid_datetime(value):
    assert is_datetime(value) is True


# test is_datetime function with invalid values
@pytest.mark.parametrize(('value'), (
    ('1.1.2020'),
    ('1.1.2020 20'),
    ('1.1.2020_20:30'),
    ('20:30'),
    ('1.1.20 20:30'),
    (''),
))
def test_invalid_datetime(value):
    assert is_datetime(value) is False


# test is_timestamp function with valid values
@pytest.mark.parametrize(('value'), (
    ('20:30'),
    ('02:30'),
    ('2:30'),
    ('20:03'),
    ('20:3'),
    ('20:30:45'),
    ('20:30:05'),
    ('20:30:5'),
    ('2:3:5'),
    ('2:3'),
    ('00:00'),
    ('00:00:00'),
))
def test_valid_timestamp(value):
    assert is_timestamp(value) is True


# test is_timestamp function with invalid values
@pytest.mark.parametrize(('value'), (
    ('2'),
    ('203'),
    ('203:30'),
    ('20:300'),
    ('20:30:450'),
    (''),
))
def test_invalid_timestamp(value):
    assert is_timestamp(value) is False


# test get_format_timestamp function with valid values and no parameter
def test_valid_format_timestamp_no_parameter():
    assert get_format_timestamp() == time.strftime(
        "%d.%m.%Y %H:%M",
        time.localtime(time.time()))


# test get_format_timestamp function with valid values and parameter
@pytest.mark.parametrize(('value', 'result'), (
    (1577907000, '01.01.2020 20:30'),
))
def test_valid_format_timestamp_with_parameter(value, result):
    assert get_format_timestamp(value) == result


# test get_format_timestamp function with invalid values
@pytest.mark.parametrize(('value'), (
    ('203:30'),
    ('20:300'),
    ('20:30:450'),
    ('abc'),
))
def test_invalid_format_timestamp(value):
    assert get_format_timestamp(value) == -1


# test timestamp_to_sec function with valid values
@pytest.mark.parametrize(('value', 'result'), (
    ('20:30', 73800),
    ('02:30', 9000),
    ('2:30', 9000),
    ('20:03', 72180),
    ('20:3', 72180),
    ('20:30:45', 73845),
    ('20:30:05', 73805),
    ('20:30:5', 73805),
    ('2:3:5', 7385),
    ('2:3', 7380),
    ('00:00', 0),
    ('00:00:00', 0),
    ('2', 2),
    ('203', 203),
    ('20.3', 20),
))
def test_valid_timestamp_to_sec(value, result):
    assert timestamp_to_sec(value) == result


# test timestamp_to_sec function with invalid values
@pytest.mark.parametrize(('value'), (
    ('203:30'),
    ('20:300'),
    ('20:30:450'),
    (''),
))
def test_invalid_timestamp_to_sec(value):
    assert timestamp_to_sec(value) == -1


# test datetime_to_sec function with valid values
# Test based on timezone: Europe/Berlin
@pytest.mark.parametrize(('value', 'result'), (
    ('1.1.2020 20:30', 1577907000),
    ('10.10.2020 20:30', 1602354600),
    ('1.10.2020 20:30', 1601577000),
    ('01.10.2020 20:30', 1601577000),
    ('10.1.2020 20:30', 1578684600),
    ('10.01.2020 20:30', 1578684600),
    ('10.10.2020 2:30', 1602289800),
    ('10.10.2020 20:3', 1602352980),
    ('10.10.2020 20:30:45', 1602354645),
    ('10.10.2020 20:30:4', 1602354604),
    ('1.1.2020 00:00', 1577833200),
    ('1.1.2020 00:00:00', 1577833200),
))
def test_valid_datetime_to_sec(value, result):
    assert datetime_to_sec(value) == result


# test datetime_to_sec function with invalid values
@pytest.mark.parametrize(('value'), (
    ('1.1.2020'),
    ('1.1.2020 20'),
    ('1.1.2020_20:30'),
    ('20:30'),
    ('1.1.20 20:30'),
    (''),
))
def test_invalid_datetime_to_sec(value):
    assert datetime_to_sec(value) == -1
