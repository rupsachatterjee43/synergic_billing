from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import UserLogin,CompId,UserList,AddUser,EditUser
from utils import get_hashed_password,verify_password
from datetime import datetime


# testing git
userRouter = APIRouter()

# ==================================================================================================
# User List

@userRouter.post('/user_list')
async def user_list(data:UserList):
    select = "*"
    table_name = "md_user"
    where = f"comp_id = {data.comp_id} {f'and br_id = {data.br_id}' if data.br_id > 0 else ''} and user_type!='A'"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# Verify Phone no and active status
#------------------------------------------------------------------------------------------------------
@userRouter.post('/user_login')
async def user_login(data_login:UserLogin):
    # pwd = get_hashed_password(data_login.password)
    # print(pwd)
    res_dt = {}
    select = "a.*, b.*, c.*"
    table_name = "md_user a, md_branch b, md_company c"
    where = f"a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id AND a.active_flag='Y'"
    order = f''
    flag = 0
    result = await db_select(select,table_name,where,order,flag)
    if(result['suc'] > 0 and result['suc'] < 2):
        if(verify_password(data_login.password, result['msg']['password'])):
            res_dt = {"suc": 1, "msg": [result['msg']]}
        else:
            res_dt = {"suc": 2, "msg": "Please check your userID or password"}
    elif(result['suc'] == 2):
        res_dt = {"suc": 2, "msg": "Please check your userID or password"}
    else:
        res_dt = {"suc": 0, "msg": "No Data Found"}

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

# ==================================================================================================
# User Management

@userRouter.post('/add_user')
async def add_user(data:AddUser):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_user"
    fields = "comp_id, br_id, user_name, user_type, user_id, phone_no, email_id, active_flag, login_flag, created_by, created_dt"
    values =f"{data.comp_id}, '{data.br_id}', '{data.user_name}', '{data.user_type}', '{data.phone_no}', '{data.phone_no}', '{data.email_id}', '{data.active_flag}', '{data.login_flag}', 'Admin', '{formatted_dt}'"
    where = None
    flag = 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt

@userRouter.post('/edit_user')
async def edit_user(data:EditUser):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_user"
    fields = f"user_name = '{data.user_name}', user_type = '{data.user_type}', phone_no = '{data.phone_no}', login_flag = '{data.login_flag}', active_flag = '{data.active_flag}', modified_by = 'Admin', modified_dt = '{formatted_dt}'"
    values = None
    where = f"comp_id={data.comp_id} and user_id='{data.user_id}' and user_type!='A'"
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt