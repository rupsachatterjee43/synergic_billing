from fastapi import APIRouter, File, UploadFile, Depends, Form
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import AddEditLocation,AddEditCompany,AddEditUser,AddEditOutletS,OneOutlet,AddHeaderFooter,AddEditSettings,AddEditUnit
from datetime import datetime
from typing import Annotated, Union, Optional
import os
# import pandas as pd

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
    select = "id,company_name,address,location,phone_no,email_id,active_flag,max_user"
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
    fields = f"company_name='{data.company_name}', address='{data.address}', location={data.location}, contact_person='{data.contact_person}', phone_no={data.phone_no}, email_id='{data.email_id}', logo='{data.logo}',web_portal='{data.web_portal}',active_flag='{data.active_flag}',max_user={data.max_user},modified_by='{data.user_id}', modified_dt='{formatted_dt}'" if data.id>0 else f"company_name,address,location,contact_person,phone_no,email_id,logo,web_portal,active_flag,max_user,created_by, created_dt"
    values = None if data.id>0 else f"'{data.company_name}','{data.address}',{data.location},'{data.contact_person}',{data.phone_no},'{data.email_id}','{data.logo}','{data.web_portal}','{data.active_flag}',{data.max_user},'{data.user_id}', '{formatted_dt}'"
    where = f"id = {data.id}" if data.id>0 else None
    order = ""
    flag = 1 if data.id>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
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

# ---------------Add And Edit User---------------
@superadminRouter.post('/S_Admin/add_edit_user')
async def add_edit_user(data:AddEditUser):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    table_name = f"md_user"
    fields = f"comp_id={data.comp_id}, br_id={data.br_id}, user_name='{data.user_name}', user_type='{data.user_type}', user_id='{data.user_id}', phone_no={data.phone_no}, email_id='{data.email_id}', device_id='0',password='{data.password}',active_flag='{data.active_flag}',login_flag='{data.login_flag}',modified_by='{data.created_by}', modified_dt='{formatted_dt}'" if data.id>0 else f"comp_id,br_id,user_name,user_type,user_id,phone_no,email_id,device_id,password,active_flag,login_flag,created_by, created_dt"
    values = None if data.id>0 else f"{data.comp_id},{data.br_id},'{data.user_name}','{data.user_type}','{data.user_id}',{data.phone_no},'{data.email_id}','0','{data.password}','{data.active_flag}','{data.login_flag}','{data.created_by}', '{formatted_dt}'"
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
    select = "comp_id,header1,on_off_flag1,header2,on_off_flag2,footer1,on_off_flag3,footer2,on_off_flag4"
    table_name = "md_header_footer"
    where = f"comp_id={comp_id}" if comp_id>0 else f""
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
    select = "comp_id,rcv_cash_flag,rcpt_type,gst_flag,gst_type,unit_flag,cust_inf,pay_mode,discount_flag,stock_flag,discount_type,discount_position,price_type,refund_days,kot_flag"
    table_name = "md_receipt_settings"
    where = f"comp_id={comp_id}" if comp_id>0 else f""
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


# @superadminRouter.get('/S_Admin/insert_excel')
# async def insert_excel():
#     current_datetime = datetime.now()
#     formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

#     for index, row in df.iterrows():
#         print(row)
#         return tuple(row)