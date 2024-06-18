from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import AddEditLocation
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

