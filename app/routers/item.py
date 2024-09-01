from fastapi import APIRouter, Depends, HTTPException, Form, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_account
from app.db.database import get_db_session
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.crud import item as crud

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
async def create_item(
        name: str = Form(...),
        description: str = Form(...),
        category: str = Form(...),
        quantity: int = Form(...),
        price: int = Form(...),
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account),
):
    try:
        item_schema = ItemCreate(
            name=name,
            description=description,
            category=category,
            quantity=quantity,
            price=price,
        )
    except ValueError as e:
        raise HTTPException(detail=str(e))

    new_item = await crud.create_item(
        db=session,
        item_schema=item_schema,
    )

    return new_item


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ItemResponse])
async def get_items(
        limit: int = Query(10, description="items to retrieve"),
        offset: int = Query(0, description="items to skip"),
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    items = await crud.get_items(session, limit, offset)
    return items


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
async def get_item_by_id(
        item_id: int,
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    item = await crud.get_item(session, item_id)
    return item


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
async def update_item_by_id(
        item_id: int,
        name: str = Form(None),
        description: str = Form(None),
        category: str = Form(None),
        quantity: int = Form(None),
        price: int = Form(None),
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    try:
        item_schema = ItemUpdate(
            name=name,
            description=description,
            category=category,
            quantity=quantity,
            price=price,
        )
    except ValueError as e:
        raise HTTPException(detail=str(e))

    updated_item = await crud.update_item(
        session, item_id, item_schema
    )
    return updated_item


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
async def delete_item_by_id(
        item_id: int,
        session: AsyncSession = Depends(get_db_session),
        current_account: dict = Depends(get_current_account)
):
    deleted_item = await crud.delete_item(session, item_id)
    return deleted_item
