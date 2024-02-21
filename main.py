from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserLogin,Receipt,CreatePIN,DashBoard,SearchBill,SaleReport,ItemReport,EditHeaderFooter,EditItem,EditRcpSettings
from datetime import datetime, date
from utils import get_hashed_password, verify_password


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
    query = f"SELECT a.*, b.* FROM md_items a, md_item_rate b WHERE a.id=b.item_id AND a.com_id={comp_id}"
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
    query = f"SELECT a.id, a.item_name, c.price, c.discount, c.sale_price, c.hsn_code, c.cgst, c.sgst FROM md_items a, md_company b, md_item_rate c WHERE a.com_id=b.id AND a.id=c.item_id AND a.id={item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result'''

# Generate receipt no.


# Item Sale
#-------------------------------------------------------------------------------------------------------------
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
    query = f"INSERT INTO td_receipt (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, created_by, created_dt) VALUES ('{receipt}','{formatted_datetime}',{rcpt[0].tprice},{rcpt[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{rcpt[0].amount},{rcpt[0].round_off},{rcpt[0].net_amt},'{rcpt[0].pay_mode}','{rcpt[0].received_amt}','{rcpt[0].pay_dtls}','{rcpt[0].cust_name}','{rcpt[0].phone_no}','{rcpt[0].created_by}','{formatted_datetime}')"
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
#-------------------------------------------------------------------------------------------------------------
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
    query = f"SELECT a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name FROM td_item_sale a, td_receipt b, md_items c WHERE a.receipt_no=b.receipt_no and a.trn_date=b.trn_date and a.item_id=c.id and a.receipt_no={recp_no}"
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
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/sale_report')
async def sale_report(sl_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, sum(a.price)price, sum(a.discount_amt)discount_amt, sum(a.cgst_amt)cgst_amt, sum(a.sgst_amt)sgst_amt, sum(a.round_off)rount_off, sum(a.amount)net_amt, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date, a.created_by"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":"no such data"}
    else:
        resData= {
        "status":1,
        "data":result
        }
    return resData

# Collection Report
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/collection_report')
async def collection_report(col_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"Select created_by, pay_mode, sum(net_amt)net_amt from ( select Distinct a.created_by created_by, a.pay_mode pay_mode, a.net_amt net_amt from td_receipt a, td_item_sale b where a.receipt_no = b.receipt_no and a.trn_date BETWEEN '{col_rep.from_date}' and '{col_rep.to_date}' and b.comp_id= {col_rep.comp_id} AND b.br_id = {col_rep.br_id} )a group by created_by, pay_mode"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":"no such data"}
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
    query = f"select a.receipt_no,a.trn_date,a.qty,a.price,a.discount_amt,a.cgst_amt,a.sgst_amt,b.amount,b.pay_mode,c.item_name,d.branch_name from   td_item_sale a, td_receipt b, md_items c, md_branch d where  a.receipt_no = b.receipt_no AND a.comp_id = c.com_id AND a.comp_id = d.comp_id AND a.br_id = d.id AND a.item_id = c.id And a.trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' And a.comp_id = {item_rep.comp_id} AND a.br_id = {item_rep.br_id} AND a.item_id = {item_rep.item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":"no such data"}
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
    query = f"select distinct a.receipt_no, a.trn_date, (a.price - a.discount_amt)taxable_amt, a.cgst_amt, a.sgst_amt, (a.cgst_amt + a.sgst_amt)total_tax, a.net_amt from td_receipt a, td_item_sale b where a.receipt_no = b.receipt_no and b.comp_id = {gst_st.comp_id} and b.br_id = {gst_st.br_id} and a.trn_date BETWEEN '{gst_st.from_date}' and '{gst_st.to_date}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":"no such data"}
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
    query = f"SELECT cgst_prtg, SUM(cgst_amt)cgst_amt, SUM(sgst_amt)sgst_amt, SUM(cgst_amt) + SUM(sgst_amt)total_tax FROM td_item_sale WHERE comp_id = {gst_sm.comp_id} AND br_id = {gst_sm.br_id} AND trn_date BETWEEN '{gst_sm.from_date}' AND '{gst_sm.to_date}' GROUP BY cgst_prtg"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[]:
        resData= {"status":0, "data":"no such data"}
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
@app.post('/api/edit_items')
async def edit_items(edit_item:EditItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_item_rate JOIN md_items ON md_items.id=md_item_rate.item_id SET md_item_rate.price = {edit_item.price}, md_item_rate.discount = {edit_item.discount}, md_item_rate.cgst = {edit_item.cgst}, sgst = {edit_item.sgst}, md_item_rate.modified_by = '{edit_item.modified_by}', md_item_rate.modified_dt = '{formatted_dt}' WHERE md_item_rate.item_id={edit_item.item_id} AND md_items.com_id={edit_item.com_id}"
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

# Edit Receipt Settings
#-------------------------------------------------------------------------------------------------------------
@app.post('/api/edit_rcp_settings')
async def edit_rcp_settings(rcp_set:EditRcpSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET rcpt_type='{rcp_set.rcpt_type}', gst_flag='{rcp_set.gst_flag}', cust_inf='{rcp_set.cust_inf}', pay_mode='{rcp_set.pay_mode}', discount_type='{rcp_set.discount_type}', created_by='{rcp_set.created_by}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
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