"""Admin-side main handlers"""

from aiogram import types

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Group, Row, Start
from aiogram_dialog.widgets.text import Const

from dialog.dialog_state import (
    AdminSG,
    DeleteCategorySG,
    DeleteItemSG,
    CreateCategorySG,
    CreateItemSG,
    OrdersSG,
)

from sqlalchemy.orm import Session

admin_window = Window(
    Const("Привет админ! Вот опции которые тебе доступны:"),
    Group(
        Row(
            Start(
                Const("Удалить категорию"),
                id="deletecategory",
                state=DeleteCategorySG.list_of_categories_to_delete,
            ),
            Start(
                Const("Удалить товар"),
                id="deleteitem",
                state=DeleteItemSG.list_of_items_categories,
            ),
        ),
        Row(
            Start(
                Const("Добавить категорию"),
                id="addcategory",
                state=CreateCategorySG.start_create_category,
            ),
            Start(
                Const("Добавить товар"),
                id="additem",
                state=CreateItemSG.start_create_item,
            ),
        ),
        Row(
            Start(
                Const("Заказы"),
                id="orders",
                state=OrdersSG.list_of_orders),
        ),
    ),
    state=AdminSG.admin,
)


async def admin(
    message: types.Message, dialog_manager: DialogManager, db_session: Session
):
    """
    This handler will be called when user sends `/admin` command

    Admin main menu.
    """

    await dialog_manager.start(AdminSG.admin, mode=StartMode.RESET_STACK)


admin_dialog = Dialog(admin_window)
