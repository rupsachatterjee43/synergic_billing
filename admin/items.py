from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,ItemId,AddEditItem
from datetime import datetime


itemRouter = APIRouter()

# ==================================================================================================
# Item List

@itemRouter.post('/item_list')
async def item_list(data:CompId):
    select = "*"
    table_name = "md_items"
    where = f"comp_id = {data.comp_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# All details of an Item

@itemRouter.post('/item_details')
async def item_details(data:ItemId):
    select = "a.id,a.comp_id,a.hsn_code,a.item_name, a.unit_id,b.price,b.discount,b.cgst,b.sgst"
    table_name = "md_items a , md_item_rate b"
    where = f"a.id = b.item_id AND a.id = {data.item_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Add and Edit Item Details

@itemRouter.post('/add_edit_items')
async def add_edit_items(data:AddEditItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if ({data.item_id}.pop())>0:

        table_name = "md_items"
        fields = f"item_name ='{data.item_name}', unit_id = {data.unit_id}, modified_by = 'admin', modified_dt = '{formatted_dt}'"
        values = None
        where = f"id = {data.item_id} and comp_id = {data.comp_id}"
        flag = 1
        res_dt = await db_Insert(table_name,fields,values,where,flag)
        if res_dt["suc"] > 0:
            table_name1 = "md_item_rate"
            fields1 = f"price = {data.price},discount = {data.discount},cgst = {data.cgst},sgst = {data.sgst}, modified_by = 'admin', modified_dt = '{formatted_dt}'"
            values1 = None
            where1 = f"item_id = {data.item_id}"
            flag1 = 1
            res_dt1 = await db_Insert(table_name1,fields1,values1,where1,flag1)

    else:

        table_name = "md_items"
        fields = "comp_id,hsn_code,item_name, unit_id,created_by,created_dt"
        values =f"{data.comp_id},{data.hsn_code},'{data.item_name}', {data.unit_id},'admin','{formatted_dt}'"
        where = None
        print(data.unit_id)
        order = f""
        flag = 0
        res_dt = await db_Insert(table_name,fields,values,where,flag)
        if res_dt["suc"] > 0:
            table_name1 = "md_item_rate"
            fields1 = "item_id,price,discount,cgst,sgst,created_by,created_dt"
            values1 = f"{res_dt['lastId']},{data.price},{data.discount},{data.cgst},{data.sgst},'admin','{formatted_dt}'"
            where1 = None
            flag1 = 0
            res_dt1= await db_Insert(table_name1,fields1,values1,where1,flag1)
    
    return res_dt1