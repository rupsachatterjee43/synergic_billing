from fastapi import APIRouter
from config.database import connect

import mysql.connector

from models.master_model import createResponse
from models.form_model import Receipt,SearchBill
from datetime import datetime

# testing git
tnxRouter = APIRouter()

# Item Sale
#---------------------------------------------------------------------------------------------------------------------------
@tnxRouter.post('/saleinsert')
async def register(rcpt:list[Receipt]):
    # return rcpt
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    curr_date = current_datetime.strftime("%Y-%m-%d")
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
        if cursor.rowcount>0:
            if i.stock_flag=='Y':
                conn = connect()
                cursor = conn.cursor()

                query = f"UPDATE td_stock SET stock=stock-{i.qty}, modified_by='{i.created_by}', modified_dt='{formatted_datetime}' WHERE comp_id={i.comp_id} AND br_id={i.br_id} AND item_id={i.item_id}"

                cursor.execute(query)
                conn.commit()
                conn.close()
                cursor.close()
                if cursor.rowcount==1:
                    resData = {"status":1, "data":receipt}
                else:
                    resData = {"status":0, "data":'error while updating stock'}
            else:
                resData = {"status":1, "data":receipt}
        else:
            resData = {"status":-1, "data":"Data not inserted in item_sale"}
    
    conn = connect()
    cursor = conn.cursor()
    print(rcpt[0],"tttttttttttttttt")
    phn_no1 = f",'{rcpt[0].phone_no}'" if rcpt[0].phone_no != "" else ",'0000000000'"
    query = f"INSERT INTO td_receipt (receipt_no, comp_id, br_id, trn_date, price, discount_amt, cgst_amt, sgst_amt, amount, round_off, net_amt, pay_mode, received_amt, pay_dtls, cust_name, phone_no, rcv_cash_flag, gst_flag, gst_type, discount_flag, discount_type, discount_position, created_by, created_dt) VALUES ('{receipt}', {rcpt[0].comp_id}, {rcpt[0].br_id},'{formatted_datetime}',{rcpt[0].tprice},{rcpt[0].tdiscount_amt},{tcgst_amt},{tsgst_amt},{rcpt[0].amount},{rcpt[0].round_off},{rcpt[0].net_amt},'{rcpt[0].pay_mode}','{rcpt[0].received_amt}','{rcpt[0].pay_dtls}','{rcpt[0].cust_name}' {phn_no1},'{rcpt[0].rcv_cash_flag}','{rcpt[0].gst_flag}', '{rcpt[0].gst_type}','{rcpt[0].discount_flag}','{rcpt[0].discount_type}','{rcpt[0].discount_position}','{rcpt[0].created_by}','{formatted_datetime}')"
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    # print(rcpt[0].pay_mode,"tttttttttt")
    if cursor.rowcount==1:
        try:
            if rcpt[0].kot_flag == 'Y':
                conn = connect()
                cursor = conn.cursor()
                query = f"SELECT ifnull(max(kot_no),0)+1 kot_no FROM td_kot where date(kot_date) = '{curr_date}'"
                cursor.execute(query)
                records = cursor.fetchall()
                result = createResponse(records, cursor.column_names, 1)
                conn.close()
                cursor.close()
                if cursor.rowcount>0:
                    conn = connect()
                    cursor = conn.cursor()
                    query = f"INSERT INTO td_kot (kot_no,kot_date,receipt_no,table_no) VALUES ({result[0]['kot_no']},'{formatted_datetime}','{receipt}',{rcpt[0].table_no})"
                    cursor.execute(query)
                    conn.commit()
                    conn.close()
                    cursor.close()
                    if cursor.rowcount>0:
                        ResData = {"status":1, "data":resData, "kot_no":result[0]}
                    else:
                        ResData = {"status":1, "data":"Data not inserted in kot table"}

                else:
                    ResData = {"status":1, "data":"Error While generating kot no."}

            else:
                ResData = {"status":1, "data":resData}
        except:
            print("!!!!!!!!!!Error in kot!!!!!!!!!!!!!")

