from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,SupplierId,UpdateSupplier
from datetime import datetime

purchaseRouter = APIRouter()

# =================================================================================================
# Suppliers' List

@purchaseRouter.post('/all_supplier_list')
async def all_supplier_list(data:CompId):
    select = "id,supplier_name,gstin,address"
    table_name = "md_supplier"
    where = f"comp_id = {data.comp_id}"
    order = ''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Details of a Supplier

@purchaseRouter.post('/supplier_by_id')
async def supplier_by_id(data:SupplierId):
    select = "supplier_name,gstin,address"
    table_name = "md_supplier"
    where = f"comp_id = {data.comp_id} and id = {data.sup_id}"
    order = ''
    flag = 1
    res_dt = await db_select(select,table_name,where,order,flag)
    return res_dt

# ==================================================================================================
# Add or Edit Supplier

@purchaseRouter.post('/add_edit_supplier')
async def add_edit_supplier(data:UpdateSupplier):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    select = "supplier_name,gstin,address"
    table_name = "md_supplier"
    where = f"comp_id = {data.comp_id} and id = {data.sup_id}"
    order = ''
    flag = 1
    sup_dt = await db_select(select,table_name,where,order,flag)
    table_name = "md_supplier"
    fields = f"supplier_name ='{data.supplier_name}', gstin = '{data.gstin}', address = '{data.address}', modified_by = 'admin', modified_at = '{formatted_dt}'" if sup_dt["suc"]>0 and len(sup_dt["msg"])>0 else "comp_id,supplier_name,gstin,address,created_by,created_at"
    values = f"{data.comp_id},'{data.supplier_name}','{data.gstin}','{data.address}','admin','{formatted_dt}'"
    where = f"comp_id={data.comp_id} and id={data.sup_id}" if sup_dt["suc"]>0 and len(sup_dt["msg"])>0 else None
    flag = 1 if sup_dt["suc"]>0 and len(sup_dt["msg"])>0 else 0
    res_dt = await db_Insert(table_name,fields,values,where,flag)
    
    return res_dt