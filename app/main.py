from fastapi import FastAPI, HTTPException, Depends, status

from app.routers.item import router as items_router
from app.routers.account import router as accounts_router

app = FastAPI()

app.include_router(accounts_router)
app.include_router(items_router)
