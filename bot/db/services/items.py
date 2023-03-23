"""Services (queries) for the Item model"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, delete

from db.models import Item, ItemPhoto
from db.services.categories import get_category

from schemas.admin import ItemModel


async def create_item(session: Session, item_obj: ItemModel) -> None:
    """
    Create the Item instance, photos are list of (file_id)
    """

    category = await get_category(session, item_obj.category_id)
    item = Item(
        title=item_obj.title,
        description=item_obj.description,
        price=item_obj.price,
        stock=item_obj.stock,
        category=category
    )
    item_photo_objects = []
    for photo_id in item_obj.photos:
        obj = ItemPhoto(file_id=photo_id)
        item_photo_objects.append(obj)
    item.photos.extend(item_photo_objects)
    session.add(item)
    await session.commit()


async def get_items_by_category(session: Session, category_id: int) -> list[Item]:
    """Select items by category_id"""

    q = select(Item).where(Item.category_id == category_id)
    res = await session.execute(q)
    return res.scalars().all()


async def get_items_by_category_count(session: Session, category_id: int) -> int:
    """Select COUNT items by category_id"""

    q = select(func.count(Item.id)).where(Item.category_id == category_id)
    res = await session.execute(q)
    return res.scalar()


async def get_items(session: Session) -> list[Item]:
    """Select all items"""

    q = select(Item)
    res = await session.execute(q)
    return res.scalars().all()


async def get_item(session: Session, item_id: int, joined: bool = True) -> Item:
    """Get Item instance"""

    q = select(Item).where(Item.id == item_id)
    if joined:
        q = q.options(joinedload(Item.category), joinedload(Item.photos))
    res = await session.execute(q)
    return res.scalar()


async def get_items_count(session: Session) -> int:
    """Select COUNT items"""

    q = select(func.count(Item.id))
    res = await session.execute(q)
    return res.scalar()


async def delete_item(session: Session, item_id: int) -> None:
    """Delete item by id"""

    q = delete(Item).where(Item.id == item_id)
    await session.execute(q)
    await session.commit()
