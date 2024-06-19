from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import SaleReport,CollectionReport,PayModeReport,UserWiseReport,GSTstatement,RefundReport,CreditReport,ItemReport,CancelReport,DaybookReport,CustomerLedger

reportRouter = APIRouter()

#======================================================================================================
# Sale Report

@reportRouter.post('/sale_report')
async def sale_report(sale:SaleReport):
    if ({sale.br_id}.pop())>0:
        select = "a.cust_name,a.phone_no,a.receipt_no,a.trn_date,count(b.receipt_no)no_of_items, SUM(b.qty) qty,a.price price,a.discount_amt discount_amt,a.cgst_amt cgst_amt,a.sgst_amt sgst_amt,a.round_off rount_off,a.net_amt,IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode,c.user_name created_by"
        table_name = "td_receipt a,td_item_sale b,md_user c"
        where = f"a.receipt_no = b.receipt_no AND a.trn_date BETWEEN '{sale.from_date}' AND '{sale.to_date}' AND b.comp_id = {sale.comp_id} AND b.br_id = {sale.br_id} AND a.created_by=c.user_id"
        order = "Group BY a.cust_name,a.phone_no,a.receipt_no,a.trn_date,a.price,a.discount_amt,a.cgst_amt,a.sgst_amt,a.round_off,a.net_amt,a.pay_mode,a.created_by Order by a.trn_date,a.receipt_no"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
    
    else:
        select = "a.cust_name,a.phone_no,a.receipt_no,a.trn_date,count(b.receipt_no)no_of_items, SUM(b.qty) qty,a.price price,a.discount_amt discount_amt,a.cgst_amt cgst_amt,a.sgst_amt sgst_amt,a.round_off rount_off,a.net_amt,IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode,c.user_name created_by"
        table_name = "td_receipt a,td_item_sale b,md_user c"
        where = f"a.receipt_no = b.receipt_no AND a.trn_date BETWEEN '{sale.from_date}' AND '{sale.to_date}' AND b.comp_id = {sale.comp_id} AND a.created_by=c.user_id"
        order = "Group BY a.cust_name,a.phone_no,a.receipt_no,a.trn_date,a.price,a.discount_amt,a.cgst_amt,a.sgst_amt,a.round_off,a.net_amt,a.pay_mode,a.created_by Order by a.trn_date,a.receipt_no"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)

    return res_dt

#===================================================================================================
# Bill Report / Collection Report
'''
@reportRouter.post('/collection_report')
async def collection_report(data:CollectionReport):

    select = "a.created_by, IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode ,SUM(a.net_amt)net_amt,user_name, count(a.receipt_no)no_of_bills"
    table_name = f"(Select Distinct a.created_by created_by,a.pay_mode pay_mode,a.net_amt net_amt,c.user_name user_name, a.receipt_no receipt_no from   td_receipt a, td_item_sale b, md_user c where  a.created_by=c.user_id and a.receipt_no = b.receipt_no and a.trn_date BETWEEN '{data.from_date}' AND '{data.to_date}' and b.comp_id = {data.comp_id} AND b.br_id = {data.br_id} AND a.created_by = '{data.user_id}')a" if data.br_id>0 else f"(Select Distinct a.created_by created_by,a.pay_mode pay_mode,a.net_amt net_amt,c.user_name user_name, a.receipt_no receipt_no from   td_receipt a, td_item_sale b, md_user c where  a.created_by=c.user_id and a.receipt_no = b.receipt_no and a.trn_date BETWEEN '{data.from_date}' AND '{data.to_date}' and b.comp_id = {data.comp_id} AND a.created_by = '{data.user_id}')a"
    where = f""
    order = "GROUP BY a.created_by,a.pay_mode"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt 
    '''

# ==================================================================================================
# PayMode Report

