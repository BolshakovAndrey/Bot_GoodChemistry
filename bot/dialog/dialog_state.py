"""Aiogram dialog StatesGroup's """

from aiogram.fsm.state import StatesGroup, State


# Client


class ClientSG(StatesGroup):
    """Client StatesGroup"""

    start = State()


class CategoriesSG(StatesGroup):
    """Category StatesGroup"""

    list_of_categories = State()


class ItemsSG(StatesGroup):
    """Items StatesGroup"""

    list_of_category_items = State()


class ItemSG(StatesGroup):
    """Item detail StatesGroup"""

    item_detail = State()


class CreateItemOrderSG(StatesGroup):
    """Create item order StatesGroup"""

    create_item_order = State()
    set_order_quantity = State()
    item_order_created = State()


class UserItemsSG(StatesGroup):
    """User items StatesGroup"""

    user_items = State()


# Admin


class AdminSG(StatesGroup):
    """Admin StatesGroup"""

    admin = State()


class DeleteCategorySG(StatesGroup):
    """Delete category StatesGroup"""

    list_of_categories_to_delete = State()


class DeleteItemSG(StatesGroup):
    """Delete item StatesGroup"""

    list_of_items_categories = State()
    list_of_category_items_to_delete = State()


class CreateCategorySG(StatesGroup):
    """Create category StatesGroup"""

    start_create_category = State()

class CreateItemSG(StatesGroup):
    """Create item StatesGroup"""

    start_create_item = State()
    set_item_description = State()
    set_item_photos = State()
    set_item_price = State()
    set_item_category_id = State()
    set_item_shops = State()


class OrdersSG(StatesGroup):
    """Orders StatesGroup"""

    list_of_orders = State()


class OrderSG(StatesGroup):
    """Order StatesGroup"""

    order_details = State()