# Inserting Data in td_recovery #
        try:
            # if rcpt[0].pay_mode == 'R':
            #     conn = connect()
            #     cursor = conn.cursor()
            #     query = f"INSERT INTO td_recovery (recover_dt,phone_no,paid_amt,due_amt,pay_mode,created_by,created_dt) VALUES ('{formatted_datetime}','{rcpt[0].phone_no}','{rcpt[0].received_amt}',{rcpt[0].net_amt-int(rcpt[0].received_amt)},'{rcpt[0].pay_mode}','{rcpt[0].created_by}','{formatted_datetime}')"
            #     cursor.execute(query)
            #     conn.commit()
            #     conn.close()
            #     cursor.close()
            #     if cursor.rowcount>0:
            #         ResData = {"status":1, "data":resData, "msg":"recovery data inserted successfully"}
            #     else:
            #         ResData = {"status":1, "data":"Data not inserted in recovery table"}

            if rcpt[0].pay_mode == 'R':
                conn = connect()
                cursor = conn.cursor()
                query = f"SELECT curr_due_amt FROM td_recovery_new where comp_id = {rcpt[0].comp_id} AND br_id = {rcpt[0].br_id} AND phone_no = '{rcpt[0].phone_no}' ORDER BY recover_id DESC LIMIT 1"
                cursor.execute(query)
                records = cursor.fetchall()
                recov_dt = createResponse(records, cursor.column_names, 1)
                conn.close()
                cursor.close()

                curr_due_amt = recov_dt[0]['curr_due_amt'] if(cursor.rowcount>0) else 0

                curr_due_amt += rcpt[0].net_amt

                conn = connect()
                cursor = conn.cursor()
                query = f"INSERT INTO td_recovery_new (comp_id,br_id,recover_dt,receipt_no,phone_no,paid_amt,due_amt,curr_due_amt,pay_mode,created_by,created_dt) VALUES ({rcpt[0].comp_id}, {rcpt[0].br_id},'{formatted_datetime}', {receipt},'{rcpt[0].phone_no}',0,{rcpt[0].net_amt}, {curr_due_amt},'{rcpt[0].pay_mode}','{rcpt[0].created_by}','{formatted_datetime}')"
                cursor.execute(query)
                conn.commit()
                conn.close()
                cursor.close()
                if cursor.rowcount>0:
                    if int(rcpt[0].received_amt) > 0:
                        curr_due_amt -= int(rcpt[0].received_amt)

                        conn = connect()
                        cursor = conn.cursor()
                        query = f"INSERT INTO td_recovery_new (comp_id,br_id,recover_dt,receipt_no,phone_no,paid_amt,due_amt,curr_due_amt,pay_mode,created_by,created_dt) VALUES ({rcpt[0].comp_id}, {rcpt[0].br_id},'{formatted_datetime}', {receipt},'{rcpt[0].phone_no}',{rcpt[0].received_amt},0,{curr_due_amt},'{rcpt[0].pay_mode}','{rcpt[0].created_by}','{formatted_datetime}')"
                        cursor.execute(query)
                        conn.commit()
                        conn.close()
                        cursor.close()

                        if cursor.rowcount>0:
                            ResData = {"status":1, "data":resData, "msg":"recovery data inserted successfully"}
                        else:
                            ResData = {"status":1, "data":"Data not inserted in recovery table"}
                    else:
                        ResData = {"status":1, "data":resData, "msg":"recovery data inserted successfully"}
                else:
                    ResData = {"status":1, "data":"Data not inserted in recovery table"}

        except mysql.connector.Error as err:
            print("----------Error in recovery---------")
            print(err)

    else:
        ResData = {"status":0, "data":"Data not inserted"}
    

    if rcpt[0].cust_info_flag > 0:
        conn = connect()
        cursor = conn.cursor()
        query= f"update md_customer set cust_name = '{rcpt[0].cust_name}', pay_mode = '{rcpt[0].pay_mode}', modified_by = '{rcpt[0].created_by}', modified_dt = '{formatted_datetime}' where phone_no = '{rcpt[0].phone_no}' and comp_id = {rcpt[0].comp_id}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()

    else:
        conn = connect()
        cursor = conn.cursor()
        phn_no = f",'{rcpt[0].phone_no}'" if rcpt[0].phone_no != None else None
        query= f"insert into md_customer (comp_id,cust_name,phone_no,pay_mode,created_by,created_dt) values ({rcpt[0].comp_id},'{rcpt[0].cust_name}' {phn_no},'{rcpt[0].pay_mode}','{rcpt[0].created_by}','{formatted_datetime}')"
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close()

    print(values) 
    return ResData

