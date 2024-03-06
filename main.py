from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserLogin,Receipt,CreatePIN,DashBoard,SearchBill,SaleReport,ItemReport,EditHeaderFooter,EditItem,EditRcpSettings,AddItem,CancelBill,AddUnit,EditUnit,InventorySearch
from datetime import datetime, date
from utils import get_hashed_password, verify_password

# testing git
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=3004, reload=True)

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
        if cursor.rowcount==1:
            resData = {"status":1, "data":receipt}
        else:
            resData = {"status":0, "data":'Data not inserted'}
    
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO td_receipt (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt) VALUES ('{receipt}','{formatted_datetime}',{rcpt[0].tprice},{rcpt[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{rcpt[0].amount},{rcpt[0].round_off},{rcpt[0].net_amt},'{rcpt[0].pay_mode}','{rcpt[0].received_amt}','{rcpt[0].pay_dtls}','{rcpt[0].cust_name}','{rcpt[0].phone_no}','{rcpt[0].gst_flag}','{rcpt[0].discount_type}','{rcpt[0].created_by}','{formatted_datetime}')"
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
#---------------------------------------------------------------------------------------------------------------------------
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
    query = f"SELECT a.* FROM td_receipt a, md_user b, md_branch c, md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={rec_bill.comp_id} and c.id={rec_bill.br_id} and a.trn_date='{rec_bill.trn_date}' and a.created_by='{rec_bill.user_id}' ORDER BY created_dt DESC LIMIT 4"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

#Select Bill
# ------------------------------------------------------------------------------------------------------------
@app.get('/api/show_bill/{recp_no}')
async def show_bill(recp_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.gst_flag, b.discount_type, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name FROM td_item_sale a, td_receipt b, md_items c WHERE a.receipt_no=b.receipt_no and a.trn_date=b.trn_date and a.item_id=c.id and a.receipt_no={recp_no}"
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
        "data":"no data found"
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
    query = f"select distinct a.receipt_no, a.trn_date, (a.price - a.discount_amt)taxable_amt, a.cgst_amt, a.sgst_amt, (a.cgst_amt + a.sgst_amt)total_tax, a.net_amt from td_receipt a, td_item_sale b where a.receipt_no = b.receipt_no and b.comp_id = {gst_st.comp_id} and b.br_id = {gst_st.br_id} and a.created_by = {gst_st.user_id} and a.trn_date BETWEEN '{gst_st.from_date}' and '{gst_st.to_date}'"
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
    query = f"UPDATE md_item_rate JOIN md_items ON md_items.id=md_item_rate.item_id SET md_item_rate.price = {edit_item.price}, md_item_rate.discount = {edit_item.discount}, md_item_rate.cgst = {edit_item.cgst}, md_item_rate.sgst = {edit_item.sgst}, md_item_rate.modified_by = '{edit_item.modified_by}', md_item_rate.modified_dt = '{formatted_dt}', md_items.modified_by = '{edit_item.modified_by}', md_items.modified_dt = '{formatted_dt}' WHERE md_item_rate.item_id={edit_item.item_id} AND md_items.comp_id={edit_item.comp_id} AND md_items.unit_id={edit_item.unit_id}"
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
            resData= {
            "status":1,
            "data":"data added successfully"
            } 
        else:
            resData= {"status":0, "data":"item rate not added"}
    else:
        resData={"status":-1, "data":"data not added" }
       
    return resData

# Edit Receipt Settings
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/edit_rcp_settings')
async def edit_rcp_settings(rcp_set:EditRcpSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET rcpt_type='{rcp_set.rcpt_type}', gst_flag='{rcp_set.gst_flag}', unit_flag='{rcp_set.unit_flag}', cust_inf='{rcp_set.cust_inf}', pay_mode='{rcp_set.pay_mode}', discount_flag='{rcp_set.discount_flag}', discount_type='{rcp_set.discount_type}', price_type='{rcp_set.price_type}', created_by='{rcp_set.created_by}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
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
    query = "SELECT * FROM md_version"
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

# Cancel Bill
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


@app.post('/api/cancel_bill')
async def cancel_bill(del_bill:CancelBill):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
    cursor.execute(query)
    records = cursor.fetchone()
    conn.close()
    cursor.close()
    # print (type(records))
    rec = list(records)
    rec.append(del_bill.user_id)
    rec.append(formatted_dt)
    # return len(rec)
    # result = createResponse(records, cursor.column_names, 1)
    # i = result[0]
    # print(i["created_dt"])

    if cursor.rowcount>0:
       
        conn1 = connect()
        cursor1 = conn1.cursor()
        # query1 = f"INSERT INTO td_receipt_cancel (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) Values ({i["receipt_no"]}, {i["trn_date"]}, {i["price"]}, {i["discount_amt"]}, {i["cgst_amt"]}, {i["sgst_amt"]}, {i["amount"]}, {i["round_off"]}, {i["net_amt"]}, {i["pay_mode"]}, {i["received_amt"]}, {i["pay_dtls"]}, {i["cust_name"]}, {i["phone_no"]}, {i["created_by"]}, {i["created_dt"]}, {i["modified_by"]}, {i["modified_dt"]}, '{del_bill.user_id}', '{formatted_dt}')"
        query1 = f"INSERT INTO td_receipt_cancel_new (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor1.execute(query1, tuple(rec))
        conn1.commit()
        conn1.close()
        cursor1.close()
        # return cursor1.rowcount
        if cursor1.rowcount>0:
            conn2 = connect()
            cursor2 = conn2.cursor()
            query2 = f"DELETE FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
            cursor2.execute(query2)
            conn2.commit()
            conn2.close()
            cursor2.close()
            if cursor2.rowcount>0:
                resData= {
                "status":1,
                "data":"Bill Cancelled Successfully"
                } 
            else:
                resData= {"status":0, "data":"Bill Not Cancelled"}
        else:
            resData={"status":-1, "data":"bill not added" }
    else:
        resData={"status":-2, "data":"bill not selected properly" }
    return resData

# Add unit
#---------------------------------------------------------------------------------------------------------------------------
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
        query = f"UPDATE md_unit SET unit_name='{edit.unit_name}', modified_by='{edit.modified_by}', modified_at='      {formatted_dt}' WHERE sl_no={edit.sl_no} and comp_id={edit.comp_id}"
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
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT stock FROM td_stock WHERE comp_id = {st_list.comp_id} AND br_id = {st_list.br_id} AND item_id = {st_list.item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result[0]
