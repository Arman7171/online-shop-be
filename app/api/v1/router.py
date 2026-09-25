from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.categories import router as category_router
from app.api.v1.product import router as product_router
from app.api.v1.cart import router as cart_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(cart_router)