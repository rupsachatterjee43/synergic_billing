from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,CustomerId,AddEditCustomer
from datetime import datetime

customerRouter = APIRouter()
# ==================================================================================================
# Customer List of All customers

@customerRouter.post('/all_customer_list')
async def all_customer_list(data:CompId):
    select = "*"
    table_name = "md_customer"
    where = f"(cust_name != '' OR phone_no != '') AND comp_id = {data.comp_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ========================================================================================================
# Details of a Perticular Customer

@customerRouter.post('/customer_list')
async def customer_list(data:CustomerId):
    select = "*"
    table_name = "md_customer"
    where = f"comp_id = {data.comp_id} and cust_id = {data.cust_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Add And Edit Customer Details

@customerRouter.post('/add_edit_customer')
async def add_edit_customer(data:AddEditCustomer):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    if ({data.cust_id}.pop())>0:

        table_name = "md_customer"
        fields = f"cust_name = '{data.cust_name}', phone_no = '{data.phone_no}', bill_address = '{data.bill_address}', delivery_address = '{data.delivery_address}', email_id = '{data.email_id}', pay_mode = '{data.pay_mode}', date_of_birth = '{data.date_of_birth}', gender = '{data.gender}', modified_by = 'Admin', modified_dt = '{formatted_dt}'"
        values = None
        where = f"comp_id={data.comp_id} and cust_id={data.cust_id}"
        flag = 1
        res_dt = await db_Insert(table_name,fields,values,where,flag)
    else:
        table_name = "md_customer"
        fields = "comp_id, cust_name, phone_no, bill_address, delivery_address, email_id, pay_mode, date_of_birth, gender, created_by, created_dt"
        values =f"{data.comp_id}, '{data.cust_name}', '{data.phone_no}', '{data.bill_address}', '{data.delivery_address}', '{data.email_id}', '{data.pay_mode}', '{data.date_of_birth}', '{data.gender}', 'Admin', '{formatted_dt}'"
        where = None
        flag = 0
        res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt


# @customerRouter.post('/add_edit_customer')
# async def add_edit_customer(data:AddEditCustomer):

#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     table_name = "md_customer"
#     fields = f"cust_name = '{data.cust_name}', phone_no = '{data.phone_no}', bill_address = '{data.bill_address}', delivery_address = '{data.delivery_address}', email_id = '{data.email_id}', pay_mode = '{data.pay_mode}', date_of_birth = '{data.date_of_birth}', gender = '{data.gender}', modified_by = 'Admin', modified_dt = '{formatted_dt}'" if data.cust_id > 0 else f"comp_id, cust_name, phone_no, bill_address, delivery_address, email_id, pay_mode, date_of_birth, gender, created_by, created_dt"
#     values = None if data.cust_id>0 else f"{data.comp_id}, '{data.cust_name}', '{data.phone_no}', '{data.bill_address}', '{data.delivery_address}', '{data.email_id}', '{data.pay_mode}', '{data.date_of_birth}', '{data.gender}', 'Admin', '{formatted_dt}'"
#     where = f"comp_id={data.comp_id} and cust_id={data.cust_id}" if data.cust_id>0 else None
#     flag = 1 if data.cust_id>0 else 0
#     res_dt = await db_Insert(table_name,fields,values,where,flag)

#     return res_dt

# ============================================================================================================