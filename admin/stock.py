from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import Stock,Fetch,AddStock,StockIn,StockOut
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

# ==========================================================================================================
# Fetch Stock

@stockRouter.post('/fetch_stock')
async def fetch_stock(data:Fetch):
    select = "stock"
    table_name = "td_stock"
    where = f"comp_id = {data.comp_id} and br_id = {data.br_id} and item_id = {data.item_id}"
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

# ======================================================================================================
# Stock In

@stockRouter.post('/stock_in')
async def add_edit_stock(data:StockIn):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "td_stock_in"
    fields = "comp_id,br_id,in_date,item_id,in_price,in_cgst,in_sgst,qty,created_by,created_at"
    values = f"{data.comp_id},{data.br_id},date('{formatted_dt}'),{data.item_id},{data.in_price},{data.in_cgst},{data.in_sgst},{data.qty},'{data.created_by}','{formatted_dt}'"
    where = None
    flag = 0 
    res_dt = await db_Insert(table_name,fields,values,where,flag)

    if res_dt["suc"]>0:
    
        table_name = "td_stock"
        fields = f"stock = (stock+{data.qty}), modified_by = '{data.created_by}', modified_dt = '{formatted_dt}'"
        values = None
        where = f"comp_id = {data.comp_id} AND br_id = {data.br_id} AND item_id = {data.item_id}" if data.br_id>0 else f"comp_id = {data.comp_id} AND item_id = {data.item_id}"
        flag = 1 
        res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt

# ===========================================================================================================
# Stock Out -> Return/Damage

@stockRouter.post('/stock_out')
async def stock_out(data:StockOut):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    select = "a.price,a.cgst,a.sgst,b.stock"
    table_name = "md_item_rate a, td_stock b"
    where = f"a.item_id=b.item_id and a.item_id={data.item_id} and b.comp_id = {data.comp_id} and b.br_id = {data.br_id}"
    # order = 'GROUP BY a.id'
    order = f""
    flag = 1
    res_dt= await db_select(select,table_name,where,order,flag)
    res_dt2={
        "suc":0,
        "msg":[]
    }

    if res_dt["suc"]>0:
        try:

            if res_dt["msg"][0]["stock"]>=data.qty:

                table_name = "td_return"
                fields = "comp_id,br_id,trn_date,item_id,qty,price,cgst_prtg,cgst_amt,sgst_prtg,sgst_amt,damage_flag,remarks,created_by,created_dt"
                values = f"{data.comp_id},{data.br_id},date('{formatted_dt}'),{data.item_id},{data.qty},{res_dt['msg'][0]['price']},{res_dt['msg'][0]['cgst']},{res_dt['msg'][0]['price']*(res_dt['msg'][0]['cgst']/100)},{res_dt['msg'][0]['sgst']},{res_dt['msg'][0]['price']*(res_dt['msg'][0]['sgst']/100)},'{data.damage_flag}','{data.remarks}','{data.created_by}','{formatted_dt}'"
                where = None
                flag = 0 
                res_dt1 = await db_Insert(table_name,fields,values,where,flag)

                if res_dt1["suc"] > 0:

                    try:

                        table_name = "td_stock"
                        fields = f"stock = (stock-{data.qty}), modified_by = '{data.created_by}', modified_dt = '{formatted_dt}'"
                        values = None
                        where = f"comp_id = {data.comp_id} AND br_id = {data.br_id} AND item_id = {data.item_id}" if data.br_id>0 else f"comp_id = {data.comp_id} AND item_id = {data.item_id}"
                        flag = 1 
                        res_dt2 = await db_Insert(table_name,fields,values,where,flag)
                    except:
                        print("<<<<<<<<<<<<>>>>>>>>>>>>>>>")

        except:
            print("++++++++++++++++++")
        return res_dt2