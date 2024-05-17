from fastapi import APIRouter

from . import user, report, searchbill, settings

router = APIRouter(prefix="/admin", tags=["Admin API"])

router.include_router(user.userRouter)
router.include_router(report.reportRouter)
router.include_router(searchbill.searchRouter)
router.include_router(settings.settingsRouter)

