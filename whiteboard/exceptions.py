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


class EquipmentNotFoundError(Exception):

    """Custom error that raised when a equipment with an id doesn't exist."""

    def __init__(self, equipment_id: int) -> None:
        self.equipment_id = equipment_id
        super().__init__(
            f'Equipment with id {self.equipment_id} does not exist.')


class EquipmentInvalidIdError(Exception):

    """Custom error that raised when a equipment contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid equipment id.')


class EquipmentInvalidNameError(Exception):

    """Custom error that raised when a equipment contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid equipment name.')


class MovementNotFoundError(Exception):

    """Custom error that raised when a movement with an id doesn't exist."""

    def __init__(self, movement_id: int) -> None:
        self.movement_id = movement_id
        super().__init__(
            f'Movement with id {self.movement_id} does not exist.')


class MovementInvalidIdError(Exception):

    """Custom error that raised when a movement contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid movement id.')


class MovementInvalidNameError(Exception):

    """Custom error that raised when a movement contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid movement name.')


class TagNotFoundError(Exception):

    """Custom error that raised when a tag with an id doesn't exist."""

    def __init__(self, tag_id: int) -> None:
        self.tag_id = tag_id
        super().__init__(
            f'Tag with id {self.tag_id} does not exist.')


class TagNoneObjectError(Exception):

    """Custom error that raised when a tag object is None."""

    def __init__(self) -> None:
        super().__init__('Tag object is None.')


class TagInvalidIdError(Exception):

    """Custom error that raised when a tag contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid tag id.')


class TagInvalidNameError(Exception):

    """Custom error that raised when a tag contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid tag name.')
