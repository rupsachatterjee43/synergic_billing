from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import AddUnit,EditUnit
from datetime import datetime

from urllib.parse import quote

# testing git
unitRouter = APIRouter()

# Add unit
#--------------------------------------------------------------------------------------------------------------------------
@unitRouter.post('/add_unit')
async def add_unit(add_unit:AddUnit):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO md_unit(comp_id, unit_name, created_by, created_at) VALUES ({add_unit.comp_id}, '{add_unit.unit_name}', '{add_unit.created_by}', '{formatted_dt}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData={
            "status":1,
            "data":"Unit Added Successfully"
        }
    else:
        resData={
            "status":0,
            "data":"Unit Not Added"
        }
    return resData

# All Units
#---------------------------------------------------------------------------------------------------------------------------
@unitRouter.get('/units/{comp_id}')
async def unit_list(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM md_unit WHERE comp_id = {comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

# Edit Units
#---------------------------------------------------------------------------------------------------------------------------
@unitRouter.post('/edit_unit')
async def edit_unit(edit:EditUnit):
    try:
        current_datetime = datetime.now()
        formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        conn = connect()
        cursor = conn.cursor()
        query = f"UPDATE md_unit SET unit_name='{edit.unit_name}', modified_by='{edit.modified_by}', modified_at='{formatted_dt}' WHERE sl_no={edit.sl_no} and comp_id={edit.comp_id}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.rowcount>0:
            resData= {  
            "status":1,
            "data":"Unit Edited Successfully"
            }
        else:
            resData= {
            "status":0, 
            "data":"Error while updating Unit."
            }
    except:
        print("An exception occurred")
    finally:
        return resData
    