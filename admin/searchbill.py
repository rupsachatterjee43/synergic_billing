from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import SearchByDate,SearchByPhone,SearchByItem

searchRouter = APIRouter()

# ==================================================================================================
# Search Bill by Date

@searchRouter.post('/search_by_date')
async def search_by_date(data:SearchByDate):

    select = "receipt_no,trn_date,created_by,net_amt,pay_mode"
    table_name = "td_receipt"
    where = f"comp_id = {data.comp_id} AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Search Bill by Customer Phone No.

@searchRouter.post('/search_by_phone')
async def search_by_phone(data:SearchByPhone):

    select = "receipt_no,trn_date,created_by,net_amt,pay_mode"
    table_name = "td_receipt"
    where = f"comp_id = {data.comp_id} AND phone_no = {data.phone_no} AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Search Bill by Customer Product

@searchRouter.post('/search_by_item')
async def search_by_item(data:SearchByItem):

    select = "a.receipt_no,c.trn_date,a.item_id,b.item_name,a.qty,a.price,c.pay_mode"
    table_name = "td_item_sale a, md_items b, td_receipt c"
    where = f"a.receipt_no=c.receipt_no AND a.item_id=b.id AND a.comp_id=b.comp_id AND a.comp_id = {data.comp_id} AND b.id = {data.item_id} AND a.trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt
