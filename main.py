from fastapi import FastAPI, requests, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserLogin,Receipt,CreatePIN,DashBoard,SearchBill,SaleReport,ItemReport,EditHeaderFooter,EditItem,DiscountSettings,GSTSettings,GeneralSettings,AddItem,AddUnit,EditUnit,InventorySearch,UpdateStock,StockReport,RefundItem,RefundList,RefundBillReport,CustInfo,BillList,SearchByItem
# from models.otp_model import generateOTP
from datetime import datetime, date
from utils import get_hashed_password, verify_password

import requests, random
from urllib.parse import quote
import json

# testing git
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=3005, reload=True)

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

# @app.get('/api/otp')
# async def otp():
#     result = generateOTP
#     return result

# Verify Phone no and active status
#------------------------------------------------------------------------------------------------------
@app.post('/api/verify_phone/{phone_no}')
async def verify(phone_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*)phone_no FROM md_user WHERE user_id=phone_no AND user_type in ('U','M') AND phone_no={phone_no}"
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
async def verify(phone_no:int):
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
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/create_pin')
async def register(data:CreatePIN):
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

# Generate OTP
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/otp/{phone_no}') 
async def OTP(phone_no:int):
    return {"status":1, "data":"1234"}

# USER LOGIN
#-----------------------------------------------------------------------------------------------------------  
@app.post('/api/login')
async def login(data_login:UserLogin):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.*, c.* FROM md_user a, md_branch b, md_company c WHERE a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id AND a.active_flag='Y' AND a.user_type in ('U','M')"
    cursor.execute(query)
    print(cursor.rowcount)
    records = cursor.fetchone()
    result = createResponse(records, cursor.column_names, 0)
    conn.close()
    cursor.close()

    if(records is not None):
        # result = createResponse(records, cursor.column_names, 0)

        # conn = connect()
        # cursor = conn.cursor()
        # query = f"SELECT otp_template FROM md_sms WHERE comp_id = {result['comp_id']}"
        # cursor.execute(query)
        # # print(cursor.rowcount)
        # records = cursor.fetchone()
        # conn.close()
        # cursor.close()
        # sms_res = createResponse(records, cursor.column_names, 0)
        
        # res_dt = ''
        # # if(verify_password(data_login.PIN, result['password'])):
        # otp = sms(data_login.user_id, sms_res['otp_template'])
        # res_dt = {"suc": 1, "msg": result, "otp": otp}
        # res_dt = {"suc": 1, "msg": result, "otp": {"msg": "OK [d2863a61-f0bd-11ee-b125-14187734a8d9]", "otp": 1234}, "SMS": sms_res}
        # # else:
        # #     res_dt = {"suc": 0, "msg": "Please check your userid or PIN", "otp": {}}

        res_dt = {"suc": 1, "msg": result}
    else:
        res_dt = {"suc": 0, "msg": "No user found"}

    return res_dt

