from fastapi import APIRouter

from . import user,report,searchbill,settings,items,unit

router = APIRouter(prefix="/admin", tags=["Admin API"])

router.include_router(user.userRouter)
router.include_router(report.reportRouter)
router.include_router(searchbill.searchRouter)
router.include_router(settings.settingsRouter)
router.include_router(items.itemRouter)
router.include_router(unit.unitRouter)



