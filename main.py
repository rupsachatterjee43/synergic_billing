from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserLogin,Receipt,CreatePIN
from datetime import datetime
from utils import get_hashed_password, verify_password

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=3003, reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return "Welcome to the billing app"

# user registration
# @app.post('/api/register')
# def register(data:UserRegistration):
#     current_datetime = datetime.now()
#     formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     print(formatted_datetime)
#     password=data.password
#     haspass=get_hashed_password(password)
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"INSERT INTO md_user (comp_id, br_id, user_name, user_id, phone_no, email_id, device_id, password, created_by, created_dt) VALUES('{data.comp_id}','{data.br_id}','{data.user_name}','{data.phone_no}','{data.phone_no}','{data.email_id}', '{data.device_id}', '{haspass}', '{data.user_name}', '{formatted_datetime}')"
#     cursor.execute(query)
#     conn.commit()
#     conn.close()
#     cursor.close()
#     print(cursor.rowcount)
#     if cursor.rowcount==1:
#         return "registered successfully"
#     else:
#         return "invalid date!"


# Verify Phone no and active status
@app.post('/api/verify_phone/{phone_no}')
def verify(phone_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*)phone_no FROM md_user WHERE user_id=phone_no AND phone_no={phone_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    # return result
    if records==[(0,)]:
       resData= {"status":0, "data":"invalid phone"}
    else:
        resData= {
        "status":1,
        "data":"valid phone no."
        }
    return resData
     
   
@app.post('/api/verify_active/{phone_no}')
def verify(phone_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*)active_flag FROM md_user WHERE active_flag='N' AND user_id={phone_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    # result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[(0,)]:
        resData= {"status":-1, "data":"Already registered or invalid phone"}
    else:
        resData= {
        "status":1,
        "data":"registered successfully"
        }
    return resData 

# Create PIN
@app.post('/api/create_pin')
def register(data:CreatePIN):
    password=data.PIN
    haspass=get_hashed_password(password)
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_user SET password='{haspass}', active_flag='Y' where user_id='{data.phone_no}'"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount==1:
        resData= {"status":1, "data":"Pin inserted"}
    else:
        resData= {
        "status":0,
        "data":"invalid phone"
        }
    return resData 

@app.post('/api/otp/{phone_no}') 
def OTP(phone_no:int):
    return {"status":1, "data":"1234"}

    
@app.post('/api/login')
def login(data_login:UserLogin):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.comp_id, c.company_name, a.br_id, b.branch_name, a.user_id, a.user_name, a.phone_no, a.email_id, a.device_id, a.password, a.created_by, a.created_dt, a.active_flag FROM md_user a, md_branch b, md_company c WHERE a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id"
    cursor.execute(query)
    print(cursor.rowcount)
    records = cursor.fetchone()
    conn.close()
    cursor.close()
    if(records is not None):
        result = createResponse(records, cursor.column_names, 0)
        # print(result)
        res_dt = ''
        if(verify_password(data_login.PIN, result['password'])):
            res_dt = {"suc": 1, "msg": result}
        else:
            res_dt = {"suc": 0, "msg": "Please check your userid or PIN"}
    else:
        res_dt = {"suc": 0, "msg": "No user found"}

    return res_dt

#Select location
@app.get('/api/location')
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

#Select items
@app.get('/api/items/{comp_id}')
async def show_items(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.* FROM md_items a, md_item_rate b WHERE a.id=b.item_id AND a.com_id={comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

#Select items with rate
'''@app.get('/api/item_rate/{item_id}')
async def show_item_rate(item_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.id, a.item_name, c.price, c.discount, c.sale_price, c.hsn_code, c.cgst, c.sgst FROM md_items a, md_company b, md_item_rate c WHERE a.com_id=b.id AND a.id=c.item_id AND a.id={item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result'''

# Item Sale
@app.post('/api/saleinsert')
def register(rcpt:Receipt):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_datetime)
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, tnx_date, price, discount_amt, cgst_amt, sgst_amt, created_by, created_dt) VALUES('{rcpt.receipt_no}','{rcpt.br_id}','{rcpt.user_name}','{rcpt.phone_no}','{rcpt.phone_no}','{rcpt.email_id}', '{rcpt.device_id}', '{rcpt.user_name}', '{formatted_datetime}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount==1:
        return "registered successfully"
    else:
        return "invalid date!"