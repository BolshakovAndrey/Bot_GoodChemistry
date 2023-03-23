"""Services (queries) for the Order model"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from db.models import Order, UserItem

from db.services.items import get_item
from db.services.users import get_user, get_user_item

from schemas.client import OrderModel


async def get_unpaid_orders(session: Session) -> list[Order]:
    """Get unpaid orders"""

    q = (
        select(Order)
        .where(Order.paid == False)
        .options(joinedload(Order.item))
    )
    res = await session.execute(q)
    return res.scalars().all()


async def get_order(session: Session, order_id: int, joined: bool = True) -> Order:
    """Get order instance"""

    q = select(Order).where(Order.id == order_id)
    if joined:
        q = q.options(joinedload(Order.item))
    res = await session.execute(q)
    return res.scalar()


async def get_unpaid_orders_count(session: Session) -> list[Order]:
    """Get unpaid orders count"""

    q = select(func.count(Order.id)).where(Order.paid == False)
    res = await session.execute(q)
    return res.scalar()


async def create_order(session: Session, order_obj: OrderModel) -> Order:
    """Create the Order instance"""

    order = Order()

    if order_obj.item_id:
        item = await get_item(session, order_obj.item_id)
        order.item = item

    user = await get_user(session, order_obj.user_id)

    order.user = user
    order.summ = order_obj.summ
    order.quantity = order_obj.quantity

    if order_obj.item_id:
        user_item = await get_user_item(session, order_obj.item_id, order.user_id)

        if user_item:
            user_item.quantity = user_item.quantity + order.quantity
        else:
            session.add(
                UserItem(
                    user_id=order.user_id,
                    item_id=order.item_id,
                    quantity=order.quantity,
                )
            )

    session.add(order)
    await session.commit()

    return order

async def pay_order(session: Session, order_id: int) -> None:
    """Make order paid"""

    order = await get_order(session, order_id, joined=False)

    if order.item_id:
        user_item = await get_user_item(session, order.item_id, order.user_id)

        if user_item:
            user_item.quantity = user_item.quantity + order.quantity
        else:
            session.add(
                UserItem(
                    user_id=order.user_id,
                    item_id=order.item_id,
                    quantity=order.quantity,
                )
            )

    order.paid = True

    await session.commit()
