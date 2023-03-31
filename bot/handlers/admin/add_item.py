"""Admin-side add item handlers"""

from typing import Any

from pydantic import ValidationError

from aiogram import types

from aiogram_dialog import Window, DialogManager, Dialog

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Next,
    ScrollingGroup,
    Select,
    Button,
    SwitchTo,
)

from schemas.admin import ItemModel

from db.services.items import create_item as create_item_service

from sqlalchemy.exc import DBAPIError

from dialog.dialog_state import CreateItemSG
from dialog.data_getters import get_categories_data



async def create_item(message: types.Message, widget: Any, manager: DialogManager):
    """Create the item"""
    item = ItemModel(**manager.dialog_data)

    await create_item_service(
        manager.middleware_data.get("db_session"),
        item,
    )

    await message.answer("Товар успешно добавлен!")
    # Stop the dialog
    await manager.done()


async def set_item_shops(message: types.Message, widget: Any, manager: DialogManager):
    """Set item and create it"""

    try:
        item = ItemModel(**manager.dialog_data)

        # Set the window as the current window for the manager
        await manager.current_window(set_item_shops_window)

    except (ValidationError, DBAPIError) as err:
        await message.answer("Произошла ошибка при добавлении товара!")

    await manager.done()


set_item_shops_window = Window(
    Const("Создание товара"),
    Button(Const("Создать товар"), id="itemcreated", on_click=create_item),
    Button(Const("Отмена"), id="itemcancel", on_click=Cancel()),
    state=CreateItemSG.set_item_shops,
)


# Set quantity of the item in the stock
async def set_item_stock(
        message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set item quantity in the stock"""

    manager.dialog_data["stock"] = input

    await manager.switch_to(CreateItemSG.set_item_shops)


set_item_stock_window = Window(
    Const(
        "Введите начальное количество товара на складе"
    ),
    TextInput("itemquantity", str, on_success=set_item_stock),
    state=CreateItemSG.set_item_stock,
)


async def set_item_category_id(
        message: types.Message, widget: Any, manager: DialogManager, category_id: int
):
    """Set item category_id"""

    manager.dialog_data["category_id"] = category_id

    await manager.switch_to(CreateItemSG.set_item_stock)


set_item_category_id_window = Window(
    Const("Выберите категорию товара"),
    ScrollingGroup(
        Select(
            Format("{item.title}"),
            "itemcatselsel",
            lambda category: category.id,
            "categories",
            on_click=set_item_category_id,
        ),
        width=2,
        height=4,
        id="itemcatsel",  # item category select
    ),
    state=CreateItemSG.set_item_category_id,
    getter=get_categories_data,
)


async def set_item_price(
        message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set item price"""

    manager.dialog_data["price"] = input

    await manager.switch_to(CreateItemSG.set_item_category_id)


set_item_price_window = Window(
    Const(
        "Введите цену товара, не больше 12 цифр в числе и не больше 2 цифр после запятой.\nПример: 9999999999.99"
    ),
    TextInput("itempriceinp", str, on_success=set_item_price),
    state=CreateItemSG.set_item_price,
)


async def set_item_photos(message: types.Message, widget: Any, manager: DialogManager):
    """Set item photos"""

    photos: list = manager.dialog_data.get("photos")
    if not photos:
        manager.dialog_data["photos"] = []
    manager.dialog_data.get("photos").extend([message.photo[-1].file_id])


async def item_photos_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    """Data getter for set_item_photos window"""

    selected_photos = dialog_manager.dialog_data.get("photos", [])
    return {"photos_count": len(selected_photos)}


set_item_photos_window = Window(
    Const("Отправьте фотографии товара"),
    Format("Выбрано {photos_count} фото", when="photos_count"),
    MessageInput(set_item_photos, content_types=types.ContentType.PHOTO),
    SwitchTo(Const("Дальше"), id="tosetitemprice", state=CreateItemSG.set_item_price),
    state=CreateItemSG.set_item_photos,
    getter=item_photos_getter,
)


async def set_item_description(
        message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set item description"""

    manager.dialog_data["description"] = input
    await manager.switch_to(CreateItemSG.set_item_photos)


set_item_description_window = Window(
    Const("Введите описание товара"),
    Next(Const("Пропустить")),
    TextInput("itemdescinp", str, on_success=set_item_description),
    state=CreateItemSG.set_item_description,
)


async def set_item_title(
        message: types.Message, widget: Any, manager: DialogManager, input: str
):
    """Set item title"""

    manager.dialog_data["title"] = input

    await manager.switch_to(CreateItemSG.set_item_description)


start_create_item_window = Window(
    Const("Введите название товара, не более 50 символов."),
    Cancel(Const("Отмена")),
    TextInput("itemnameinp", str, on_success=set_item_title),
    state=CreateItemSG.start_create_item,
)

create_item_dialog = Dialog(
    start_create_item_window,
    set_item_description_window,
    set_item_photos_window,
    set_item_price_window,
    set_item_category_id_window,
    set_item_stock_window,
    set_item_shops_window,
)
