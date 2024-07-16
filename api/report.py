from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import DashBoard,SaleReport,GSTStatement,GSTSummary,ItemReport,RefundBillReport,BillList,SearchByItem,CreditReport,CancelReport,DaybookReport,SearchByRcpt,SearchByName,UserwiseReport,CustomerLedger,RecveryReport,DueReport

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
    query = f"SELECT a.* FROM td_receipt a, md_user b, md_branch c, md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={rec_bill.comp_id} and c.id={rec_bill.br_id} and a.trn_date='{rec_bill.trn_date}' and a.created_by='{rec_bill.user_id}' and a.receipt_no not in (select receipt_no from td_receipt_cancel_new) ORDER BY created_dt DESC LIMIT 10"
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
    query=f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.pay_mode, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} and a.receipt_no not in (select receipt_no from td_receipt_cancel_new where date(cancelled_dt) between '{sl_rep.from_date}' and '{sl_rep.to_date}') group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date,a.price, a.discount_amt, a.cgst_amt, a.sgst_amt, a.round_off, a.net_amt, a.pay_mode, a.created_by Order by a.trn_date,a.receipt_no"
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

# Collection Report (Sales Summary in app)
#---------------------------------------------------------------------------------------------------------------------------
@repoRouter.post('/collection_report')
async def collection_report(col_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select count(receipt_no)no_of_rcpt, pay_mode, Sum(net_amt) net_amt, sum(cancelled_amt)can_amt from( select receipt_no, pay_mode, net_amt, 0 cancelled_amt from td_receipt where trn_date BETWEEN '{col_rep.from_date}' and '{col_rep.to_date}' and comp_id= {col_rep.comp_id} AND br_id = {col_rep.br_id} UNION select a.receipt_no receipt_no, a.pay_mode pay_mode, 0 net_amt, a.net_amt cancelled_amt from td_receipt a,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and date(b.cancelled_dt) BETWEEN '{col_rep.from_date}' and '{col_rep.to_date}' and a.comp_id= {col_rep.comp_id} AND a.br_id = {col_rep.br_id})a group by pay_mode"
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
    query = f"SELECT a.receipt_no,a.item_id,b.item_name,sum(a.qty)qty,sum(a.price*a.qty)price from td_item_sale a, md_items b where a.item_id = b.id and a.comp_id = {item_rep.comp_id} and a.br_id = {item_rep.br_id} and a.trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' and a.receipt_no not in (select receipt_no from td_receipt_cancel_new where date(cancelled_dt)between '{item_rep.from_date}' and '{item_rep.to_date}') group by a.receipt_no,a.item_id,b.item_name"
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
async def gst_statement(gst_st:GSTStatement):
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
async def gst_summary(gst_sm:GSTSummary):
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
            "data":[]
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
# Search by Receipt No

@repoRouter.post('/search_bill_by_receipt')
async def search_bill_by_receipt(bill:SearchByRcpt):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT DISTINCT receipt_no, trn_date, pay_mode, net_amt FROM td_receipt WHERE comp_id = {bill.comp_id} AND br_id = {bill.br_id} AND receipt_no = '{bill.receipt_no}'"
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
            "data":[]
        }

    return resData

#==================================================================================================
# Search Bill by Customer Name

@repoRouter.post('/search_bill_by_name')
async def search_bill_by_receipt(bill:SearchByName):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT DISTINCT receipt_no, trn_date, pay_mode, net_amt FROM td_receipt WHERE comp_id = {bill.comp_id} AND br_id = {bill.br_id} AND cust_name LIKE '%{bill.cust_name}%'"
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
            "data":[]
        }

    return resData

#=================================================================================================

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

