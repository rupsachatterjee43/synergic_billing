from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import Stock,AddStock
from datetime import datetime

stockRouter = APIRouter()

# ==================================================================================================
# Stock List

@stockRouter.post('/stock_list')
async def stock_list(data:Stock):
    select = "a.id, a.item_name, a.comp_id, IF(b.stock > 0, b.stock, 0) stock,b.br_id,c.branch_name"
    table_name = "md_items a LEFT JOIN td_stock b on a.id=b.item_id AND a.comp_id=b.comp_id LEFT JOIN md_branch c on b.br_id=c.id"
    where = f"a.comp_id = {data.comp_id} {f'AND a.id = {data.item_id}' if data.item_id > 0 else f''}"
    # order = 'GROUP BY a.id'
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Update Stock

@stockRouter.post('/add_edit_stock')
async def add_edit_stock(data:AddStock):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "td_stock"
    fields = f"stock = (stock+{data.stock_add})-{data.stock_less}, modified_by = 'admin', modified_dt = '{formatted_dt}'"
    values = None
    where = f"comp_id = {data.comp_id} AND br_id = {data.br_id} AND item_id = {data.item_id}"
    flag = 1 
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt