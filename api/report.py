from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import DashBoard,SaleReport,ItemReport,RefundBillReport,BillList,SearchByItem,CreditReport

# testing git
repoRouter = APIRouter()

# Dashboard
#-------------------------------------------------------------------------------------------------------------------------
@repoRouter.post('/billsummary')
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
@repoRouter.post('/recent_bills')
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

# Sale Report
#---------------------------------------------------------------------------------------------------------------------------
@repoRouter.post('/sale_report')
async def sale_report(sl_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    # query = f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, sum(a.price)price, sum(a.discount_amt)discount_amt, sum(a.cgst_amt)cgst_amt, sum(a.sgst_amt)sgst_amt, sum(a.round_off)rount_off, sum(a.amount)net_amt, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date, a.created_by"
    query=f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.pay_mode, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} and a.created_by='{sl_rep.user_id}' group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date, a.created_by"
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
@repoRouter.post('/collection_report')
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
@repoRouter.post('/item_report')
async def item_report(item_rep:ItemReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT receipt_no,trn_date,(price*qty)price,cgst_amt,sgst_amt,qty FROM td_item_sale where trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' and comp_id = {item_rep.comp_id} and br_id = {item_rep.br_id} and item_id = {item_rep.item_id}"
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
@repoRouter.post('/gst_statement')
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
@repoRouter.post('/gst_summary')
async def gst_summary(gst_sm:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT cgst_prtg, SUM(cgst_amt)cgst_amt, SUM(sgst_amt)sgst_amt, SUM(cgst_amt) + SUM(sgst_amt)total_tax FROM td_item_sale WHERE cgst_amt+sgst_amt>0 AND comp_id = {gst_sm.comp_id} AND br_id = {gst_sm.br_id} AND created_by = {gst_sm.user_id} AND trn_date BETWEEN '{gst_sm.from_date}' AND '{gst_sm.to_date}' GROUP BY cgst_prtg"
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

# Refund Report [Bill]

@repoRouter.post('/refund_bill_report')
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

# Search Bill by Phone no.

@repoRouter.post('/search_bill_by_phone')
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

@repoRouter.post('/billsearch_by_item')
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

#==================================================================================================

@repoRouter.get('/show_refund_bill/{recp_no}')
async def show_refund_bill(recp_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no, a.refund_dt, a.refund_rcpt_no, a.comp_id, a.br_id, a.item_id, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.refund_by, a.refund_at, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.cust_name, b.phone_no, b.gst_flag,b.gst_type,b.discount_flag, b.discount_type,b.discount_position, b.refund_by AS trefund_by, b.refund_at AS trefund_at, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name FROM td_refund_item a, td_refund_bill b, md_items c WHERE a.refund_rcpt_no=b.refund_rcpt_no and a.refund_dt=b.refund_dt and a.item_id=c.id and a.refund_rcpt_no={recp_no}"
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

# Credit Report
#==================================================================================================

@repoRouter.post('/credit_report')
async def credit_report(cr_rep:CreditReport):
    conn = connect()
    cursor = conn.cursor()

    query=f"select trn_date, phone_no, receipt_no, net_amt, received_amt as paid_amt, net_amt-received_amt as due_amt from  td_receipt  where pay_mode = 'R' and net_amt-received_amt > 0 and trn_date between '{cr_rep.from_date}' and '{cr_rep.to_date}' and comp_id = {cr_rep.comp_id} AND br_id = {cr_rep.br_id} and created_by='{cr_rep.user_id}' group by phone_no,receipt_no,trn_date,created_by"

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
        "data":[]
        }
    return resData
