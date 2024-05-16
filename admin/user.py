from fastapi import APIRouter

# testing git
userRouter = APIRouter()


# Verify Phone no and active status
#------------------------------------------------------------------------------------------------------
@userRouter.post('/test')
async def test(phone_no:int):
    return f"Your Phone no is {phone_no}"