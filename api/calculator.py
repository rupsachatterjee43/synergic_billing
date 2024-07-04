from fastapi import APIRouter
from config.database import connect
import mysql.connector
from models.master_model import createResponse
from models.form_model import CalReceipt
from datetime import datetime

CalRouter = APIRouter()

# =========================================================================================================

@CalRouter.post('/calculator/saleinsert')
async def calculator(rcpt:list[CalReceipt]):
    # return rcpt
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    curr_date = current_datetime.strftime("%Y-%m-%d")
    values = []
    print(rcpt)
    for i in rcpt:
        print(len(i),"+++++++")
        conn = connect()
        cursor = conn.cursor()
        print(cursor.lastrowid)
        values.append((receipt, i.comp_id, i.br_id, formatted_datetime, i.price, i.qty))
        # item_id = f"cursor.lastrowid" if cursor.lastrowid != None else f"0"
        # item_id = int(item_id)+ int(cursor.rowcount)
        # print(item_id,'YYYYYYYYYYY')

        # query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, trn_date, price, qty, created_by, created_dt) VALUES ('{receipt}',{i.comp_id},{i.br_id},{item_id},'{curr_date}',{i.price}, {i.qty}, '{i.created_by}', '{formatted_datetime}')"

        # cursor.execute(query)
        # print(cursor.lastrowid,'>>>>>>>>>>><<<<<<<<<<')
        # conn.commit()
        # conn.close()
        # cursor.close()
        # if cursor.rowcount>0:
        #     resData = {"status":1, "data":receipt}
        # else:
        #     resData = {"status":0, "data":'error while inserting'}

    # return resData
    
    # conn = connect()
    # cursor = conn.cursor()
    # print(rcpt[0],"tttttttttttttttt")
    # # phn_no1 = f",'{rcpt[0].phone_no}'" if rcpt[0].phone_no != "" else ",'0000000000'"
    # query = f"INSERT INTO td_receipt (receipt_no, comp_id, br_id, trn_date, price, amount, round_off, net_amt, received_amt, created_by, created_dt) VALUES ('{receipt}', {rcpt[0].comp_id}, {rcpt[0].br_id},'{curr_date}',{rcpt[0].tprice},{rcpt[0].tprice},{rcpt[0].round_off},{rcpt[0].net_amt},{rcpt[0].tprice},'{rcpt[0].created_by}','{formatted_datetime}')"
    # print(query)
    # cursor.execute(query)
    # conn.commit()
    # conn.close()
    # cursor.close()
    # # print(rcpt[0].pay_mode,"tttttttttt")
    # if cursor.rowcount==1:
    #     ResData = {"status":1, "data":resData}
    # else:
    #     ResData = {"status":0, "data":"Data not inserted"}
    
    # return ResData