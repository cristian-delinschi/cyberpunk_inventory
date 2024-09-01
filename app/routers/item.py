from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db_session
from app.models.item import Item
from app.core.auth import get_current_account

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def create_item(
        name: str, description: str, category: str, quantity: int, price: int,
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    async with session.begin():
        new_item = Item(name=name, description=description, category=category, quantity=quantity, price=price)
        session.add(new_item)
        await session.commit()

    return {"name": name}


@router.get("")
async def get_items(
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    async with session.begin():
        result = await session.execute(select(Item))
        items = result.scalars().all()

        return [
            {
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in items
        ]
