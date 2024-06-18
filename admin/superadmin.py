from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import AddEditLocation, AddEditCompany
from datetime import datetime

superadminRouter = APIRouter()

# Manage Location
# ========================================================================================================
#-----------Select Location List---------------------

@superadminRouter.get('/S_Admin/select_location')
async def select_location():
    select = "sl_no,location_name"
    table_name = "md_location"
    where = f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ---------------Add And Edit Location-----------------

@superadminRouter.post('/S_Admin/add_edit_location')
async def add_edit_location(data:AddEditLocation):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_location"
    fields = f"location_name='{data.location_name}', modified_by='{data.user_id}', modified_at='{formatted_dt}'" if data.sl_no>0 else f"location_name, created_by, created_at"
    values = None if data.sl_no>0 else f"'{data.location_name}', '{data.user_id}', '{formatted_dt}'"
    where = f"sl_no = {data.sl_no}" if data.sl_no>0 else None
    order = ""
    flag = 1 if data.sl_no>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# =====================================================================================================
# Manage Shop(Company)

# -------------------Select Company-----------------
@superadminRouter.get('/S_Admin/select_shop')
async def select_shop():
    select = "id,company_name,address,phone_no,email_id,active_flag,max_user"
    table_name = "md_company"
    where = f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# -------------------Add And Edit Shop-----------------
@superadminRouter.post('/S_Admin/add_edit_shop')
async def add_edit_shop(data:AddEditCompany):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_company"
    fields = f"company_name='{data.company_name}', address='{data.address}', location={data.location}, contact_person='{data.contact_person}', phone_no={data.phone_no}, email_id='{data.email_id}', logo='{data.logo}',web_portal='{data.web_portal}',active_flag='{data.active_flag}',max_user={data.max_user},modified_by='{data.user_id}', modified_dt='{formatted_dt}'" if data.id>0 else f"company_name,address,location,contact_person,phone_no,email_id,logo,web_portal,active_flag,max_user,created_by, created_dt"
    values = None if data.id>0 else f"'{data.company_name}','{data.address}',{data.location},'{data.contact_person}',{data.phone_no},'{data.email_id}','{data.logo}','{data.web_portal}','{data.active_flag}',{data.max_user},'{data.user_id}', '{formatted_dt}'"
    where = f"id = {data.id}" if data.id>0 else None
    order = ""
    flag = 1 if data.id>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# =======================================================================================================
# Manage User

# --------------Select All Users-------------
@superadminRouter.get('/S_Admin/select_user')
async def select_user():
    select = "id,comp_id,br_id,user_name,user_type,user_id,phone_no,email_id,active_flag,login_flag"
    table_name = "md_user"
    where = f""
    order = f"ORDER BY comp_id,br_id,user_type"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ---------------Add And Edit User---------------