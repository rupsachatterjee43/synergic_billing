from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,DiscountSettings,GSTSettings,GeneralSettings
from datetime import datetime

settingsRouter = APIRouter()

# ==================================================================================================
# All Settings Details

@settingsRouter.post('/settings_details')
async def settings_details(data:CompId):

    select = "b.company_name, a.*"
    table_name = f"md_receipt_settings a, md_company b"
    where = f"a.comp_id = b.id AND a.comp_id = {data.comp_id}"
    order = ""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Edit Discount Settings

@settingsRouter.post('/edit_discount_settings')
async def edit_discount_settings(data:DiscountSettings):

    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_receipt_settings"
    fields = f"discount_flag='{data.discount_flag}', discount_type='{data.discount_type}', discount_position='{data.discount_position}', modified_by='{data.modified_by}', modified_at='{formatted_dt}'"
    values = None
    where = f"comp_id = {data.comp_id}"
    order = ""
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# ==================================================================================================
# Edit GST Settings

@settingsRouter.post('/edit_gst_settings')
async def edit_gst_settings(data:GSTSettings):

    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_receipt_settings"
    fields = f"gst_flag='{data.gst_flag}', gst_type='{data.gst_type}', modified_by='{data.modified_by}', modified_at='{formatted_dt}'"
    values = None
    where = f"comp_id = {data.comp_id}"
    order = ""
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# ==================================================================================================
# Edit General Settings

@settingsRouter.post('/edit_general_settings')
async def edit_general_settings(data:GeneralSettings):

    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_receipt_settings"
    fields = f"rcv_cash_flag='{data.rcv_cash_flag}' ,rcpt_type='{data.rcpt_type}', unit_flag='{data.unit_flag}', cust_inf='{data.cust_inf}', pay_mode='{data.pay_mode}', stock_flag='{data.stock_flag}', price_type='{data.price_type}', refund_days='{data.refund_days}', kot_flag='{data.kot_flag}', modified_by='{data.modified_by}', modified_at='{formatted_dt}'"
    values = None
    where = f"comp_id = {data.comp_id}"
    order = ""
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt