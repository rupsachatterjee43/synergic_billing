from fastapi import APIRouter, File, UploadFile, Depends, Form
import pathlib
import mysql.connector
from pathlib import Path
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import AddEditLocation,AddEditCompany,AddEditUser,AddEditOutletS,OneOutlet,AddHeaderFooter,AddEditSettings,AddEditUnit,Excel,EditItemDtls,Item
from utils import get_hashed_password,verify_password
from datetime import datetime
from typing import Annotated, Union, Optional
from io import BytesIO
import os
from pandas import read_excel
# import openpyxl



# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))
# df = pd.read_excel('/home/rupsa/Documents/Data.xlsx')
# print(df)

UPLOAD_FOLDER = "upload_file"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

superadminRouter = APIRouter()

# ======================================================================================================
# Check Superadmin
@superadminRouter.get('/S_Admin/user_type')
async def select_location(user_id:str):
    select = "user_type"
    table_name = "md_user"
    where = f"user_id = '{user_id}'"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# Manage Location
# ========================================================================================================
#-----------Select Location List---------------------

@superadminRouter.get('/S_Admin/select_location')
async def select_location():
    select = "sl_no,location_name"
    table_name = "md_location"
    where = f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ---------------Add And Edit Location-----------------

@superadminRouter.post('/S_Admin/add_edit_location')
async def add_edit_location(data:AddEditLocation):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_location"
    fields = f"location_name='{data.location_name}', modified_by='{data.user_id}', modified_at='{formatted_dt}'" if data.sl_no>0 else f"location_name, created_by, created_at"
    values = None if data.sl_no>0 else f"'{data.location_name}', '{data.user_id}', '{formatted_dt}'"
    where = f"sl_no = {data.sl_no}" if data.sl_no>0 else None
    order = ""
    flag = 1 if data.sl_no>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# =====================================================================================================
# Manage Shop(Company)

# -------------------Select Company-----------------
@superadminRouter.get('/S_Admin/select_shop')
async def select_shop(id:int):
    select = "id,company_name,mode,address,location,contact_person,phone_no,email_id,web_portal,active_flag,max_user"
    table_name = "md_company"
    where = f"id={id}" if id>0 else f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# -------------------Add And Edit Shop-----------------
@superadminRouter.post('/S_Admin/add_edit_shop')
async def add_edit_shop(data:AddEditCompany):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_company"
    fields = f"company_name='{data.company_name}', mode='{data.mode}', address='{data.address}', location={data.location}, contact_person='{data.contact_person}', phone_no={data.phone_no}, email_id='{data.email_id}',web_portal='{data.web_portal}',active_flag='{data.active_flag}',max_user={data.max_user},modified_by='{data.user_id}', modified_dt='{formatted_dt}'" if data.id>0 else f"company_name,address,location,contact_person,phone_no,email_id,web_portal,active_flag,max_user,created_by, created_dt"
    values = None if data.id>0 else f"'{data.company_name}','{data.address}',{data.location},'{data.contact_person}',{data.phone_no},'{data.email_id}','{data.web_portal}','{data.active_flag}',{data.max_user},'{data.user_id}', '{formatted_dt}'"
    where = f"id = {data.id}" if data.id>0 else None
    order = ""
    flag = 1 if data.id>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    print(res_dt["lastId"],"22222222")
    return res_dt

# =======================================================================================================
# Manage User

# --------------Select All Users-------------
@superadminRouter.get('/S_Admin/select_user')
async def select_user(id:int):
    select = "id,comp_id,br_id,user_name,user_type,user_id,phone_no,email_id,active_flag,login_flag"
    table_name = "md_user"
    where = f"id={id}" if id>0 else f""
    order = f"ORDER BY comp_id,br_id,user_type"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.get('/S_Admin/select_user_by_shop')
async def select_user(comp_id:int,br_id:int):
    select = "id,comp_id,br_id,user_name,user_type,user_id,phone_no,email_id,active_flag,login_flag"
    table_name = "md_user"
    where = f"comp_id={comp_id} and br_id={br_id}"
    order = f"ORDER BY user_type"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ---------------Add And Edit User---------------
@superadminRouter.post('/S_Admin/add_edit_user')
async def add_edit_user(data:AddEditUser):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    pwd = get_hashed_password(data.password)

    table_name = f"md_user"

    # fields = f"comp_id={data.comp_id}, br_id={data.br_id}, user_name='{data.user_name}', user_type='{data.user_type}', user_id='{data.user_id}', phone_no={data.phone_no}, email_id='{data.email_id}', device_id='0',password='{pwd}',active_flag='{data.active_flag}',login_flag='{data.login_flag}',modified_by='{data.created_by}', modified_dt='{formatted_dt}'" if data.id>0 else f"comp_id,br_id,user_name,user_type,user_id,phone_no,email_id,device_id,password,active_flag,login_flag,created_by, created_dt"
    # values = None if data.id>0 else f"{data.comp_id},{data.br_id},'{data.user_name}','{data.user_type}','{data.user_id}',{data.phone_no},'{data.email_id}','0','{pwd}','{data.active_flag}','{data.login_flag}','{data.created_by}', '{formatted_dt}'"

    if data.user_type == 'A':

        fields = f"comp_id={data.comp_id}, br_id={data.br_id}, user_name='{data.user_name}', user_type='{data.user_type}', user_id='{data.user_id}', email_id='{data.user_id}', device_id='0', password='{pwd}',active_flag='{data.active_flag}',login_flag='{data.login_flag}',modified_by='{data.created_by}', modified_dt='{formatted_dt}'" if data.id>0 else f"comp_id,br_id,user_name,user_type,user_id,email_id,device_id,password,active_flag,login_flag,created_by, created_dt"

        values = None if data.id>0 else f"{data.comp_id},{data.br_id},'{data.user_name}','{data.user_type}','{data.user_id}','{data.user_id}','0','{pwd}','Y','N','{data.created_by}', '{formatted_dt}'"

    else:

        fields = f"comp_id={data.comp_id}, br_id={data.br_id}, user_name='{data.user_name}', user_type='{data.user_type}', user_id='{data.user_id}', phone_no='{data.user_id}', device_id='0', active_flag='{data.active_flag}',login_flag='{data.login_flag}',modified_by='{data.created_by}', modified_dt='{formatted_dt}'" if data.id>0 else f"comp_id,br_id,user_name,user_type,user_id,phone_no,device_id,active_flag,login_flag,created_by, created_dt"

        values = None if data.id>0 else f"{data.comp_id},{data.br_id},'{data.user_name}','{data.user_type}','{data.user_id}','{data.user_id}','0','Y','N','{data.created_by}', '{formatted_dt}'"

    where = f"id = {data.id}" if data.id>0 else None
    order = ""
    flag = 1 if data.id>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# =========================================================================================================
# Manage Outlet

# ----------------company wise branch select-----------------
@superadminRouter.get('/S_Admin/select_outlet')
async def select_outlet(comp_id:int):
    select = "id,comp_id,branch_name,branch_address,location,contact_person,phone_no,email_id"
    table_name = "md_branch"
    where = f"comp_id={comp_id}" if comp_id>0 else f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# @superadminRouter.post('/S_Admin/select_one_outlet')
# async def select_outlet(data:OneOutlet):
#     select = "id,comp_id,branch_name,branch_address,location,contact_person,phone_no,email_id"
#     table_name = "md_branch"
#     where = f"comp_id={data.comp_id} AND id = {data.br_id}" 
#     order = f""
#     flag = 1
#     res_dt = await db_select(select,table_name,where,order,flag)
#     return res_dt

