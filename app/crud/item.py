from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def item_dict(item):
    return {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "category": item.category,
        "quantity": item.quantity,
        "price": item.price
    }


async def create_item(db: AsyncSession, item_schema: ItemCreate) -> dict[str, Any]:
    result = await db.execute(select(Item).filter(Item.name == item_schema.name))
    existing_item = result.scalars().first()

    if existing_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")

    new_item = Item(
        name=item_schema.name,
        description=item_schema.description,
        category=item_schema.category,
        quantity=item_schema.quantity,
        price=item_schema.price
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return item_dict(new_item)


async def get_item(db: AsyncSession, item_id: int) -> dict[str, Any]:
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return item_dict(item)


async def get_items(db: AsyncSession, limit: int, offset: int) -> list[dict[str, Any]]:
    result = await db.execute(select(Item).limit(limit).offset(offset))
    items = result.scalars().all()

    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Items not found")

    return [item_dict(item) for item in items]


async def update_item(db: AsyncSession, item_id: int, item_schema: ItemUpdate) -> dict[str, Any]:
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    for attribute, value in item_schema.dict(exclude_unset=True).items():
        if value is not None:
            setattr(item, attribute, value)

    await db.commit()
    await db.refresh(item)

    return item_dict(item)


async def delete_item(db: AsyncSession, item_id: int) -> dict[str, Any]:
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await db.delete(item)
    await db.commit()

    return item_dict(item)
