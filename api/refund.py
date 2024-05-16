from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import RefundItem,RefundList
# from models.otp_model import generateOTP
from datetime import datetime
# testing git
refRouter = APIRouter()

#refund item
#--------------------------------------------------------------------------------------------------------------------------
@refRouter.post('/refund_item')
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
    
    query = f"INSERT INTO td_refund_bill (receipt_no, refund_dt, refund_rcpt_no, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, cust_name, phone_no, gst_flag, gst_type, discount_flag, discount_type, discount_position, refund_by, refund_at) VALUES ({refund[0].receipt_no},'{formatted_datetime}','{receipt}',{refund[0].tprice},{refund[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{refund[0].tot_refund_amt},{refund[0].round_off},{refund[0].net_amt},'{refund[0].pay_mode}','{refund[0].received_amt}','{refund[0].cust_name}','{refund[0].phone_no}','{refund[0].gst_flag}','{refund[0].gst_type}','{refund[0].discount_flag}','{refund[0].discount_type}','{refund[0].discount_position}','{refund[0].user_id}','{formatted_datetime}')"
    # print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        ResData = {"status":1, "data":resData}
    else:
        ResData = {"status":0, "data":"Data not inserted"}
   
    return ResData

#======================================================================================================
@refRouter.post('/refund_list')
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