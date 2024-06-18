from fastapi import APIRouter

from . import user,report,searchbill,settings,items,unit,headerfooter,customer,stock,purchase,superadmin

router = APIRouter(prefix="/admin", tags=["Admin API"])


router.include_router(user.userRouter)
router.include_router(report.reportRouter)
router.include_router(searchbill.searchRouter)
router.include_router(settings.settingsRouter)
router.include_router(items.itemRouter)
router.include_router(unit.unitRouter)
router.include_router(headerfooter.headerfooterRouter)
router.include_router(customer.customerRouter)
router.include_router(stock.stockRouter)
router.include_router(purchase.purchaseRouter)
router.include_router(superadmin.superadminRouter)






