from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserLogin,Receipt,CreatePIN
from datetime import datetime, date
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
    query = f"SELECT a.*, b.*, c.* FROM md_user a, md_branch b, md_company c WHERE a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id AND a.active_flag='Y'"
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

# Receipt settings
@app.get('/api/receipt_settings/{comp_id}')
async def show_items(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.* FROM md_receipt_settings a, md_header_footer b WHERE a.comp_id=b.comp_id AND a.comp_id={comp_id}"
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

# Generate receipt no.


# Item Sale
@app.post('/api/saleinsert')
def register(rcpt:list[Receipt]):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # print(receipt)
    # print(rcpt)
    # conn = connect()
    # tprice = 0
    # tdiscount_amt = 0
    # tcgst_amt = 0
    # tsgst_amt = 0
    values = []
    for i in rcpt:
        # tprice += i.price
        # tdiscount_amt += i.discount_amt
        # tcgst_amt += i.cgst_amt
        # tsgst_amt += i.sgst_amt
        conn = connect()
        cursor = conn.cursor()
        # print(i)
        values.append((receipt, i.comp_id, i.br_id, i.item_id, formatted_datetime, i.price, i.discount_amt, i.cgst_amt, i.sgst_amt, i.qty))

        query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, trn_date, price, discount_amt, cgst_amt, sgst_amt, qty, created_by, created_dt) VALUES ('{receipt}',{i.comp_id},{i.br_id},{i.item_id},'{formatted_datetime}',{i.price},{i.discount_amt}, {i.cgst_amt}, {i.sgst_amt}, {i.qty}, '{i.created_by}', '{formatted_datetime}')"
        # print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        # print(cursor.rowcount)
        if cursor.rowcount==1:
            resData = {"status":1, "data":receipt}
        else:
            resData = {"status":0, "data":'Data not inserted'}
    # round_off = round(rcpt[0].amount)
    conn = connect()
    cursor = conn.cursor()
    # print(rcpt[0].pay_dtls)
    query = f"INSERT INTO td_receipt (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt) VALUES ('{receipt}','{formatted_datetime}',{rcpt[0].tprice},{rcpt[0].tdiscount_amt},{rcpt[0].tcgst_amt},{rcpt[0].tsgst_amt},{rcpt[0].amount},{rcpt[0].round_off},{rcpt[0].net_amt},'{rcpt[0].pay_mode}','{rcpt[0].received_amt}','{rcpt[0].pay_dtls}','{rcpt[0].cust_name}','{rcpt[0].phone_no}','{rcpt[0].created_by}','{formatted_datetime}')"
    # print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount==1:
        ResData = {"status":1, "data":resData}
    else:
        ResData = {"status":0, "data":"Data not inserted"}
    print(values) 
    return ResData

# Dashboard
@app.get('/api/billsummary/{trn_date}')
async def Bill_sum(trn_date:date):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(receipt_no)Total_Bills, SUM(net_amt)Amount_collected FROM td_receipt WHERE trn_date='{trn_date}'"
    cursor.execute(query)
    records = cursor.fetchall()
    # print(records)
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[(0,None)]:
        resData= {"status":0, "data":"no data"}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Dashboard - Last 4 bills
@app.get('/api/recent_bills')
async def Bill_sum():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM td_receipt ORDER BY created_dt DESC LIMIT 4"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result
    
# insert receipt details
# @app.post('/api/receipt_insert/{rcp_no}')
# def register(rcp:FinalRcp,rcp_no:int):
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"INSERT INTO td_receipt (receipt_no, trn_date,, price, discount_amt, cgst_amt, sgst_amt) VALUES('{rcp_no}')"
#     cursor.execute(query)
#     conn.commit()
#     conn.close()
#     cursor.close()
#     if cursor.rowcount==1:
#         resData = {"status":1, "data":""}
#     else:
#         resData = {"status":0, "data":'Data not inserted'}

#     return resData


# 1005874526987

    # conn = connect()
    # cursor = conn.cursor()
    # query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, trn_date, price, discount_amt, cgst_amt, sgst_amt, created_by, created_dt) VALUES('{rcpt.receipt_no}','{rcpt.br_id}','{rcpt.user_name}','{rcpt.phone_no}','{rcpt.phone_no}','{rcpt.email_id}', '{rcpt.device_id}', '{rcpt.user_name}', '{formatted_datetime}')"
    # cursor.execute(query)
    # conn.commit()
    # conn.close()
    # cursor.close()
    # print(cursor.rowcount)
    # if cursor.rowcount==1:
    #     return "registered successfully"
    # else:
    #     return "invalid date!"