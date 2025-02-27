from fastapi import APIRouter
from .user import router as user_router
from .equipment import router as equipment_router
from .rentals import router as rentals_router

router = APIRouter(prefix="/api")

router.include_router(user_router)
router.include_router(equipment_router)
router.include_router(rentals_router)
