from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,AddEditHeaderFooter
from datetime import datetime

headerfooterRouter = APIRouter()

@headerfooterRouter.post('/header_footer_details')
async def header_footer_details(data:CompId):
    select = "*"
    table_name = "md_header_footer"
    where = f"comp_id = {data.comp_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Add Header Footer

@headerfooterRouter.post('/add_header_footer')
async def add_header_footer(data:AddEditHeaderFooter):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_header_footer"
    fields = "comp_id, header1, on_off_flag1, header2, on_off_flag2, footer1, on_off_flag3, footer2, on_off_flag4, created_by, created_at"
    values =f"{data.comp_id}, '{data.header1}', '{data.on_off_flag1}', '{data.header2}', '{data.on_off_flag2}', '{data.footer1}', '{data.on_off_flag3}', '{data.footer2}', '{data.on_off_flag4}', 'Admin', '{formatted_dt}'"
    where = None
    flag = 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt

# ==================================================================================================
# Edit Header Footer

@headerfooterRouter.post('/edit_header_footer')
async def edit_header_footer(data:AddEditHeaderFooter):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_header_footer"
    fields = f"header1 = '{data.header1}', on_off_flag1 = '{data.on_off_flag1}', header2 = '{data.header2}', on_off_flag2 = '{data.on_off_flag2}', footer1 = '{data.footer1}', on_off_flag3 = '{data.on_off_flag3}', footer2 = '{data.footer2}', on_off_flag4 = '{data.on_off_flag4}', modified_by = 'Admin', modified_at = '{formatted_dt}'"
    values = None
    where = f"comp_id={data.comp_id}"
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt