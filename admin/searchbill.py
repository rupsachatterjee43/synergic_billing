from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import SearchByDate,SearchByPhone,SearchByItem,PrintBill

searchRouter = APIRouter()

# ==================================================================================================
# Search Bill by Date

@searchRouter.post('/search_by_date')
async def search_by_date(data:SearchByDate):

    select = "receipt_no,trn_date,created_by,net_amt,IF(pay_mode='C', 'Cash', IF(pay_mode='U', 'UPI', IF(pay_mode='D', 'Card', IF(pay_mode='R', 'Credit', '')))) pay_mode"
    table_name = "td_receipt"
    where = f"comp_id = {data.comp_id} AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Search Bill by Customer Phone No.

@searchRouter.post('/search_by_phone')
async def search_by_phone(data:SearchByPhone):

    select = "receipt_no,trn_date,created_by,net_amt,IF(pay_mode='C', 'Cash', IF(pay_mode='U', 'UPI', IF(pay_mode='D', 'Card', IF(pay_mode='R', 'Credit', '')))) pay_mode"
    table_name = "td_receipt"
    where = f"comp_id = {data.comp_id} AND phone_no = {data.phone_no} AND trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# ==================================================================================================
# Search Bill by Customer Product

@searchRouter.post('/search_by_item')
async def search_by_item(data:SearchByItem):

    select = "a.receipt_no,c.trn_date,a.item_id,b.item_name,a.qty,a.price,IF(c.pay_mode='C', 'Cash', IF(c.pay_mode='U', 'UPI', IF(c.pay_mode='D', 'Card', IF(c.pay_mode='R', 'Credit', '')))) pay_mode,c.created_by"
    table_name = "td_item_sale a, md_items b, td_receipt c"
    where = f"a.receipt_no=c.receipt_no AND a.item_id=b.id AND a.comp_id=b.comp_id AND a.comp_id = {data.comp_id} AND b.id = {data.item_id} AND a.trn_date BETWEEN '{data.from_date}' AND '{data.to_date}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

#===================================================================================================
# Receipt details

@searchRouter.post('/print_bill')
async def print_bill(data:PrintBill):

    select = "a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.gst_flag, b.gst_type, b.discount_flag, b.discount_type, b.discount_position, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name, d.header1, d.on_off_flag1, d.header2, d.on_off_flag2, d.footer1, d.on_off_flag3, d.footer2, d.on_off_flag4"
    table_name = "td_item_sale a, td_receipt b, md_items c, md_header_footer d"
    where = f"a.receipt_no=b.receipt_no and b.comp_id=d.comp_id and a.trn_date=b.trn_date and a.item_id=c.id and a.receipt_no={data.recp_no}"
    order = ""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    
    return res_dt

# =========================================================================================================
# Search Bill by Receipt

# @searchRouter.post('/search_by_receipt')
# async def search_by_receipt(data:SearchByReceipt):

#     select = "receipt_no,trn_date,created_by,net_amt,pay_mode"
#     table_name = "td_receipt"
#     where = f"comp_id = {data.comp_id} AND receipt_no = {data.receipt_no}"
#     order = f""
#     flag = 1
#     res_dt = await db_select(select,table_name,where,order,flag)
    
#     return res_dt