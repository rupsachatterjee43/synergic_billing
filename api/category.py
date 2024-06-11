from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import SearchByCategory, EditCategory, AddCategory
from datetime import datetime

from urllib.parse import quote

# testing git
categoryRouter = APIRouter()

@categoryRouter.get('/category_list/{comp_id}')
async def category_list(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT sl_no, category_name, catg_picture FROM md_category WHERE comp_id={comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        res_dt={"status":1, "msg":result}
    else:
        res_dt={"status":0, "msg":[]}
    return res_dt

#==========================================================================================================
# Search Items by Category:

@categoryRouter.post('/categorywise_item_list')
async def categorywise_item_list(catg:SearchByCategory):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.*, c.unit_name, d.stock FROM md_items a JOIN md_item_rate b on a.id=b.item_id LEFT JOIN md_unit c on c.sl_no=a.unit_id LEFT JOIN td_stock d on d.comp_id=a.comp_id and d.item_id=a.id WHERE a.comp_id={catg.comp_id} AND a.catg_id={catg.catg_id} AND d.br_id={catg.br_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        res_dt={"status":1, "msg":result}
    else:
        res_dt={"status":0, "msg":[]}
    return res_dt


@categoryRouter.post('/edit_category')
async def edit_category(edit:EditCategory):
    try:
        current_datetime = datetime.now()
        formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        conn = connect()
        cursor = conn.cursor()
        query = f"UPDATE md_category SET category_name='{edit.category_name}', modified_by='{edit.modified_by}', modified_at='{formatted_dt}' WHERE sl_no={edit.sl_no} and comp_id={edit.comp_id}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.rowcount>0:
            resData= {  
            "status":1,
            "data":"Category Edited Successfully"
            }
        else:
            resData= {
            "status":0, 
            "data":"Error while updating Category."
            }
    except:
        print("An exception occurred")
    finally:
        return resData
    

@categoryRouter.post('/add_category')
async def add_category(add_cat:AddCategory):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO md_category(comp_id, category_name, created_by, created_at) VALUES ({add_cat.comp_id}, '{add_cat.category_name}', '{add_cat.created_by}', '{formatted_dt}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData={
            "status":1,
            "data":"Category Added Successfully"
        }
    else:
        resData={
            "status":0,
            "data":"Category Not Added"
        }
    return resData