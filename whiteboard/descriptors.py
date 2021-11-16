# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from whiteboard.exceptions import InvalidAttributeError

import whiteboard.logger as logger


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        logger.debug(f'Validating {self.public_name} with value {value}.')
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):

    """
    Descriptor to validate numbers.

    :param none_allowed: None is a valid value (default: True).
    :param negative_allowed: Negative numbers are allows (default: True).
    :param float_allowed: Float numbers are allows (default: False).
    """

    def __init__(self,
                 none_allowed=True,
                 negative_allowed=True,
                 float_allowed=False):
        self.none_allowed = none_allowed
        self.negative_allowed = negative_allowed
        self.float_allowed = float_allowed

    def validate(self, value):

        def invalid():
            raise InvalidAttributeError(self.public_name)

        if self.none_allowed and value is None:
            return

        if value is None or isinstance(value, bool):
            invalid()

        if not self.float_allowed and isinstance(value, float):
            invalid()

        try:
            value = int(value)
        except (ValueError, TypeError):
            invalid()

        if not self.negative_allowed and value < 0:
            invalid()


class Bool(Validator):

    """
    Descriptor to validate boolean values.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        self.none_allowed = none_allowed

    def validate(self, value):
        if self.none_allowed and value is None:
            return

        if value is None or not isinstance(value, bool):
            raise InvalidAttributeError(self.public_name)


class String(Validator):

    """
    Descriptor to validate strings.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        self.none_allowed = none_allowed

    def validate(self, value):
        if self.none_allowed and value is None:
            return

        if value is None or not isinstance(value, str):
            raise InvalidAttributeError(self.public_name)


class Id(Number):

    """
    Descriptor to validate ids.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        super(Id, self).__init__(none_allowed=none_allowed,
                                 negative_allowed=False,
                                 float_allowed=False)


class UnixTimestamp(Number):

    """
    Descriptor to validate unix timestamps.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        super(UnixTimestamp, self).__init__(none_allowed=none_allowed,
                                            negative_allowed=False,
                                            float_allowed=False)


class Name(String):

    """
    Descriptor to validate names.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        super(Name, self).__init__(none_allowed=none_allowed)


class Text(String):

    """
    Descriptor to validate text.

    :param none_allowed: None is a valid value (default: True).
    """

    def __init__(self, none_allowed=True):
        super(Text, self).__init__(none_allowed=none_allowed)


class Hash(String):

    """
    Descriptor to validate hashes.

    :param none_allowed: None is a valid value (default: True).
    @todo: Validate hashes!
    """

    def __init__(self, none_allowed=True):
        super(Hash, self).__init__(none_allowed=none_allowed)


class Choice(Validator):

    """
    Descriptor value if it is contained in a given list of values.
    """

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(
                f'Expected {value!r} to be one of {self.options!r}')
