from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import InventorySearch,UpdateStock,StockReport

from datetime import datetime

# testing git
stockRouter = APIRouter()

# Inventory Searching
#---------------------------------------------------------------------------------------------------------------------------
@stockRouter.post('/stock')
async def stock(st_list:InventorySearch):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT stock FROM td_stock WHERE comp_id = {st_list.comp_id} AND br_id = {st_list.br_id} AND item_id = {st_list.item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result[0]

# Stock update
#---------------------------------------------------------------------------------------------------------------------------
@stockRouter.post('/update_stock')
async def update_stock(update:UpdateStock):
    try:
        current_datetime = datetime.now()
        formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        conn = connect()
        cursor = conn.cursor()
        query = f"UPDATE td_stock SET stock=(stock+{update.added_stock})-{update.removed_stock}, modified_by='{update.user_id}', modified_dt='{formatted_dt}' WHERE comp_id={update.comp_id} AND br_id={update.br_id} AND item_id={update.item_id}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.rowcount>0:
            resData= {  
            "status":1,
            "data":"Stock updated Successfully"
            }
        else:
            resData= {
            "status":0, 
            "data":"Error while updating Stock"
            }
    except:
        print("An exception occurred")
    finally:
        return resData

# Stock Report
#---------------------------------------------------------------------------------------------------------------------------
@stockRouter.post('/stock_report')
async def stock_report(stk_rep:StockReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.item_id, b.item_name, c.unit_name, a.stock, a.created_by, a.created_dt, a.modified_by, a.modified_dt FROM td_stock a JOIN md_items b ON  a.item_id=b.id AND a.comp_id=b.comp_id LEFT JOIN md_unit c on c.sl_no=b.unit_id WHERE a.comp_id={stk_rep.comp_id} AND a.br_id={stk_rep.br_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records,cursor.column_names,1)
    conn.close()
    cursor.close()
    return result