from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import RecoverBill,RecoveryUpdate
from datetime import datetime

# testing git
recoRouter = APIRouter()

# Recovery Amount
#==================================================================================================
@recoRouter.post('/recovery_amount')
async def recovery_amount(bill:RecoverBill):
    conn = connect()
    cursor = conn.cursor()

    query = f"SELECT receipt_no, trn_date, net_amt, received_amt, net_amt-received_amt due_amt FROM td_receipt WHERE pay_mode='R' AND net_amt-received_amt > 0 AND comp_id = {bill.comp_id} AND br_id = {bill.br_id} AND phone_no = '{bill.phone_no}'"

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

# Update td_receipt and Insert recovery_bill
#=================================================================================================
@recoRouter.post('/recovery_update')
async def recovery_update(recover:RecoveryUpdate):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = connect()
        cursor = conn.cursor()
    
        query = f"SELECT net_amt FROM td_receipt WHERE receipt_no={recover.receipt_no} and pay_mode='R'"

        cursor.execute(query)
        records = cursor.fetchall()
        res = createResponse(records, cursor.column_names, 1)
        conn.close()
        cursor.close()
        # print(res[0]['net_amt'])
        if cursor.rowcount>0:
        
            try:
                conn = connect()
                cursor = conn.cursor()

                query = f"INSERT INTO td_recovery (recover_id,recover_dt,receipt_no,net_amt,received_amt,pay_mode,created_by,created_dt) VALUES ({receipt},'{formatted_dt}',{recover.receipt_no},'{res[0]['net_amt']}',{recover.received_amt},'{recover.pay_mode}','{recover.user_id}','{formatted_dt}')"

                cursor.execute(query)
                conn.commit()
                conn.close()
                cursor.close()
                if cursor.rowcount>0:

                    try:
                        conn = connect()
                        cursor = conn.cursor()

                        query = f"UPDATE td_receipt SET received_amt = received_amt+{recover.received_amt}, modified_by = '{recover.user_id}', modified_dt = '{formatted_dt}' WHERE receipt_no = {recover.receipt_no}"

                        cursor.execute(query)
                        conn.commit()
                        conn.close()
                        cursor.close()
                        if cursor.rowcount>0:
                            resData = {"status":1, "recover_id":receipt, "msg":"data inserted and updated successfully"}
                        else:
                            resData = {"status":0, "data":'error while updating td_receipt'}
                    except:
                        print("********* Error while updating ************")
            
                else:
                    resData = {"status":-1, "data":"Data not inserted in td_recovery"}
            except:
                print("<<<<<<<<<<<<< Error while inserting >>>>>>>>>>>>>>")
        else:
            resData = {"status":-2, "data":"Data not selected"}

    except:
        print("------------- Error while selecting ---------------")
    
    return resData