#===================================================================================================
@repoRouter.post('/cancel_report')
async def cancel_report(data:CancelReport):
    conn = connect()
    cursor = conn.cursor()
    
    query=f"select a.cust_name, a.phone_no, a.receipt_no, a.trn_date, count(b.receipt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt, a.round_off, a.net_amt, a.pay_mode, a.created_by from td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no and b.comp_id = {data.comp_id} AND b.br_id = {data.br_id} and a.receipt_no In (select receipt_no from td_receipt_cancel_new where date(cancelled_dt) between '{data.from_date}' and '{data.to_date}') group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date,a.price, a.discount_amt, a.cgst_amt, a.sgst_amt, a.round_off, a.net_amt, a.pay_mode, a.created_by Order by a.trn_date,a.receipt_no"

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

#===================================================================================================
# Daybook Report

@repoRouter.post('/daybook_report')
async def daybook_report(data:DaybookReport):
    conn = connect()
    cursor = conn.cursor()
    
    query=f"select receipt_no, trn_date, pay_mode, net_amt, 0 cancelled_amt, created_by, ''cancelled_by From td_receipt where comp_id = {data.comp_id} and br_id = {data.br_id} and trn_date between '{data.from_date}' and '{data.to_date}' UNION select a.receipt_no receipt_no, a.trn_date trn_date, a.pay_mode, 0 net_amt, a.net_amt cancelled_amt, a.created_by created_by, b.cancelled_by cancelled_by From td_receipt a, td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and date(b.cancelled_dt) between '{data.from_date}' and '{data.to_date}'"

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

#============================================================================================
# Userwise Report

@repoRouter.post('/userwise_report')
async def userwise_report(data:UserwiseReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select created_by, sum(net_amt)net_amt, sum(cancelled_amt)cancelled_amt, COUNT(receipt_no)no_of_receipts, user_name from( Select a.created_by created_by, a.net_amt net_amt, 0 cancelled_amt, c.user_name user_name, a.receipt_no receipt_no from td_receipt a, md_user c where a.created_by=c.user_id and a.trn_date BETWEEN '{data.from_date}' AND '{data.to_date}' and a.created_by='{data.user_id}' and a.comp_id = {data.comp_id} AND a.br_id = {data.br_id} UNION Select a.created_by created_by, 0 net_amt, a.net_amt cancelled_amt, c.user_name user_name, b.receipt_no receipt_no from td_receipt a, md_user c,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.created_by=c.user_id and date(b.cancelled_dt) BETWEEN '{data.from_date}' AND '{data.to_date}' and b.cancelled_by = '{data.user_id}' and a.comp_id = {data.comp_id} AND a.br_id = {data.br_id})a group by created_by,user_name"
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

# ===================================================================================================
# Customer Ledger

@repoRouter.post('/customer_ledger')
async def customer_ledger(data:CustomerLedger):
    conn = connect()
    cursor = conn.cursor()
    query = f"select ifnull(b.cust_name,'NA')cust_name, a.phone_no, a.recover_dt, a.paid_amt, a.due_amt, a.curr_due_amt balance from td_recovery_new a,md_customer b where a.comp_id = b.comp_id and a.phone_no = b.phone_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and a.phone_no = {data.phone_no} order by a.recover_dt,a.recover_id"
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

# ========================================================================================================
# Recovery report between 2 dates

@repoRouter.post('/recovery_report')
async def recovery_report(data:RecveryReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select ifnull(b.cust_name,'NA')cust_name, a.phone_no, a.recover_dt, Sum(a.paid_amt)recovery_amt from td_recovery_new a,md_customer b where a.comp_id = b.comp_id and a.phone_no = b.phone_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and a.recover_dt between '{data.from_date}' and '{data.to_date}' GROUP BY b.cust_name,a.phone_no,a.recover_dt order by a.recover_dt"
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

# =====================================================================================================
# Due report 

@repoRouter.post('/due_report')
async def due_report(data:DueReport):
    conn = connect()
    cursor = conn.cursor()
    query = f"select ifnull(b.cust_name,'NA')cust_name, a.phone_no, Sum(due_amt) - Sum(paid_amt)due_amt from td_recovery_new a,md_customer b where a.comp_id = b.comp_id and a.phone_no = b.phone_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and a.recover_dt <= '{data.date}' GROUP BY b.cust_name,a.phone_no having due_amt>0"
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