@superadminRouter.get('/S_Admin/select_one_outlet')
async def select_outlet(comp_id:int,br_id:int):
    select = "id,comp_id,branch_name,branch_address,location,contact_person,phone_no,email_id"
    table_name = "md_branch"
    where = f"comp_id={comp_id} AND id = {br_id}" 
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.post('/S_Admin/add_edit_outlet')
async def add__edit_outlet(data:AddEditOutletS):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_branch"

    fields = f"branch_name = '{data.branch_name}', branch_address = '{data.branch_address}', location = {data.location}, contact_person = '{data.contact_person}', phone_no = {data.phone_no}, email_id = '{data.email_id}', modified_by = '{data.created_by}', modified_dt = '{formatted_dt}'" if data.br_id>0 else "comp_id, branch_name, branch_address, location, contact_person, phone_no, email_id, created_by, created_dt"    

    values =f"{data.comp_id}, '{data.branch_name}', '{data.branch_address}', {data.location}, '{data.contact_person}', {data.phone_no}, '{data.email_id}', '{data.created_by}', '{formatted_dt}'"

    where = f"comp_id={data.comp_id} and id={data.br_id}" if data.br_id>0 else None 

    flag = 1 if data.br_id>0 else 0

    res_dt = await db_Insert(table_name,fields,values,where,flag)

    return res_dt

# =======================================================================================================
# Manage Header-Footer

@superadminRouter.get('/S_Admin/select_header_footer')
async def select_header_footer(comp_id:int):
    select = "a.comp_id,b.company_name,a.header1,a.on_off_flag1,a.header2,a.on_off_flag2,a.footer1,a.on_off_flag3,a.footer2,a.on_off_flag4"
    table_name = "md_header_footer a, md_company b"
    where = f"a.comp_id = b.id and a.comp_id={comp_id}" if comp_id>0 else f"a.comp_id=b.id"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    # print(res_dt["msg"],"yyyyyyy")
    return res_dt

@superadminRouter.post('/S_Admin/add_edit_header_footer')
async def add_edit_header_footer(data:AddHeaderFooter):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    select = "comp_id,header1,on_off_flag1,header2,on_off_flag2,footer1,on_off_flag3,footer2,on_off_flag4"
    table_name = "md_header_footer"
    where = f"comp_id={data.comp_id}"
    order = f""
    flag = 1
    res_dt1 = await db_select(select,table_name,where,order,flag)
    if res_dt1["suc"] == 1:
        table_name = f"md_header_footer"
        fields = f"comp_id,header1,on_off_flag1,header2,on_off_flag2,footer1,on_off_flag3,footer2,on_off_flag4,created_by, created_at" if res_dt1["msg"] == [] else f"header1='{data.header1}',on_off_flag1='{data.on_off_flag1}',header2='{data.header2}',on_off_flag2='{data.on_off_flag2}',footer1='{data.footer1}',on_off_flag3='{data.on_off_flag3}',footer2='{data.footer2}',on_off_flag4='{data.on_off_flag4}',modified_by='{data.created_by}', modified_at='{formatted_dt}'"
        values = f"{data.comp_id},'{data.header1}','{data.on_off_flag1}','{data.header2}','{data.on_off_flag2}','{data.footer1}','{data.on_off_flag3}','{data.footer2}','{data.on_off_flag4}','{data.created_by}', '{formatted_dt}'" if res_dt1["msg"] == [] else None
        where = None if res_dt1["msg"] == [] else f"comp_id = {data.comp_id}"
        order = f""
        flag = 0 if res_dt1["msg"] == [] else 1
        res_dt = await db_Insert(table_name,fields,values,where,flag)
        return res_dt
    else:
        return res_dt1

# =======================================================================================================
# Manage Settings

@superadminRouter.get('/S_Admin/select_settings')
async def select_settings(comp_id:int):
    select = "a.comp_id,b.company_name,a.rcv_cash_flag,a.rcpt_type,a.gst_flag,a.gst_type,a.unit_flag,a.cust_inf,a.pay_mode,a.discount_flag,a.stock_flag,a.discount_type,a.discount_position,a.price_type,a.refund_days,a.kot_flag"
    table_name = "md_receipt_settings a, md_company b"
    where = f"a.comp_id=b.id and a.comp_id={comp_id}" if comp_id>0 else f"a.comp_id=b.id"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.post('/S_Admin/add_edit_settings')