#Select Bill
#------------------------------------------------------------------------------------------------------------
@tnxRouter.get('/show_bill/{recp_no}')
async def show_bill(recp_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.receipt_no, a.comp_id, a.br_id, a.item_id, a.trn_date, a.price, a.dis_pertg, a.discount_amt, a.cgst_prtg, a.cgst_amt, a.sgst_prtg, a.sgst_amt, a.qty, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.price AS tprice, b.discount_amt AS tdiscount_amt, b.cgst_amt AS tcgst_amt, b.sgst_amt AS tsgst_amt, b.amount, b.round_off, b.net_amt, b.pay_mode, b.received_amt, b.pay_dtls, b.cust_name, b.phone_no, b.rcv_cash_flag, b.gst_flag, b.gst_type, b.discount_flag, b.discount_type, b.discount_position, b.created_by AS tcreated_by, b.created_dt AS tcreated_dt, b.modified_by AS tmodified_by, b.modified_dt AS tmodified_dt, c.item_name FROM td_item_sale a, td_receipt b, md_items c WHERE a.receipt_no=b.receipt_no and a.trn_date=b.trn_date and a.item_id=c.id and a.receipt_no={recp_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        try:
            conn1 = connect()
            cursor1 = conn1.cursor()
            query1 = f"SELECT count(*)Count FROM td_receipt_cancel_new WHERE receipt_no = {recp_no}"
            cursor1.execute(query1)
            records1 = cursor1.fetchall()
            result1 = createResponse(records1, cursor1.column_names, 1)
            conn1.close()
            cursor1.close()
            print(result1[0]["Count"])
            if result1[0]["Count"]>0:
                resData = {"status":1,
                            "cancel_flag":"Y", 
                            "data":result}
            else:
                resData = {"status":1,
                            "cancel_flag":"N", 
                            "data":result}
            
        except:
            return "Error 1"

        # resData= {"status":1, 
        #           "data":result}
    else:
        resData= {
        "status":0,
        "cancel_flag":"N",
        "data":[]
        }
    return resData


#Search bills within a date range
#-------------------------------------------------------------------------------------------------------------
@tnxRouter.post('/search_bills')
async def search_bills(search:SearchBill):
    conn = connect()
    cursor = conn.cursor()
    # query = f"SELECT a.* FROM td_receipt a, md_user b, md_branch c, md_company d WHERE a.created_by=b.user_id and b.br_id=c.id and b.comp_id=d.id and d.id={search.comp_id} and c.id={search.br_id} and a.created_by='{search.user_id}' and a.trn_date BETWEEN '{search.from_date}' AND '{search.to_date}'"
    query = f"SELECT * FROM td_receipt WHERE comp_id={search.comp_id} and br_id={search.br_id} and created_by='{search.user_id}' and trn_date BETWEEN '{search.from_date}' AND '{search.to_date}' and receipt_no not in (select receipt_no from td_receipt_cancel_new)"
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