@reportRouter.post('/paymode_report')
async def paymode_report(data:PayModeReport):

    select = "count(receipt_no)no_of_rcpt, IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode, Sum(net_amt) net_amt, sum(cancelled_amt)can_amt"

    table_name = f"(select receipt_no, pay_mode, net_amt, 0 cancelled_amt from td_receipt where trn_date BETWEEN '{data.from_date}' and '{data.to_date}' and comp_id= {data.comp_id} AND br_id = {data.br_id} UNION select a.receipt_no receipt_no, a.pay_mode pay_mode, 0 net_amt, a.net_amt cancelled_amt from td_receipt a,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and date(b.cancelled_dt) BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id= {data.comp_id} AND a.br_id = {data.br_id})a" if data.br_id>0 else f"(select receipt_no, pay_mode, net_amt, 0 cancelled_amt from td_receipt where trn_date BETWEEN '{data.from_date}' and '{data.to_date}' and comp_id= {data.comp_id} UNION select a.receipt_no receipt_no, a.pay_mode pay_mode, 0 net_amt, a.net_amt cancelled_amt from td_receipt a,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and date(b.cancelled_dt) BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id= {data.comp_id})a"

    where = f""
    order = "GROUP BY pay_mode"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
#  Userwise Sale Report Details

@reportRouter.post('/userwise_sale_report')
async def userwise_sale_report(data:UserWiseReport):

    select = "created_by, sum(net_amt)net_amt, sum(cancelled_amt)cancelled_amt, COUNT(receipt_no)no_of_receipts, user_name"
    table_name = f"( Select a.created_by created_by, a.net_amt net_amt, 0 cancelled_amt, c.user_name user_name, a.receipt_no receipt_no from td_receipt a, md_user c where a.created_by=c.user_id and a.trn_date BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id = {data.comp_id} AND a.br_id = {data.br_id} UNION Select a.created_by created_by, 0 net_amt, a.net_amt cancelled_amt, c.user_name user_name, b.receipt_no receipt_no from td_receipt a, md_user c,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.created_by=c.user_id and date(b.cancelled_dt) BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id = {data.comp_id} AND a.br_id = {data.br_id})a" if data.br_id>0 else f"( Select a.created_by created_by, a.net_amt net_amt, 0 cancelled_amt, c.user_name user_name, a.receipt_no receipt_no from td_receipt a, md_user c where a.created_by=c.user_id and a.trn_date BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id = {data.comp_id} UNION Select a.created_by created_by, 0 net_amt, a.net_amt cancelled_amt, c.user_name user_name, b.receipt_no receipt_no from td_receipt a, md_user c,td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.created_by=c.user_id and date(b.cancelled_dt) BETWEEN '{data.from_date}' and '{data.to_date}' and a.comp_id = {data.comp_id})a"
    where = f""
    order = "GROUP BY created_by,user_name"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# =================================================================================================
# GST Statement

@reportRouter.post('/gst_statement')
async def gst_statement(gst:GSTstatement):
    if ({gst.br_id}.pop())>0:
        select = "Distinct a.receipt_no, a.trn_date, (a.price - a.discount_amt)taxable_amt, a.cgst_amt, a.sgst_amt, (a.cgst_amt + a.sgst_amt)total_tax, a.net_amt"
        table_name = "td_receipt a, td_item_sale b"
        where = f"a.receipt_no = b.receipt_no AND b.comp_id = {gst.comp_id} AND b.br_id = {gst.br_id} AND a.trn_date BETWEEN '{gst.from_date}' AND '{gst.to_date}'"
        order = f""
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
    
    else:
        select = "Distinct a.receipt_no, a.trn_date, (a.price - a.discount_amt)taxable_amt, a.cgst_amt, a.sgst_amt, (a.cgst_amt + a.sgst_amt)total_tax, a.net_amt"
        table_name = "td_receipt a, td_item_sale b"
        where = f"a.receipt_no = b.receipt_no AND b.comp_id = {gst.comp_id} AND a.trn_date BETWEEN '{gst.from_date}' AND '{gst.to_date}'"
        order = f""
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)

    return res_dt

# ==================================================================================================
# GST Summary

