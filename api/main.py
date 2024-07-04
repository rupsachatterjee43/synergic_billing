from fastapi import APIRouter

from . import user, unit, transaction, stock, settings, report, refund, recovery, master, items, category, cancelbill, calculator

router = APIRouter(prefix="/api", tags=["Mobile API"])

router.include_router(user.userRouter)
router.include_router(unit.unitRouter)
router.include_router(transaction.tnxRouter)
router.include_router(stock.stockRouter)
router.include_router(settings.setRouter)
router.include_router(report.repoRouter)
router.include_router(refund.refRouter)
router.include_router(recovery.recoRouter)
router.include_router(master.masterRouter)
router.include_router(items.itmRouter)
router.include_router(category.categoryRouter)
router.include_router(cancelbill.cancelRouter)
router.include_router(calculator.CalRouter)


