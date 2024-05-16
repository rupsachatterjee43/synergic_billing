from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import CustInfo

# testing git
masterRouter = APIRouter()

#Select location
#-------------------------------------------------------------------------------------------------------------
@masterRouter.get('/location')
async def show_location():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT sl_no, location_name FROM md_location"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

# App version checking
#-------------------------------------------------------------------------------------------------------------
@masterRouter.get('/app_version')
async def app_version():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT sl_no, version_no, url FROM md_version"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":result
        }
    else:
        resData= {"status":0, "data":"no data"}
    return resData
#======================================================================================================
# Customer Information 

@masterRouter.post('/cust_info')
async def cust_info(info:CustInfo):

    conn = connect()
    cursor = conn.cursor()

    query=f"select cust_name from md_customer where comp_id={info.comp_id} and phone_no='{info.phone_no}'"
    # print(query)

    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData= {"status":1, "data":result}
    else:
        resData= {
        "status":0,
        # "data":result[0]
        "data":[]
        }
    return resData