@reportRouter.post('/gst_summary')
async def gst_summary(gst:GSTstatement):
    if ({gst.br_id}.pop())>0:
        select = "cgst_prtg, SUM(cgst_amt)cgst_amt, SUM(sgst_amt)sgst_amt, SUM(cgst_amt) + SUM(sgst_amt)total_tax"
        table_name = "td_item_sale"
        where = f"comp_id = {gst.comp_id} AND br_id = {gst.br_id} AND trn_date BETWEEN '{gst.from_date}' AND '{gst.to_date}'"
        order = "GROUP BY cgst_prtg"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
    
    else:
        select = "cgst_prtg, SUM(cgst_amt)cgst_amt, SUM(sgst_amt)sgst_amt, SUM(cgst_amt) + SUM(sgst_amt)total_tax"
        table_name = "td_item_sale"
        where = f"comp_id = {gst.comp_id} AND trn_date BETWEEN '{gst.from_date}' AND '{gst.to_date}'"
        order = "GROUP BY cgst_prtg"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)

    return res_dt

# ==================================================================================================
#  Refund Report Details 

@reportRouter.post('/refund_report')
async def refund_report(data:RefundReport):
    if ({data.br_id}.pop())>0:
        select = "a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt,  count(b.refund_rcpt_no)no_of_items, SUM(b.qty) qty, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.refund_by"
        table_name = "td_refund_bill a, td_refund_item b"
        where = f"a.refund_rcpt_no = b.refund_rcpt_no AND a.refund_dt BETWEEN '{data.from_date}' AND '{data.to_date}' AND b.comp_id = {data.comp_id} AND b.br_id = {data.br_id}"
        order = "group by a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt, a.refund_by"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
    
    else:
        select = "a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt,  count(b.refund_rcpt_no)no_of_items, SUM(b.qty) qty, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt,a.round_off, a.net_amt, a.refund_by"
        table_name = "td_refund_bill a, td_refund_item b"
        where = f"a.refund_rcpt_no = b.refund_rcpt_no AND a.refund_dt BETWEEN '{data.from_date}' AND '{data.to_date}' AND b.comp_id = {data.comp_id}"
        order = "group by a.cust_name, a.phone_no, a.refund_rcpt_no, a.refund_dt, a.refund_by"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)

    return res_dt

# ==================================================================================================
#  Credit Report Details 

@reportRouter.post('/credit_report')
async def credit_report(data:CreditReport):
    if ({data.br_id}.pop())>0:
        select = "trn_date, cust_name, phone_no, receipt_no, net_amt, received_amt as paid_amt, net_amt-received_amt as due_amt, created_by"
        table_name = "td_receipt"
        where = f"pay_mode = 'R' and net_amt-received_amt > 0 AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}' AND comp_id = {data.comp_id} AND br_id = {data.br_id}"
        order = "group by phone_no,receipt_no,trn_date,created_by"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
    
    else:
        select = "trn_date, cust_name, phone_no, receipt_no, net_amt, received_amt as paid_amt, net_amt-received_amt as due_amt, created_by"
        table_name = "td_receipt"
        where = f"pay_mode = 'R' and net_amt-received_amt > 0 AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}' AND comp_id = {data.comp_id}"
        order = "group by phone_no,receipt_no,trn_date,created_by"
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)

    return res_dt

# ==================================================================================================
# Item Wise Sale Report

@reportRouter.post('/item_report')
async def collection_report(item_rep:ItemReport):
    
    select = f"a.receipt_no,a.item_id,b.item_name,sum(a.qty)qty,sum(a.price*a.qty)price"
    table_name = "td_item_sale a, md_items b"
    where = f"a.item_id = b.id and a.comp_id = {item_rep.comp_id} and a.br_id = {item_rep.br_id} and a.trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' and a.receipt_no not in (select receipt_no from td_receipt_cancel_new where date(cancelled_dt)between '{item_rep.from_date}' and '{item_rep.to_date}')" if item_rep.br_id>0 else f"a.item_id = b.id and a.comp_id = {item_rep.comp_id} and a.trn_date BETWEEN '{item_rep.from_date}' and '{item_rep.to_date}' and a.receipt_no not in (select receipt_no from td_receipt_cancel_new where date(cancelled_dt)between '{item_rep.from_date}' and '{item_rep.to_date}')"
    order = "group by a.receipt_no,a.item_id,b.item_name"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

