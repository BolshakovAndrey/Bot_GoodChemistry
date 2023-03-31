"""Admin-side pydantic schemas"""

import datetime

from typing import TypeVar

from pydantic import BaseModel, Field, condecimal, validator

T = TypeVar("T", bound=str)


def must_not_digit(title: T) -> T:
    if title.isdigit():
        raise ValueError("Название не должно быть числом.")
    return title


class CategoryModel(BaseModel):
    """Category schema"""

    title: str = Field(max_length=50)
    _must_not_digit_title = validator("title", allow_reuse=True)(must_not_digit)


class ItemModel(BaseModel):
    """Item schema"""

    title: str = Field(max_length=50)
    description: str = ""
    photos: list[str]
    price: condecimal(max_digits=12, decimal_places=2)
    category_id: int
    stock: int

    _must_not_digit_title = validator("title", allow_reuse=True)(must_not_digit)