#Select location
#-------------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------------
@app.get('/api/items/{comp_id}')
async def show_items(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.*, c.unit_name FROM md_items a JOIN md_item_rate b on a.id=b.item_id LEFT JOIN md_unit c on c.sl_no=a.unit_id WHERE a.comp_id={comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

# Receipt settings
#-------------------------------------------------------------------------------------------------------------
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
    query = f"SELECT a.id, a.item_name, c.price, c.discount, c.sale_price, c.hsn_code, c.cgst, c.sgst FROM md_items a, md_company b, md_item_rate c WHERE a.comp_id=b.id AND a.id=c.item_id AND a.id={item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result'''

# Generate receipt no.


# Item Sale
#---------------------------------------------------------------------------------------------------------------------------
@app.post('/api/saleinsert')
async def register(rcpt:list[Receipt]):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    values = []
    tcgst_amt = 0
    tsgst_amt = 0
    for i in rcpt:
        tcgst_amt += i.cgst_amt
        tsgst_amt += i.sgst_amt
        conn = connect()
        cursor = conn.cursor()
        # print(i)
        values.append((receipt, i.comp_id, i.br_id, i.item_id, formatted_datetime, i.price, i.discount_amt, i.cgst_amt, i.sgst_amt, i.qty))

        query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, trn_date, price, dis_pertg, discount_amt, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, created_by, created_dt) VALUES ('{receipt}',{i.comp_id},{i.br_id},{i.item_id},'{formatted_datetime}',{i.price},{i.dis_pertg},{i.discount_amt}, {i.cgst_prtg}, {i.cgst_amt}, {i.sgst_prtg}, {i.sgst_amt}, {i.qty}, '{i.created_by}', '{formatted_datetime}')"

        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        if cursor.rowcount>0:
            if i.stock_flag=='Y':
                conn = connect()
                cursor = conn.cursor()

                query = f"UPDATE td_stock SET stock=stock-{i.qty}, modified_by='{i.created_by}', modified_dt='{formatted_datetime}' WHERE comp_id={i.comp_id} AND br_id={i.br_id} AND item_id={i.item_id}"

                cursor.execute(query)
                conn.commit()
                conn.close()
                cursor.close()
                if cursor.rowcount==1:
                    resData = {"status":1, "data":receipt}
                else:
                    resData = {"status":0, "data":'error while updating stock'}
            else:
                resData = {"status":1, "data":receipt}
        else:
            resData = {"status":-1, "data":"Data not inserted in item_sale"}
    
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO td_receipt (receipt_no, comp_id, br_id, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, gst_type, discount_flag, discount_type, discount_position, created_by, created_dt) VALUES ('{receipt}', {rcpt[0].comp_id}, {rcpt[0].br_id},'{formatted_datetime}',{rcpt[0].tprice},{rcpt[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{rcpt[0].amount},{rcpt[0].round_off},{rcpt[0].net_amt},'{rcpt[0].pay_mode}','{rcpt[0].received_amt}','{rcpt[0].pay_dtls}','{rcpt[0].cust_name}','{rcpt[0].phone_no}','{rcpt[0].gst_flag}', '{rcpt[0].gst_type}','{rcpt[0].discount_flag}','{rcpt[0].discount_type}','{rcpt[0].discount_position}','{rcpt[0].created_by}','{formatted_datetime}')"
    # print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount==1:
        # if rcpt[0].rcpt_type != 'P':

        #     conn = connect()
        #     cursor = conn.cursor()
        #     query = f"SELECT bill_template FROM md_sms WHERE comp_id = {rcpt[0].comp_id}"
        #     cursor.execute(query)
        #     # print(cursor.rowcount)
        #     records = cursor.fetchone()
        #     conn.close()
        #     cursor.close()
        #     sms_res = createResponse(records, cursor.column_names, 0)

        #     print_url = f'https://billing.opentech4u.co.in/bill/receipt?receipt_no={receipt}'
        #     shortUrl = short_url(print_url)
        #     if(shortUrl['msg'] != ''):
        #         send_bill_sms(shortUrl["msg"], rcpt[0].phone_no, sms_res['bill_template'])

        ResData = {"status":1, "data":resData}
    else:
        ResData = {"status":0, "data":"Data not inserted"}

    if rcpt[0].cust_info_flag > 0:
        conn = connect()
        cursor = conn.cursor()
        query= f"update md_customer set cust_name = '{rcpt[0].cust_name}', pay_mode = '{rcpt[0].pay_mode}', modified_by = '{rcpt[0].created_by}', modified_dt = '{formatted_datetime}' where phone_no = '{rcpt[0].phone_no}'"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        # cust = {"msg":"existing customer"}

    else:
        conn = connect()
        cursor = conn.cursor()
        query= f"insert into md_customer (comp_id,cust_name,phone_no,pay_mode,created_by,created_dt) values ({rcpt[0].comp_id},'{rcpt[0].cust_name}','{rcpt[0].phone_no}','{rcpt[0].pay_mode}','{rcpt[0].created_by}','{formatted_datetime}')"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        # cust = {"msg":"new customer"}

    print(values) 
    return ResData
    # print(rcpt[0][-1])

# Dashboard
#-------------------------------------------------------------------------------------------------------------------------
@app.post('/api/billsummary')
async def Bill_sum(bill_sum:DashBoard):
    conn = connect()
    cursor = conn.cursor()

    query = f"SELECT COUNT(a.receipt_no)total_bills, SUM(a.net_amt)amount_collected FROM td_receipt a, md_user b,md_branch c,md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={bill_sum.comp_id} and c.id={bill_sum.br_id} and a.trn_date='{bill_sum.trn_date}' and a.created_by='{bill_sum.user_id}'"

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
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/recent_bills')
async def recent_bill(rec_bill:DashBoard):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.* FROM td_receipt a, md_user b, md_branch c, md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={rec_bill.comp_id} and c.id={rec_bill.br_id} and a.trn_date='{rec_bill.trn_date}' and a.created_by='{rec_bill.user_id}' ORDER BY created_dt DESC LIMIT 10"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

#Select Bill
#------------------------------------------------------------------------------------------------------------
@app.get('/api/show_bill/{recp_no}')
async def show_bill(recp_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.gst_flag, b.gst_type, b.discount_flag, b.discount_type, b.discount_position, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name FROM td_item_sale a, td_receipt b, md_items c WHERE a.receipt_no=b.receipt_no and a.trn_date=b.trn_date and a.item_id=c.id and a.receipt_no={recp_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData= {"status":1, 
                  "data":result}
    else:
        resData= {
        "status":0,
        "data":[]
        }
    return resData


#Search bills within a date range
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/search_bills')
async def search_bills(search:SearchBill):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.* FROM td_receipt a, md_user b, md_branch c, md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={search.comp_id} and c.id={search.br_id} and a.created_by='{search.user_id}' and a.trn_date BETWEEN '{search.from_date}' AND '{search.to_date}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Sale Report
#---------------------------------------------------------------------------------------------------------------------------
@app.post('/api/sale_report')
async def sale_report(sl_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    # query = f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, sum(a.price)price, sum(a.discount_amt)discount_amt, sum(a.cgst_amt)cgst_amt, sum(a.sgst_amt)sgst_amt, sum(a.round_off)rount_off, sum(a.amount)net_amt, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date, a.created_by"
    query=f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} and a.created_by='{sl_rep.user_id}' group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date, a.created_by"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Collection Report
#---------------------------------------------------------------------------------------------------------------------------
@app.post('/api/collection_report')
async def collection_report(col_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"Select created_by, pay_mode, sum(net_amt)net_amt, user_name, count(receipt_no)no_of_bills from ( select Distinct a.created_by created_by, a.pay_mode pay_mode, a.net_amt net_amt, c.user_name user_name, a.receipt_no receipt_no from td_receipt a, td_item_sale b, md_user c where a.created_by=c.user_id and a.receipt_no = b.receipt_no and a.trn_date BETWEEN '{col_rep.from_date}' and '{col_rep.to_date}' and b.comp_id= {col_rep.comp_id} AND b.br_id = {col_rep.br_id} AND a.created_by='{col_rep.user_id}')a group by created_by, pay_mode"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Item Report
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/item_report')
async def item_report(item_rep:ItemReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select a.receipt_no,a.trn_date,a.qty,a.price,a.discount_amt,a.cgst_amt,a.sgst_amt,b.amount,b.pay_mode,c.item_name,d.branch_name from   td_item_sale a, td_receipt b, md_items c, md_branch d where  a.receipt_no = b.receipt_no AND a.comp_id = c.comp_id AND a.comp_id = d.comp_id AND a.br_id = d.id AND a.item_id = c.id And a.trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' And a.comp_id = {item_rep.comp_id} AND a.br_id = {item_rep.br_id} AND a.item_id = {item_rep.item_id} and b.created_by='{item_rep.user_id}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# GST Statement
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/gst_statement')
async def gst_statement(gst_st:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select distinct a.receipt_no, a.trn_date, (a.price - a.discount_amt)taxable_amt, a.cgst_amt, a.sgst_amt, (a.cgst_amt + a.sgst_amt)total_tax, a.net_amt from td_receipt a, td_item_sale b where a.receipt_no = b.receipt_no and b.comp_id = {gst_st.comp_id} and b.br_id = {gst_st.br_id} and a.created_by = {gst_st.user_id} and (a.cgst_amt + a.sgst_amt) > '0' and a.trn_date BETWEEN '{gst_st.from_date}' and '{gst_st.to_date}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# GST  Summary
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/gst_summary')
async def gst_summary(gst_sm:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT cgst_prtg, SUM(cgst_amt)cgst_amt, SUM(sgst_amt)sgst_amt, SUM(cgst_amt) + SUM(sgst_amt)total_tax FROM td_item_sale WHERE comp_id = {gst_sm.comp_id} AND br_id = {gst_sm.br_id} AND created_by = {gst_sm.user_id} AND trn_date BETWEEN '{gst_sm.from_date}' AND '{gst_sm.to_date}' GROUP BY cgst_prtg"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Edit header-footer option for 'M' user type
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/edit_header_footer')
async def edit_header_footer(edit:EditHeaderFooter):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_header_footer SET header1 = '{edit.header1}', on_off_flag1 = '{edit.on_off_flag1}', header2 = '{edit.header2}', on_off_flag2 = '{edit.on_off_flag2}', footer1 = '{edit.footer1}', on_off_flag3 = '{edit.on_off_flag3}', footer2 = '{edit.footer2}', on_off_flag4 = '{edit.on_off_flag4}', created_by = '{edit.created_by}', created_at = '{formatted_datetime}' WHERE comp_id = {edit.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    # print(query)
    if cursor.rowcount>0:
        resData= {
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# Edit item_rate
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/edit_item')
async def edit_items(edit_item:EditItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_item_rate JOIN md_items ON md_items.id=md_item_rate.item_id SET md_items.item_name = '{edit_item.item_name}', md_item_rate.price = {edit_item.price}, md_item_rate.discount = {edit_item.discount}, md_item_rate.cgst = {edit_item.cgst}, md_item_rate.sgst = {edit_item.sgst}, md_item_rate.modified_by = '{edit_item.modified_by}', md_item_rate.modified_dt = '{formatted_dt}', md_items.modified_by = '{edit_item.modified_by}', md_items.modified_dt = '{formatted_dt}' WHERE md_item_rate.item_id={edit_item.item_id} AND md_items.comp_id={edit_item.comp_id} AND md_items.unit_id={edit_item.unit_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    # print(query)
    if cursor.rowcount>0:
        resData= {
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# Add items
#---------------------------------------------------------------------------------------------------------------------------
@app.post('/api/add_item')
async def add_items(add_item:AddItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO md_items(comp_id, hsn_code, item_name, unit_id, created_by, created_dt) VALUES ({add_item.comp_id}, '{add_item.hsn_code}', '{add_item.item_name}', {add_item.unit_id}, '{add_item.created_by}', '{formatted_dt}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    # print(query)
    if cursor.rowcount>0:
        conn1 = connect()
        cursor1 = conn1.cursor()
        query1 = f"INSERT INTO md_item_rate (item_id, price, discount, cgst, sgst, created_by, created_dt) VALUES ({cursor.lastrowid}, {add_item.price}, {add_item.discount}, {add_item.cgst}, {add_item.sgst}, '{add_item.created_by}', '{formatted_dt}')"
        cursor1.execute(query1)
        conn1.commit()
        conn1.close()
        cursor1.close()
        if cursor1.rowcount>0:
            conn2 = connect()
            cursor2 = conn2.cursor()
            query2 = f"INSERT INTO td_stock (comp_id, br_id, item_id, stock, created_by, created_dt) VALUES ({add_item.comp_id}, {add_item.br_id}, {cursor.lastrowid}, '0', '{add_item.created_by}', '{formatted_dt}')"
            cursor2.execute(query2)
            conn2.commit()
            conn2.close()
            cursor2.close()
            if cursor2.rowcount>0:
                resData={"status":1, "data": "Item and Stock Added Successfully"}
            else:
                resData={"status":0, "data": "No Stock Added"}
        else:
            resData= {"status":0, "data":"Item Rate not Added"}
    else:
        resData={"status":-1, "data":"No Data Added"}
       
    return resData

# Edit Settings
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/edit_discount_settings')
async def edit_discount_settings(rcp_set:DiscountSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET discount_flag='{rcp_set.discount_flag}', discount_type='{rcp_set.discount_type}', discount_position='{rcp_set.discount_position}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# GST Settings
#-----------------------------

@app.post('/api/edit_gst_settings')
async def edit_gst_settings(rcp_set:GSTSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET gst_flag='{rcp_set.gst_flag}', gst_type='{rcp_set.gst_type}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# General Settings
#-----------------------------

@app.post('/api/edit_general_settings')
async def edit_general_settings(rcp_set:GeneralSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET rcpt_type='{rcp_set.rcpt_type}', unit_flag='{rcp_set.unit_flag}', cust_inf='{rcp_set.cust_inf}', pay_mode='{rcp_set.pay_mode}', stock_flag='{rcp_set.stock_flag}', price_type='{rcp_set.price_type}', refund_days={rcp_set.refund_days}, modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# App version checking
#-------------------------------------------------------------------------------------------------------------
@app.get('/api/app_version')
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

# Cancel Bill1
# --------------------------------------------------------------------------------------------------------
# @app.post('/api/cancel_bill')
# async def cancel_bill(del_bill:CancelBill):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"INSERT INTO td_receipt_cancel (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancellation_dt) SELECT receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt, modified_by, modified_dt FROM td_receipt WHERE receipt_no='{del_bill.receipt_no}' AND created_by='{del_bill.user_id}'"
#     cursor.execute(query)
#     conn.commit()
#     conn.close()
#     cursor.close()
#     # print(query)
#     print(cursor.rowcount)
#     if cursor.rowcount>0:
#         conn1 = connect()
#         cursor1 = conn1.cursor()
#         query1 = f"DELETE FROM td_receipt WHERE receipt_no='{del_bill.receipt_no}' AND created_by='{del_bill.user_id}'"
#         cursor1.execute(query1)
#         conn1.commit()
#         conn1.close()
#         cursor1.close()
#         if cursor1.rowcount>0:
#             resData= {
#             "status":1,
#             "data":"Bill Cancelled Successfully"
#             } 
#         else:
#             resData= {"status":0, "data":"bill not deleted"}
#     else:
#         resData={"status":-1, "data":"bill not added" }
       
#     return resData

# cancel bill2
#======================
# @app.post('/api/cancel_bill')
# async def cancel_bill(del_bill:CancelBill):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"SELECT * FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
#     cursor.execute(query)
#     records = cursor.fetchone()
#     conn.close()
#     cursor.close()
#     # print (type(records))
#     rec = list(records)
#     rec.append(del_bill.user_id)
#     rec.append(formatted_dt)
#     # return len(rec)
#     # result = createResponse(records, cursor.column_names, 1)
#     # i = result[0]
#     # print(i["created_dt"])

#     if cursor.rowcount>0:   
#         conn1 = connect()
#         cursor1 = conn1.cursor()
#         # query1 = f"INSERT INTO td_receipt_cancel (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) Values ({i["receipt_no"]}, {i["trn_date"]}, {i["price"]}, {i["discount_amt"]}, {i["cgst_amt"]}, {i["sgst_amt"]}, {i["amount"]}, {i["round_off"]}, {i["net_amt"]}, {i["pay_mode"]}, {i["received_amt"]}, {i["pay_dtls"]}, {i["cust_name"]}, {i["phone_no"]}, {i["created_by"]}, {i["created_dt"]}, {i["modified_by"]}, {i["modified_dt"]}, '{del_bill.user_id}', '{formatted_dt}')"
#         query1 = f"INSERT INTO td_receipt_cancel_new (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         cursor1.execute(query1, tuple(rec))
#         conn1.commit()
#         conn1.close()
#         cursor1.close()
#         # return cursor1.rowcount

#         if cursor1.rowcount>0:
#             conn2 = connect()
#             cursor2 = conn2.cursor()
#             query2 = f"UPDATE td_stock JOIN td_item_sale ON td_stock.comp_id=td_item_sale.comp_id AND td_stock.br_id=td_item_sale.br_id JOIN td_receipt ON td_item_sale.receipt_no=td_receipt.receipt_no SET td_stock.stock=td_stock.stock+td_item_sale.qty, td_stock.modified_by='{del_bill.user_id}', td_stock.modified_dt='{formatted_dt}' WHERE td_stock.item_id=td_item_sale.item_id AND td_receipt.receipt_no={del_bill.receipt_no}"
#             # query2 = f"DELETE FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
#             cursor2.execute(query2)
#             conn2.commit()
#             conn2.close()
#             cursor2.close()

#             if cursor2.rowcount>0:
#                 # resData= {
#                 # "status":1,
#                 # "data":"Bill Cancelled Successfully"
#                 # } 
#                 conn3 = connect()
#                 cursor3 = conn3.cursor()
#                 query3 = f"DELETE td_receipt.*, td_item_sale.* FROM td_receipt JOIN td_item_sale ON td_receipt.receipt_no=td_item_sale.receipt_no WHERE td_receipt.receipt_no={del_bill.receipt_no}"
#                 cursor3.execute(query3)
#                 conn3.commit()
#                 conn3.close()
#                 cursor3.close()

#                 if cursor3.rowcount>0:
#                     resData={"status":1, "data":"Bill cancellled and Stock added Successfully"}
#                 else:
#                     resData={"status":0, "data":"Error while deleting receipt from td_receipt"}

#             else:
#                 resData= {"status":-1, "data":"Error while updating stock"}

#         else:
#             resData={"status":-2, "data":"Error while inserting into cancel bill table" }

#     else:
#         resData={"status":-3, "data":"bill not selected properly" }

#     return resData
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#cancel bill3

# @app.post('/api/cancel_bill')
# async def cancel_bill2(del_bill:CancelBill):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     conn = connect()
#     cursor = conn.cursor()

#     query = f"SELECT * FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"

#     cursor.execute(query)
#     records = cursor.fetchone()
#     conn.close()
#     cursor.close()
#     rec = list(records)
#     rec.append(del_bill.user_id)
#     rec.append(formatted_dt)
#     # print(rec)

#     if cursor.rowcount>0:   
#         conn1 = connect()
#         cursor1 = conn1.cursor()
       
#         query1 = f"INSERT INTO td_receipt_cancel_new (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#         cursor1.execute(query1, tuple(rec))
#         # print(tuple(rec))
#         conn1.commit()
#         conn1.close()
#         cursor1.close()
#         # return cursor1.rowcount

#         if cursor1.rowcount>0:
#             current_datetime = datetime.now()
#             formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#             conn2 = connect()
#             cursor2 = conn2.cursor()

#             query2 = f"SELECT * FROM td_item_sale WHERE receipt_no={del_bill.receipt_no} AND created_by={del_bill.user_id}"
            
#             cursor2.execute(query2)
#             records = cursor2.fetchall()
#             result = createResponse(records, cursor2.column_names, 1)
#             conn2.close()
#             cursor2.close()
#             # print(result)
#             print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
#             print(records)
#             # rec1 = list(records[0])
#             # rec1.append(del_bill.user_id)
#             # rec1.append(formatted_dt)
#             # print("_____________________")
#             # print(len(rec1))

#             if cursor2.rowcount>0:

#                 current_datetime = datetime.now()
#                 formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
#                 for i in records:

#                     print("zzzzzzzzzzzzzzzzzzzzzz")
#                     print(i)
#                     rec1 = list(i)
#                     rec1.append(del_bill.user_id)
#                     rec1.append(formatted_dt)
#                     print(rec1)
#                 #     # values.append()
#                 #     conn3 = connect()
#                 #     cursor3 = conn3.cursor()
       
#                 #     query3 = f"INSERT INTO td_item_sale_cancel (receipt_no, comp_id, br_id, item_id, trn_date, price, dis_pertg, discount_amt, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) values ({i.receipt_no}, {i.comp_id}, {i.br_id}, {i.item_id}, '{i.trn_date}', {i.price}, {i.dis_pertg}, {i.discount_amt}, {i.cgst_prtg}, {i.cgst_amt}, {i.sgst_prtg}, {i.sgst_amt}, {i.qty}, '{i.created_by}', '{i.created_dt}', '{i.modified_by}', '{i.modified_dt}', '{del_bill.user_id}', '{formatted_dt}')"

#                 #     cursor3.execute(query3)
#                 #     conn3.commit()
#                 #     conn3.close()
#                 #     cursor3.close()   
#                     conn3 = connect()
#                     cursor3 = conn3.cursor()
#                 # print("=====================================")
#                 # print(tuple(rec1))
       
#                     query3 = f"INSERT INTO td_item_sale_cancel (receipt_no, comp_id, br_id, item_id, trn_date, price, dis_pertg, discount_amt, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#                     cursor3.execute(query3, rec1)
#                     print(query3)
#                     conn3.commit()
#                     conn3.close()
#                     cursor3.close()

#                 if cursor3.rowcount>0:
#                     conn4 = connect()
#                     cursor4 = conn4.cursor()

#                     query4 = f"UPDATE td_stock JOIN td_item_sale ON td_stock.comp_id=td_item_sale.comp_id AND td_stock.br_id=td_item_sale.br_id JOIN td_receipt ON td_item_sale.receipt_no=td_receipt.receipt_no SET td_stock.stock=td_stock.stock+td_item_sale.qty, td_stock.modified_by='{del_bill.user_id}', td_stock.modified_dt='{formatted_dt}' WHERE td_stock.item_id=td_item_sale.item_id AND td_receipt.receipt_no={del_bill.receipt_no}"

#                     cursor4.execute(query4)
#                     conn4.commit()
#                     conn4.close()
#                     cursor4.close()


#                     if cursor4.rowcount>0: 
#                         conn5 = connect()
#                         cursor5 = conn5.cursor()

#                         query5 = f"DELETE td_receipt.*, td_item_sale.* FROM td_receipt JOIN td_item_sale ON td_receipt.receipt_no=td_item_sale.receipt_no WHERE td_receipt.receipt_no={del_bill.receipt_no}"

#                         cursor5.execute(query5)
#                         conn5.commit()
#                         conn5.close()
#                         cursor5.close()

#                         if cursor5.rowcount>0:
#                             resData={"status":1, "data":"Bill cancellled and Stock added Successfully"}
#                         else:
#                             resData={"status":0, "data":"Error while deleting receipt from td_receipt"}

#                     else:
#                         resData= {"status":-1, "data":"Error while updating stock"}

#                 else:
#                     resData={"status":-2, "data":"Error while inserting into cancel item table" }

#             else:
#                 resData={"status":-3, "data":"Error while inserting into cancel bill table" }

#         else:
#             resData={"status":-4, "data":"Error while selecting items" }
    
#     else:
#         resData={"status":-5, "data":"Error while selecting bills" }

#     return resData
#==========================================================================================================================
# @app.post('/api/cancel_bill_two')
# async def cancel_bill_two(del_bill: CancelBill):
#     current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     conn = connect()
#     cursor = conn.cursor()

#     query = f"SELECT * FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"

#     cursor.execute(query)
#     record = cursor.fetchall()
#     conn.close()
#     cursor.close()
#     print(record)

#     if record:
#         rec = list(record)
#         rec.append(del_bill.user_id)
#         rec.append(current_datetime)

#         query1 = """INSERT INTO td_receipt_cancel_new (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

#         cursor.execute(query1, tuple(rec))
#         conn.commit()

#         if cursor.rowcount > 0:
#             query2 = f"SELECT * FROM td_item_sale WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
#             cursor.execute(query2)
#             records = cursor.fetchall()

#             if records:
#                 for rec1 in records:
#                     query3 = """INSERT INTO td_item_sale_cancel (receipt_no, comp_id, br_id, item_id, trn_date, price, dis_pertg, discount_amt, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) 
#                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#                     cursor.execute(query3, rec1)
#                     conn.commit()

#                 query4 = f"""UPDATE td_stock JOIN td_item_sale ON td_stock.comp_id=td_item_sale.comp_id AND td_stock.br_id=td_item_sale.br_id JOIN td_receipt ON td_item_sale.receipt_no=td_receipt.receipt_no 
#                             SET td_stock.stock=td_stock.stock+td_item_sale.qty, td_stock.modified_by='{del_bill.user_id}', td_stock.modified_dt='{current_datetime}' 
#                             WHERE td_stock.item_id=td_item_sale.item_id AND td_receipt.receipt_no={del_bill.receipt_no}"""
#                 cursor.execute(query4)
#                 conn.commit()
#                 resData = {"status": 1, "data": "Bill cancelled and Stock added Successfully"}
#             else:
#                 resData = {"status": -3, "data": "Error while inserting into cancel item table"}
#         else:
#             resData = {"status": -2, "data": "Error while inserting into cancel bill table"}
#     else:
#         resData = {"status": -1, "data": "Error while selecting bills"}

#     cursor.close()
#     conn.close()

#     return resData

# Add unit
#--------------------------------------------------------------------------------------------------------------------------
@app.post('/api/add_unit')
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
@app.get('/api/units/{comp_id}')
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
@app.post('/api/edit_unit')
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
    
# Inventory Searching
#---------------------------------------------------------------------------------------------------------------------------
@app.post('/api/stock')
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
@app.post('/api/update_stock')
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
@app.post('/api/stock_report')
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
# Cancel_Bill Report
#---------------------------------------------------------------------------------------------------------------------------
# @app.post('/api/cancel_bill_report')
# async def cancel_bill_report(can_rep:CancelBillReport):
#     conn = connect()
#     cursor = conn.cursor()
#     # query = f"SELECT a.* FROM td_receipt_cancel_new AS a WHERE trn_date BETWEEN {can_rep.from_date} AND {can_rep.to_date}"
#     query = f"SELECT a.cancel_rcpt_id,a.receipt_no,a.trn_date,a.price,a.discount_amt,a.cgst_amt,a.sgst_amt,a.amount,a.round_off,a.net_amt,a.pay_mode,a.received_amt,a.cust_name,a.phone_no,a.gst_flag,a.discount_type,a.created_by,a.created_dt,a.modified_by,a.modified_dt,a.cancelled_by,a.cancelled_dt FROM td_receipt_cancel_new AS a WHERE date(a.cancelled_dt) BETWEEN '{can_rep.from_date}' AND '{can_rep.to_date}'"
#     cursor.execute(query)
#     records = cursor.fetchall()
#     # print(records)
#     result = createResponse(records,cursor.column_names,1)
#     conn.close()
#     cursor.close()
#     return result


###########################################################################################################################

# @app.get('/api/refund_bill_data/{recp_no}')
# async def refund_bill_data(recp_no:int):
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"SELECT a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, c.item_name FROM td_item_sale a, md_items c WHERE a.item_id=c.id and a.receipt_no={recp_no}"
#     cursor.execute(query)
#     records = cursor.fetchall()
#     result = createResponse(records, cursor.column_names, 1)
#     conn.close()
#     cursor.close()
#     if cursor.rowcount>0:
#         conn1 = connect()
#         cursor1 = conn1.cursor()
#         query1 = f"SELECT b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.gst_flag, b.discount_type, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt FROM td_receipt b WHERE b.receipt_no={recp_no}"
#         cursor1.execute(query1)
#         records1 = cursor1.fetchall()
#         result1 = createResponse(records1, cursor1.column_names, 1)
#         conn1.close()
#         cursor1.close()
#         if cursor1.rowcount>0:

#             resData= {"status":1, 
#                   "data":result,
#                   "data1":result1
#                   }
#         else:
#             resData= {
#             "status":0,
#             "data":"no data found"
#             }

#     else:
#         resData = {
#             "status":-1,
#             "data":"no data found in item table"
#             }

#     return resData

# Cancel Item
#--------------------------------------------------------------------------------------------------------------------------
# @app.post('/api/cancel_item')
# async def cancel_item(cn_item:CancelItem):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     conn = connect()
#     cursor = conn.cursor()
#     query = f"SELECT receipt_no,comp_id,br_id,item_id,trn_date,price,dis_pertg,discount_amt,cgst_prtg,cgst_amt,sgst_prtg,sgst_amt,qty,created_by,created_dt,modified_by,modified_dt FROM td_item_sale WHERE receipt_no = {cn_item.receipt_no} AND item_id = {cn_item.item_id}"
#     cursor.execute(query)
#     records = cursor.fetchone()
#     conn.close()
#     cursor.close()
#     rec = list(records)
    
#     rec.append(cn_item.user_id)
#     rec.append(formatted_dt)
#     rec[12]=cn_item.qty

#     print(rec)
    
#     if cursor.rowcount>0:
#         conn1 = connect()
#         cursor1 = conn1.cursor()
       
#         query1 = f"INSERT INTO td_item_sale_cancel (receipt_no,comp_id,br_id,item_id,trn_date,price,dis_pertg,discount_amt,cgst_prtg,cgst_amt,sgst_prtg,sgst_amt,qty,created_by,created_dt,modified_by,modified_dt, cancelled_by, cancelled_dt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#         cursor1.execute(query1, tuple(rec))
#         conn1.commit()
#         conn1.close()
#         cursor1.close()

#         if cursor1.rowcount>0:
#             conn2 = connect()
#             cursor2 = conn2.cursor()

#             query2 = f"UPDATE td_item_sale JOIN td_stock ON td_item_sale.comp_id=td_stock.comp_id AND td_item_sale.br_id=td_stock.br_id SET td_item_sale.qty=td_item_sale.qty-{cn_item.qty}, td_stock.stock=td_stock.stock+{cn_item.qty}, td_item_sale.modified_by='{cn_item.user_id}', td_item_sale.modified_dt='{formatted_dt}', td_stock.modified_by='{cn_item.user_id}', td_stock.modified_dt='{formatted_dt}' WHERE td_item_sale.item_id={cn_item.item_id} AND td_stock.item_id={cn_item.item_id} AND td_item_sale.receipt_no={cn_item.receipt_no}"

#             cursor2.execute(query2)
#             conn2.commit()
#             conn2.close()
#             cursor2.close()

#             if cursor2.rowcount>0:
#                 conn3 = connect()
#                 cursor3 = conn3.cursor()

#                 query3 = f"DELETE FROM td_item_sale WHERE qty='0' AND item_id={cn_item.item_id} AND receipt_no={cn_item.receipt_no}"

#                 cursor3.execute(query3)
#                 conn3.commit()
#                 conn3.close()
#                 cursor3.close()

#                 resData = {
#                     "status":1,
#                     "data":"Item cancelled and stock updated successfully"
#                 }

#             else:
#                 resData ={
#                     "status":0,
#                     "data":"Error while updating td_item_sale, td_stock"
#                 }
#         else:
#             resData={
#                 "status":-1,
#                 "data":"Error while inserting into td_item_sale_cancel"
#             }
#     else:
#         resData={
#             "status":-2,
#             "data":"Error while selecting data"
#         }
#     return resData
                
#refund item
#--------------------------------------------------------------------------------------------------------------------------
@app.post('/api/refund_item')
async def refund_item(refund:list[RefundItem]):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    tcgst_amt = 0
    tsgst_amt = 0
    # return refund
    for i in refund:
        tcgst_amt += i.cgst_amt
        tsgst_amt += i.sgst_amt

        conn = connect()
        cursor = conn.cursor()
    
        query = f"INSERT INTO td_refund_item (receipt_no,refund_dt,refund_rcpt_no,comp_id,br_id,item_id,price,dis_pertg,discount_amt,cgst_prtg,cgst_amt,sgst_prtg,sgst_amt,qty,refund_by,refund_at) VALUES ({i.receipt_no},'{formatted_datetime}','{receipt}',{i.comp_id},{i.br_id},{i.item_id},{i.price},{i.dis_pertg},{i.discount_amt},{i.cgst_prtg},{i.cgst_amt},{i.sgst_prtg},{i.sgst_amt},{i.qty},'{i.user_id}','{formatted_datetime}')"

        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()

        if cursor.rowcount>0:

            conn1 = connect()
            cursor1 = conn1.cursor()

            query1 = f"UPDATE td_stock SET stock=stock+{i.qty}, modified_by='{i.user_id}', modified_dt='{formatted_datetime}' WHERE comp_id={i.comp_id} AND br_id={i.br_id} AND item_id={i.item_id}"

            cursor1.execute(query1)
            conn1.commit()
            conn1.close()
            cursor1.close()
            if cursor1.rowcount==1:
                resData = {"status":1, "data":receipt}
            else:
                resData = {"status":0, "data":'error while updating stock'}
        
        else:
            resData = {"status":-1, "data":"Data not inserted in refund_item"}

    
    conn = connect()
    cursor = conn.cursor()
    
    query = f"INSERT INTO td_refund_bill (receipt_no, refund_dt, refund_rcpt_no, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, cust_name, phone_no, gst_flag, discount_type, refund_by, refund_at) VALUES ({refund[0].receipt_no},'{formatted_datetime}','{receipt}',{refund[0].tprice},{refund[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{refund[0].tot_refund_amt},{refund[0].round_off},{refund[0].net_amt},'{refund[0].pay_mode}','{refund[0].cust_name}','{refund[0].phone_no}','{refund[0].gst_flag}','{refund[0].discount_type}','{refund[0].user_id}','{formatted_datetime}')"
    # print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount==1:
        ResData = {"status":1, "data":resData}
    else:
        ResData = {"status":0, "data":"Data not inserted"}
   
    return ResData

# Refund Report
#--------------------------------------------------------------------------------------------------------------------------

# SELECT * 
# FROM td_refund_item a, md_items b, md_company c
# where a.item_id=b.id
# and a.comp_id=c.id
# and a.comp_id=1
# and a.refund_dt = '2024-03-21'

#======================================================================================================
@app.post('/api/refund_list')
async def refund_list(ref:RefundList):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT DISTINCT a.receipt_no, a.trn_date, a.net_amt, a.phone_no FROM td_receipt a, td_item_sale b WHERE a.receipt_no=b.receipt_no AND b.comp_id = {ref.comp_id} AND b.br_id = {ref.br_id} AND a.phone_no = '{ref.phone_no}' AND a.trn_date BETWEEN DATE_SUB(DATE(now()), INTERVAL {ref.ref_days}-1 DAY) AND DATE(now()) ORDER BY a.trn_date DESC"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result
#======================================================================================================
# SMS 

# def sms(phone_no:int, template):
#     otp = random.randint(1000,9999)

#     url = template.replace("#{SENDER}#", str(phone_no)).replace("#{OTP}#", str(otp))
#     # f"https://bulksms.sssplsales.in/api/api_http.php?username=SYNERGIC&password=SYN@526RGC&senderid=SYNGIC&to={phone_no}&text=OTP for mobile verification is {otp}. This code is valid for 5 minutes. Please do not share this OTP with anyone.-SYNGIC&route=Informative&type=text"

#     # print(url)

#     payload = {}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     # print(response.text)
#     return {"msg": response.text, "otp": otp}

#======================================================================================================

# def short_url(url:str):
#     short_url = quote(url, safe="!~*'()")

#     api_url = f"https://is.gd/create.php?format=json&url={short_url}"

#     payload = {}
#     headers = {}

#     response = requests.request("GET", api_url, headers=headers, data=payload)
#     response = json.loads(response.text)
#     final_url = response['shorturl'] if response['shorturl'] else ''
#     return {"msg": final_url}

# def send_bill_sms(url:str, phone_no:str, template):
#     url = template.replace("#{SENDER}#", str(phone_no)).replace("#{URL}#", str(url))

#     # f"https://bulksms.sssplsales.in/api/api_http.php?username=SYNERGIC&password=SYN@526RGC&senderid=SYNGIC&to={phone_no}&text=Dear customer, thank you for shopping with us. For eBill please click {url} -Synergic softek solutions pvt ltd.&route=Informative&type=text"

#     payload = {}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     print(response.text)
#     return {"msg": response.text}
#     # return response.text
#====================================================================================================================

# Refund Report [Bill]

@app.post('/api/refund_bill_report')
async def sale_report(sl_rep:RefundBillReport):
    conn = connect()
    cursor = conn.cursor()

    query=f"select a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt,  count(b.refund_rcpt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.refund_by from  td_refund_bill a, td_refund_item b where a.refund_rcpt_no = b.refund_rcpt_no  and   a.refund_dt between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND b.br_id = {sl_rep.br_id} and a.refund_by='{sl_rep.user_id}' group by a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt, a.refund_by"

    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":[]}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData
#======================================================================================================
# Customer Information 

@app.post('/api/cust_info')
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

#======================================================================================================
# Insert New Customer Information

# def new_cust_info(query, cust_name:str, phone_no:str):
  
    # conn = connect()
    # cursor = conn.cursor()
    # query_1= f"update md_customer set cust_name = '{cust_name}' where phone_no = '{phone_no}'"
    # cursor.execute(query)
    # conn.commit()
    # conn.close()
    # cursor.close()


    # conn = connect()
    # cursor = conn.cursor()
    # query_2= f"insert into md_customer (cust_name,phone_no) values ('{cust_name}','{phone_no}')"
    # cursor.execute(query)
    # conn.commit()
    # conn.close()
    # cursor.close()

#======================================================================================================

# Search Bill by Phone no.

@app.post('/api/search_bill_by_phone')
async def search_bill_by_phone(bill:BillList):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT DISTINCT a.receipt_no, a.trn_date, a.net_amt, a.phone_no FROM td_receipt a, td_item_sale b WHERE a.receipt_no=b.receipt_no AND b.comp_id = {bill.comp_id} AND b.br_id = {bill.br_id} AND a.phone_no = '{bill.phone_no}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData = {
            "status":1,
            "data":result
        }
    else:
        resData = {
            "status":0,
            "data":"No Bill Found"
        }

    return resData

# Search Bills by item name
#======================================================================================================

@app.post('/api/billsearch_by_item')
async def billsearch_by_item(item:SearchByItem):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no,a.item_id,a.qty,a.price,b.item_name FROM td_item_sale a, md_items b WHERE a.item_id=b.id AND a.comp_id=b.comp_id AND a.comp_id={item.comp_id} AND a.br_id={item.br_id} AND b.id={item.item_id} AND a.trn_date BETWEEN '{item.from_date}' AND '{item.to_date}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData= {
        "status":1, 
        "data":result}
    else:
        resData= {
        "status":0,
        "data":[]
        }
    return resData