from typing import Union


class UserNotFoundError(Exception):

    """Custom error that raised when a user with an id doesn't exist."""

    def __init__(self, identifier: Union[int, str]) -> None:
        self.identifier = identifier
        super().__init__(
            f'User with id or name {self.identifier} does not exist.')


class UserInvalidIdError(Exception):

    """Custom error that raised when a user contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid user id.')


class UserInvalidNameError(Exception):

    """Custom error that raised when a user contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid user name.')


class WorkoutNotFoundError(Exception):

    """Custom error that raised when a workout with an id doesn't exist."""

    def __init__(self, workout_id: int) -> None:
        self.workout_id = workout_id
        super().__init__(f'Workout with id {self.workout_id} does not exist.')


class WorkoutNoneObjectError(Exception):

    """Custom error that raised when a workout object is None."""

    def __init__(self) -> None:
        super().__init__('Workout object is None.')


class WorkoutInvalidIdError(Exception):

    """Custom error that raised when a workout contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid workout id.')


class WorkoutInvalidNameError(Exception):

    """Custom error that raised when a workout contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid workout name.')


class WorkoutInvalidDescriptionError(Exception):

    """
    Custom error that raised when a workout contains a invalid description.
    """

    def __init__(self) -> None:
        super().__init__('Invalid workout description.')


class WorkoutInvalidTimestampError(Exception):

    """Custom error that raised when a workout contains a invalid timestamp."""

    def __init__(self) -> None:
        super().__init__('Invalid workout timestamp.')
