from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.models import OrderModel, OrderMenuAssociation
from src.core.schemas.orders import (
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)


async def create_order(
    session: AsyncSession,
    order_in: OrderCreateSchema,
) -> OrderModel:
    order = OrderModel(**order_in.model_dump())
    session.add(order)
    await session.commit()
    order = await session.scalar(
        select(OrderModel)
        .where(OrderModel.id == order.id)
        .options(
            selectinload(OrderModel.menu_items_details),
        ),
    )
    return order


async def get_order_one(
    session: AsyncSession,
    pk: int,
) -> OrderModel | None:
    return await session.get(OrderModel, pk)


async def get_order_list(session: AsyncSession, fltr=None) -> List[OrderModel]:
    if not fltr:
        fltr = {}
    query = (
        select(OrderModel)
        .options(
            selectinload(OrderModel.menu_items_details).joinedload(
                OrderMenuAssociation.menu_item
            ),
        )
        .filter_by(**fltr)
        .order_by(OrderModel.id)
    )
    orders = await session.scalars(query)
    return list(orders)


async def update_order(
    session: AsyncSession,
    order: OrderModel,
    order_update: OrderUpdateSchema | OrderUpdatePartialSchema,
    partial: bool = False,
) -> OrderModel:
    for key, value in order_update.model_dump(exclude_unset=partial).items():
        setattr(order, key, value)
    await session.commit()
    await session.refresh(order)
    return order


async def delete_order(
    session: AsyncSession,
    order: OrderModel,
) -> None:
    await session.delete(order)
    await session.commit()