#=================================================================================================
# Cancel Report

@reportRouter.post('/cancel_report')
async def cancel_report(data:CancelReport):
    
    select = f"a.cust_name, a.phone_no, a.receipt_no, a.trn_date, count(b.receipt_no)no_of_items, a.price, a.discount_amt, a.cgst_amt, a.sgst_amt, a.round_off, a.net_amt, IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode, a.created_by"
    table_name = "td_receipt a,td_item_sale b"
    where = f"a.receipt_no = b.receipt_no and b.comp_id = {data.comp_id} AND b.br_id = {data.br_id} and a.receipt_no In (select receipt_no from td_receipt_cancel_new where date(cancelled_dt) between '{data.from_date}' and '{data.to_date}')" if data.br_id>0 else f"a.receipt_no = b.receipt_no and b.comp_id = {data.comp_id} AND a.receipt_no In (select receipt_no from td_receipt_cancel_new where date(cancelled_dt) between '{data.from_date}' and '{data.to_date}')"
    order = "group by a.cust_name, a.phone_no, a.receipt_no, a.trn_date,a.price, a.discount_amt, a.cgst_amt, a.sgst_amt, a.round_off, a.net_amt, a.pay_mode, a.created_by Order by a.trn_date,a.receipt_no"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

#==================================================================================================
# Daybook Report

@reportRouter.post('/daybook_report')
async def daybook_report(data:DaybookReport):
    
    select = f"receipt_no, trn_date, IF(pay_mode='C', 'Cash', IF(pay_mode='U', 'UPI', IF(pay_mode='D', 'Card', IF(pay_mode='R', 'Credit', '')))) pay_mode, net_amt, 0 cancelled_amt, created_by, ''cancelled_by"
    table_name = "td_receipt"
    where = f"comp_id = {data.comp_id} and br_id = {data.br_id} and trn_date between '{data.from_date}' and '{data.to_date}' UNION select a.receipt_no receipt_no, a.trn_date trn_date, IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode, 0 net_amt, a.net_amt cancelled_amt, a.created_by created_by, b.cancelled_by cancelled_by From td_receipt a, td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and date(b.cancelled_dt) between '{data.from_date}' and '{data.to_date}')'"if data.br_id>0 else f"comp_id = {data.comp_id} and trn_date between '{data.from_date}' and '{data.to_date}' UNION select a.receipt_no receipt_no, a.trn_date trn_date, IF(a.pay_mode='C', 'Cash', IF(a.pay_mode='U', 'UPI', IF(a.pay_mode='D', 'Card', IF(a.pay_mode='R', 'Credit', '')))) pay_mode, 0 net_amt, a.net_amt cancelled_amt, a.created_by created_by, b.cancelled_by cancelled_by From td_receipt a, td_receipt_cancel_new b where a.receipt_no = b.receipt_no and a.comp_id = {data.comp_id} and date(b.cancelled_dt) between '{data.from_date}' and '{data.to_date}'"
    order = ""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ======================================================================================================
# Customer Ledger

@reportRouter.post('/customer_ledger')
async def customer_ledger(data:CustomerLedger):
    select = f"ifnull(b.cust_name,'NA')cust_name, a.phone_no, a.recover_dt, a.paid_amt, a.due_amt, a.curr_due_amt balance"
    table_name = "td_recovery_new a,md_customer b"
    where = f"a.comp_id = b.comp_id and a.phone_no = b.phone_no and a.comp_id = {data.comp_id} and a.br_id = {data.br_id} and a.phone_no = {data.phone_no} order by a.recover_dt,a.recover_id" if data.br_id>0 else f"a.comp_id = b.comp_id and a.phone_no = b.phone_no and a.comp_id = {data.comp_id} and a.phone_no = {data.phone_no} order by a.recover_dt,a.recover_id"
    order = ""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

    