from fastapi import FastAPI, HTTPException, Depends, status

from app.routers.item import router as items_router
from app.routers.account import router as users_router

app = FastAPI()

# Routers
app.include_router(users_router)
app.include_router(items_router)
