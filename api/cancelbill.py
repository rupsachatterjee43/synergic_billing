from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import CancelBill
# from models.otp_model import generateOTP
from datetime import datetime

# testing git
cancelRouter = APIRouter()

@cancelRouter.post('/api/cancel_bill_two')
async def cancel_bill_two(del_bill: CancelBill):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()

    query = f"SELECT * FROM td_receipt WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"

    cursor.execute(query)
    record = cursor.fetchall()
    conn.close()
    cursor.close()
    print(record)

    if record:
        rec = list(record)
        rec.append(del_bill.user_id)
        rec.append(current_datetime)
        conn = connect()
        cursor = conn.cursor()

        query1 = """INSERT INTO td_receipt_cancel_new (receipt_no, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, gst_flag, discount_type, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(query1, tuple(rec))
        conn.commit()

        if cursor.rowcount > 0:
            conn = connect()
            cursor = conn.cursor()
            query2 = f"SELECT * FROM td_item_sale WHERE receipt_no={del_bill.receipt_no} AND created_by='{del_bill.user_id}'"
            cursor.execute(query2)
            records = cursor.fetchall()

            if records:
                conn = connect()
                cursor = conn.cursor()
                for rec1 in records:
                    conn = connect()
                    cursor = conn.cursor()
                    query3 = """INSERT INTO td_item_sale_cancel (receipt_no, comp_id, br_id, item_id, trn_date, price, dis_pertg, discount_amt, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, created_by, created_dt, modified_by, modified_dt, cancelled_by, cancelled_dt) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query3, rec1)
                    conn.commit()

                query4 = f"""UPDATE td_stock JOIN td_item_sale ON td_stock.comp_id=td_item_sale.comp_id AND td_stock.br_id=td_item_sale.br_id JOIN td_receipt ON td_item_sale.receipt_no=td_receipt.receipt_no 
                            SET td_stock.stock=td_stock.stock+td_item_sale.qty, td_stock.modified_by='{del_bill.user_id}', td_stock.modified_dt='{current_datetime}' 
                            WHERE td_stock.item_id=td_item_sale.item_id AND td_receipt.receipt_no={del_bill.receipt_no}"""
                cursor.execute(query4)
                conn.commit()
                resData = {"status": 1, "data": "Bill cancelled and Stock added Successfully"}
            else:
                resData = {"status": -3, "data": "Error while inserting into cancel item table"}
        else:
            resData = {"status": -2, "data": "Error while inserting into cancel bill table"}
    else:
        resData = {"status": -1, "data": "Error while selecting bills"}

    cursor.close()
    conn.close()

    return resData