from enum import Enum


class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

    @classmethod
    def from_string(cls, value: str):
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Неизвестная роль: {value}")