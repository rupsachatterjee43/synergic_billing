from fastapi import APIRouter
from config.database import connect
import mysql.connector
from models.master_model import createResponse
from models.form_model import CalReceipt,SaleReport
from datetime import datetime

CalRouter = APIRouter()

# =========================================================================================================

@CalRouter.post('/calculator/saleinsert')
async def calculator(rcpt:list[CalReceipt]):

    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    curr_date = current_datetime.strftime("%Y-%m-%d")
    values = []
    conn1 = connect()
    cursor1 = conn1.cursor()
    query1 = f"select count(*) last_rows from td_item_sale where comp_id={rcpt[0].comp_id}"
    cursor1.execute(query1)
    records = cursor1.fetchall()
    result = createResponse(records, cursor1.column_names, 1)
    conn1.close()
    cursor1.close()
    item_id = 0
    if cursor1.rowcount>0:
        lastid = result[0]["last_rows"]
        for i in rcpt:
            conn = connect()
            cursor = conn.cursor()
            values.append((receipt, i.comp_id, i.br_id, formatted_datetime, i.price, i.qty))
            lastid += 1

            query = f"INSERT INTO td_item_sale (receipt_no, comp_id, br_id, item_id, trn_date, price, qty, created_by, created_dt) VALUES ('{receipt}',{i.comp_id},{i.br_id},{lastid},'{curr_date}',{i.price}, {i.qty}, '{i.created_by}', '{formatted_datetime}')"

            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            if cursor.rowcount>0:
                resData = {"status":1, "data":receipt}
            else:
                resData = {"status":0, "data":'error while inserting'}
        
        conn = connect()
        cursor = conn.cursor()
        print(rcpt[0],"tttttttttttttttt")
        
        query = f"INSERT INTO td_receipt (receipt_no, comp_id, br_id, trn_date, price, amount, round_off, net_amt, received_amt, created_by, created_dt) VALUES ('{receipt}', {rcpt[0].comp_id}, {rcpt[0].br_id},'{curr_date}',{rcpt[0].tprice},{rcpt[0].tprice},{rcpt[0].round_off},{rcpt[0].net_amt},{rcpt[0].tprice},'{rcpt[0].created_by}','{formatted_datetime}')"

        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()
        
        if cursor.rowcount>0:
            ResData = {"status":1, "data":resData}
        else:
            ResData = {"status":0, "data":"Data not inserted"}
    
    return ResData


@CalRouter.get('/calculator/show_bill')
async def show_bill(recp_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no, a.comp_id, a.br_id,a.trn_date, a.price,a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice,b.round_off, b.net_amt, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt FROM td_item_sale a, td_receipt b WHERE a.receipt_no=b.receipt_no and a.trn_date=b.trn_date and a.receipt_no={recp_no}"
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

# =========================================================================================================
# Sale Report

@CalRouter.post('/calculator/sale_report')
async def sale_report(sl_rep:SaleReport):
    conn = connect()
    cursor = conn.cursor()

    query=f"select a.receipt_no, a.trn_date,  count(b.receipt_no)no_of_items, a.price, a.round_off, a.net_amt, a.created_by from  td_receipt a,td_item_sale b where a.receipt_no = b.receipt_no  and   a.trn_date between '{sl_rep.from_date}' and '{sl_rep.to_date}' and   b.comp_id = {sl_rep.comp_id} AND   b.br_id = {sl_rep.br_id} group by a.receipt_no, a.trn_date, a.price, a.round_off, a.net_amt, a.created_by Order by a.trn_date,a.receipt_no"

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