async def add_edit_settings(data:AddEditSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    select = "comp_id,rcv_cash_flag,rcpt_type,gst_flag,gst_type,unit_flag,cust_inf,pay_mode,discount_flag,stock_flag,discount_type,discount_position,price_type,refund_days,kot_flag"
    table_name = "md_receipt_settings"
    where = f"comp_id={data.comp_id}"
    order = f""
    flag = 1
    res_dt1 = await db_select(select,table_name,where,order,flag)
    if res_dt1["suc"] == 1:
        table_name = f"md_receipt_settings"
        fields = f"comp_id,rcv_cash_flag,rcpt_type,gst_flag,gst_type,unit_flag,cust_inf,pay_mode,discount_flag,stock_flag,discount_type,discount_position,price_type,refund_days,kot_flag,created_by,created_at" if res_dt1["msg"] == [] else f"rcv_cash_flag='{data.rcv_cash_flag}',rcpt_type='{data.rcpt_type}',gst_flag='{data.gst_flag}',gst_type='{data.gst_type}',unit_flag='{data.unit_flag}',cust_inf='{data.cust_inf}',pay_mode='{data.pay_mode}',discount_flag='{data.discount_flag}',stock_flag='{data.stock_flag}',discount_type='{data.discount_type}',discount_position='{data.discount_position}',price_type='{data.price_type}',refund_days={data.refund_days},kot_flag='{data.kot_flag}',modified_by='{data.created_by}', modified_at='{formatted_dt}'"
        values = f"{data.comp_id},'{data.rcv_cash_flag}','{data.rcpt_type}','{data.gst_flag}','{data.gst_type}','{data.unit_flag}','{data.cust_inf}','{data.pay_mode}','{data.discount_flag}','{data.stock_flag}','{data.discount_type}','{data.discount_position}','{data.price_type}',{data.refund_days},'{data.kot_flag}','{data.created_by}','{formatted_dt}'" if res_dt1["msg"] == [] else None
        where = None if res_dt1["msg"] == [] else f"comp_id = {data.comp_id}"
        order = f""
        flag = 0 if res_dt1["msg"] == [] else 1
        res_dt = await db_Insert(table_name,fields,values,where,flag)
        return res_dt
    else:
        return res_dt1

# =======================================================================================================
# Manage Unit

@superadminRouter.get('/S_Admin/select_unit')
async def select_unit(comp_id:int,unit_id:int):
    select = "sl_no,comp_id,unit_name"
    table_name = "md_unit"
    where = f"comp_id={comp_id} AND sl_no={unit_id}" if comp_id>0 and unit_id>0 else f"comp_id={comp_id}" if comp_id>0 else f""
    order = "order by comp_id"
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.post('/S_Admin/add_edit_unit')
async def add_edit_unit(data:AddEditUnit):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_unit"
    fields = f"unit_name='{data.unit_name}',modified_by='{data.created_by}', modified_at='{formatted_dt}'" if data.sl_no>0 else f"comp_id,unit_name,created_by,created_at"
    values = None if data.sl_no>0 else f"{data.comp_id},'{data.unit_name}','{data.created_by}', '{formatted_dt}'"
    where = f"sl_no={data.sl_no} AND comp_id = {data.comp_id}" if data.sl_no>0 else None
    order = ""
    flag = 1 if data.sl_no>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt

# ====================================================================================================
# Manage Category

@superadminRouter.get('/S_Admin/select_category')
async def select_category(comp_id:int,catg_id:int):
    select = "sl_no,comp_id,category_name,catg_picture"
    table_name = "md_category"
    where = f"comp_id={comp_id} AND sl_no={catg_id}" if comp_id>0 and catg_id>0 else f"comp_id={comp_id}" if comp_id>0 else f""
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# Add or Edit Category

@superadminRouter.post('/S_Admin/add_edit_category')
async def add_edit_category(
    comp_id: str = Form(...),
    catg_id: str = Form(...),
    category_name: str = Form(...),
    created_by: str = Form(...),
    file: Optional[UploadFile] = File(None)
    ):
    print(file)
    fileName = None if not file else await uploadfile(file)
    print(fileName,"mmmmmmmmmm")
    # return {"body":data,"file":file}
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = "md_category"
    catg_pic = f", catg_picture = '/uploads/{fileName}'" if fileName != None else ''
    catg_pic1 = f",'/uploads/{fileName}'" if fileName != None else ', ""'
    fields = f"category_name ='{category_name}' {catg_pic}, modified_by = '{created_by}', modified_at = '{formatted_dt}'" if int(catg_id)>0 else "comp_id,category_name,catg_picture,created_by,created_at"
    values = f"{comp_id},'{category_name}' {catg_pic1}, '{created_by}','{formatted_dt}'"
    where = f"comp_id={comp_id} and sl_no={catg_id}" if int(catg_id) >0 else None
    flag = 1 if int(catg_id)>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt


async def uploadfile(file):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    modified_filename = f"{receipt}_{file.filename}"
    res = ""
    try:
        file_location = os.path.join(UPLOAD_FOLDER, modified_filename)
        print(file_location)
        
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        res = modified_filename
        print(res)
    except Exception as e:
        # res = e.args
        res = ""
    finally:
        return res

# Select Item Details by comp_id:
# ===========================================================================================================

@superadminRouter.get('/S_Admin/item_detail')
async def item_detail(comp_id:int):
    select = 'a.*, b.*'
    table_name = "md_items a, md_item_rate b"
    where = f"a.id=b.item_id AND a.comp_id = {comp_id}"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.get('/S_Admin/one_item_detail')
async def item_detail(comp_id:int,item_id:int):
    select = 'a.*, b.*'
    table_name = "md_items a, md_item_rate b"
    where = f"a.id=b.item_id AND a.id = {item_id} AND a.comp_id = {comp_id}"
    order = f""
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt


# @superadminRouter.post('/S_Admin/insert_excel')
# async def insert_excel(data:Excel):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     df = pd.read_excel(file.filename)
#     print(df)
#     for index, row in df.iterrows():
#         table_name = "md_items"
#         fields = "comp_id,catg_id,hsn_code,item_name,created_by,created_dt"
#         values =f"{data.comp_id},{data.catg_id},{row['hsn_code']},'{row['item_name']}', '{data.created_by}','{formatted_dt}'"
#         where = None
#         # print(data.unit_id)
#         order = f""
#         flag = 0
#         # print(row["item_name"])
#         res_dt = await db_Insert(table_name,fields,values,where,flag)
        
#         if res_dt["suc"]>0:
#             table_name = "md_item_rate"
#             fields = "item_id,price,discount,cgst,sgst,created_by,created_dt"
#             values =f"{res_dt['lastId']},{row['price']},{row['discount']},{row['cgst']},{row['sgst']},'{data.created_by}','{formatted_dt}'"
#             where = None
#             # print(data.unit_id)
#             order = f""
#             flag = 0
#             # print(row["item_name"])
#             res_dt2 = await db_Insert(table_name,fields,values,where,flag)
        
#     return res_dt2

# *************************************************************************************************************
@superadminRouter.post('/S_Admin/insert_item_excel')
async def insert_excel(
    comp_id: int = Form(...),
    # catg_id: int = Form(...),
    created_by: str = Form(...),
    file: UploadFile = File
):
    res_dt3 = []
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    contents = await file.read()
    df = read_excel(BytesIO(contents))
    # print(df,"==============")
    data = df.to_dict(orient="records")
    # return data
    # print(df)
    for row in data:
        table_name = "md_items"
        fields = "comp_id,hsn_code,item_name,created_by,created_dt"
        values =f"{comp_id},{row['hsn_code']},'{row['item_name']}', '{created_by}','{formatted_dt}'"
        where = None
        order = f""
        flag = 0
        res_dt = await db_Insert(table_name,fields,values,where,flag)
        
        if res_dt["suc"]>0:
            table_name = "md_item_rate"
            fields = "item_id,price,discount,cgst,sgst,created_by,created_dt"
            values =f"{res_dt['lastId']},{row['price']},{row['discount']},{row['cgst']},{row['sgst']},'{created_by}','{formatted_dt}'"
            where = None
            order = f""
            flag = 0
            res_dt1 = await db_Insert(table_name,fields,values,where,flag)
            if res_dt1["suc"] > 0:
                select = "id"
                table_name = "md_branch"
                where = f"comp_id = {comp_id}"
                order = f''
                flag = 1
                res_dt2 = await db_select(select,table_name,where,order,flag)
                print(res_dt2)
                if res_dt2["suc"]>0:
                    for i in res_dt2["msg"]:
                        
                        table_name2 = "td_stock"
                        fields2 = "comp_id, br_id, item_id, stock, created_by, created_dt"
                        values2 = f"{comp_id},{i['id']},{res_dt['lastId']},'0','{created_by}','{formatted_dt}'"
                        where2 = None
                        flag2 = 0
                        res_dt3= await db_Insert(table_name2,fields2,values2,where2,flag2)
        
    return res_dt3
# **************************************************************************************************************

# @superadminRouter.post('/S_Admin/insert_item_excel')
# async def insert_excel(
#     comp_id: int = Form(...),
#     # catg_id: int = Form(...),
#     created_by: str = Form(...),
#     file: UploadFile = File
# ):
#     res_dt3 = []
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     contents = await file.read()
#     df = read_excel(BytesIO(contents))
#     # print(df,"==============")
#     data = df.to_dict(orient="records")
#     # return data
#     # print(df)
#     for row in data:
#         table_name = "md_items"
#         fields = "comp_id,hsn_code,item_name,created_by,created_dt"
#         values =f"{comp_id},{row['hsn_code']},'{row['item_name']}', '{created_by}','{formatted_dt}'"
#         where = None
#         order = f""
#         flag = 0
#         res_dt = await db_Insert(table_name,fields,values,where,flag)
        
#         if res_dt["suc"]>0:
#             table_name = "md_item_rate"
#             fields = "item_id,price,discount,cgst,sgst,created_by,created_dt"
#             values =f"{res_dt['lastId']},{row['price']},{row['discount']},{row['cgst']},{row['sgst']},'{created_by}','{formatted_dt}'"
#             where = None
#             order = f""
#             flag = 0
#             res_dt1 = await db_Insert(table_name,fields,values,where,flag)
#             if res_dt1["suc"] > 0:
#                 select = "id"
#                 table_name = "md_branch"
#                 where = f"comp_id = {comp_id}"
#                 order = f''
#                 flag = 1
#                 res_dt2 = await db_select(select,table_name,where,order,flag)
#                 print(res_dt2)
#                 if res_dt2["suc"]>0:
#                     for i in res_dt2["msg"]:
                        
#                         table_name2 = "td_stock"
#                         fields2 = "comp_id, br_id, item_id, stock, created_by, created_dt"
#                         values2 = f"{comp_id},{i['id']},{res_dt['lastId']},{row['stock']},'{created_by}','{formatted_dt}'"
#                         where2 = None
#                         flag2 = 0
#                         res_dt3= await db_Insert(table_name2,fields2,values2,where2,flag2)

#                         if res_dt3["suc"]>0:
#                             table_name3 = "td_stock_in"
#                             fields3 = "comp_id, br_id, in_date, item_id, in_price, in_cgst, in_sgst, qty, created_by, created_at"
#                             values3 = f"{comp_id},{i['id']},date('{formatted_dt}'),{res_dt['lastId']},{row['price']},{row['cgst']},{row['sgst']},{row['stock']},'{created_by}','{formatted_dt}'"
#                             where3 = None
#                             flag3 = 0
#                             res_dt4= await db_Insert(table_name3,fields3,values3,where3,flag3)
                
        
#     return res_dt4
# ***************************************************************************************************************

@superadminRouter.post('/S_Admin/edit_item_dtls')
async def edit_item_dtls(data:EditItemDtls):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    table_name = "md_items"
    fields = f"item_name ='{data.item_name}', hsn_code = '{data.hsn_code}', catg_id = {data.catg_id}, unit_id = {data.unit_id}, bar_code = '{data.bar_code}', modified_by = '{data.created_by}', modified_dt = '{formatted_dt}'"
    values = None
    where = f"id = {data.item_id} and comp_id = {data.comp_id}"
    flag = 1
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    if res_dt["suc"] > 0:
        table_name2 = "md_item_rate"
        fields2 = f"price = {data.price},discount = {data.discount},cgst = {data.cgst},sgst = {data.sgst}, modified_by = '{data.created_by}', modified_dt = '{formatted_dt}'"
        values2 = None
        where2 = f"item_id = {data.item_id}"
        flag2 = 1
        res_dt2 = await db_Insert(table_name2,fields2,values2,where2,flag2)

    return res_dt2

@superadminRouter.get('/S_Admin/item_stock')
async def item_stock_dtls(comp_id:int,br_id:int):
    select = f"a.id item_id, a.item_name, b.stock"
    table_name = "md_items a, td_stock b"
    where = f"a.id=b.item_id and a.comp_id=b.comp_id and a.comp_id = {comp_id} and b.br_id = {br_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# @superadminRouter.post('/S_Admin/stock_in')
# async def stock_in(
#     comp_id: int = Form(...),
#     br_id: int = Form(...),
#     # catg_id: int = Form(...),
#     created_by: str = Form(...),
#     file: UploadFile = File
# ):
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     contents = await file.read()
#     df = read_excel(BytesIO(contents))
#     data = df.to_dict(orient="records")

#     for row in data:
#         print(row)
#         table_name = "td_stock"
#         fields = f"stock = stock+{row['stock']}, created_by='{created_by}', created_dt='{formatted_dt}'"
#         values = None
#         where = f"comp_id = {comp_id} and br_id = {br_id} and item_id = {row['item_id']}"
#         flag = 1
#         res_dt= await db_Insert(table_name,fields,values,where,flag)

#     return res_dt

@superadminRouter.post('/S_Admin/stock_in')
async def stock_in(
    comp_id: int = Form(...),
    br_id: int = Form(...),
    # catg_id: int = Form(...),
    created_by: str = Form(...),
    file: UploadFile = File
):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    contents = await file.read()
    df = read_excel(BytesIO(contents))
    data = df.to_dict(orient="records")
    res_dt3 = {}

    for row in data:
        select = f"price, cgst, sgst"
        table_name = "md_item_rate"
        where = f"item_id = {row['item_id']}"
        order = f''
        flag = 1
        res_dt = await db_select(select,table_name,where,order,flag)
       

        if res_dt['suc']>0:
        # print(row)
            table_name1 = "td_stock"
            fields1 = f"stock = stock+{row['stock']}, created_by='{created_by}', created_dt='{formatted_dt}'"
            values1 = None
            where1 = f"comp_id = {comp_id} and br_id = {br_id} and item_id = {row['item_id']}"
            flag1 = 1
            res_dt2= await db_Insert(table_name1,fields1,values1,where1,flag1)

            if res_dt2['suc']>0:
                try:
                    table_name2 = "td_stock_in"
                    fields2 = f"comp_id, br_id, in_date, item_id, in_price, in_cgst, in_sgst, qty"
                    values2 = f"{comp_id}, {br_id}, date('{formatted_dt}'), {row['item_id']}, {res_dt['msg'][0]['price']}, {res_dt['msg'][0]['cgst']}, {res_dt['msg'][0]['sgst']}, {row['stock']}"
                    where2 = None
                    flag2 = 0
                    res_dt3= await db_Insert(table_name2,fields2,values2,where2,flag2)
                except mysql.connector.Error as err:
                    print(err)
    return res_dt3

@superadminRouter.get('/S_Admin/catg_list')
async def catg_list(comp_id:int):
    select = f"sl_no catg_id,category_name"
    table_name = "md_category"
    where = f"comp_id = {comp_id}"
    order = f''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

@superadminRouter.post("/S_Admin/categorywise_items")
async def categorywise_items(data:Item):
    res_dt={}

    for nm in data.item_id:
        try: 
            table_name = "md_items"
            fields = f"catg_id={data.catg_id}"
            values = None
            where = f"comp_id={data.comp_id} AND id={nm}"
            flag = 1
            res_dt= await db_Insert(table_name,fields,values,where,flag)
        except mysql.connector.Error as err:
            res_dt = {"suc": 0, "msg": err}
        
    return res_dt