from typing import TypeVar

from pydantic import BaseModel, Field, root_validator

T = TypeVar("T", bound=dict)


class OrderModel(BaseModel):
    """Order schema"""

    item_id: int = None
    service_id: int = None
    user_id: int
    summ: int = None
    quantity: int = 1

    @root_validator
    def check_item_id_or_order_id(cls, values: T) -> T:
        """Check that item_id not empty"""

        item_id = values.get("item_id")
        if not item_id:
            raise ValueError("Вы должны указать либо id товара.")

        return values

    @root_validator
    def check_not_item(cls, values: T) -> T:
        """Check not item_id"""

        item_id = values.get("item_id")

        if item_id:
            raise ValueError("Если вы указали id товара.")

        return values
