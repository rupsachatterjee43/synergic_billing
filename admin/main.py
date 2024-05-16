from fastapi import APIRouter

from . import user

router = APIRouter(prefix="/admin", tags=["Admin API"])

router.include_router(user.userRouter)