from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import UserLogin,CompId,UserList
# testing git
userRouter = APIRouter()

# ==================================================================================================
# User List

@userRouter.post('/user_list')
async def user_login(data:UserList):
    select = "user_name,user_id"
    table_name = "md_user"
    where = f"comp_id = {data.comp_id} and br_id = {data.br_id} and user_type!='A'"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# Verify Phone no and active status
#------------------------------------------------------------------------------------------------------
@userRouter.post('/user_login')
async def user_login(data_login:UserLogin):
    select = "a.*, b.*, c.*"
    table_name = "md_user a, md_branch b, md_company c"
    where = f"a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id AND a.active_flag='Y'"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Outlet Details

@userRouter.post('/outlet_list')
async def outlet_list(data:CompId):
    select = "id,branch_name,branch_address,location,contact_person,phone_no,email_id"
    table_name = "md_branch"
    where = f"comp_id = {data.comp_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt


