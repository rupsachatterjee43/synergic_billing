from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,AddUnit
from datetime import datetime

unitRouter = APIRouter()

# ==================================================================================================
# Get Unit List

@unitRouter.post('/unit_list')
async def unit_list(data:CompId):

    select = "sl_no,unit_name,created_by,created_at, modified_by,modified_at"
    table_name = f"md_unit"
    where = f"comp_id={data.comp_id}"
    order = ""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Add And Edit New Unit

@unitRouter.post('/add_unit_details')
async def add_unit_details(data:AddUnit):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if ({data.unit_id}.pop())>0:

        table_name = "md_unit"
        fields = f"unit_name = '{data.unit_name}', modified_by='admin', modified_at = '{formatted_dt}' "
        print(formatted_dt)
        values =f"{data.unit_id},{data.comp_id},'{data.unit_name}','admin','{formatted_dt}'"
        where = f"comp_id={data.comp_id} and sl_no={data.unit_id}"
        order = f""
        flag = 1
        res_dt = await db_Insert(table_name,fields,values,where,flag)
    else:
        table_name = "md_unit"
        fields = "comp_id, unit_name, created_by, created_at"
        values =f"{data.comp_id},'{data.unit_name}','admin','{formatted_dt}'"
        where = f""
        print(data.unit_id)
        order = f""
        flag = 0
        res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt