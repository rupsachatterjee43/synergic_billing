from fastapi import APIRouter
from models.master_model import createResponse
from models.masterApiModel import db_select, db_Insert
from models.admin_form_model import CompId,SupplierId,UpdateSupplier,UpdatePurchase
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

# ==================================================================================================
# Add And Edit Purchase Data

@purchaseRouter.post('/add_edit_purchase_data')
async def add_edit_purchase_data(data:UpdatePurchase):
    current_datetime = datetime.now()
    receipt = int(round(current_datetime.timestamp()))
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    for i in {data.item_id}:
        print(i,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if i>0:
    
            table_name1 = 'td_item_purchase'
            fields1 = f"price={i.price}, cgst_prtg={i.cgst}, cgst_amt={((i.price*i.cgst)/100).toFixed(2)}, sgst_prtg={i.sgst}, sgst_amt={((i.price*i.sgst)/100).toFixed(2)}, qty={i.qty}, modified_by='admin', modified_dt='{formatted_dt}'" if ({data.purchase_id}.pop())>0 else "purchase_id, comp_id, br_id, item_id, price, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, unit_name, created_by, created_dt"
            values1 = f"{receipt}, {i.comp_id}, {i.brn_id}, {i.item_id}, {i.price}, {i.cgst}, {((i.price*i.cgst)/100).toFixed(2)}, {i.sgst}, {((i.price*i.sgst)/100).toFixed(2)}, {i.qty}, '{i.unit_name}','admin','{formatted_dt}'"
            where1 = f"purchase_id = {i.purchase_id} AND item_id = {i.item_id} AND unit_name = '{i.unit_name}'" if ({data.purchase_id}.pop())>0 else None
            flag1 = 1 if ({data.purchase_id}.pop())>0 else 0
            res_dt = await db_Insert(table_name,fields,values,where,flag)

        else:
            table_name1 = 'td_item_purchase'
            fields1 = f"price={data.price}, cgst_prtg={data.cgst}, cgst_amt={((data.price*data.cgst)/100).toFixed(2)}, sgst_prtg={data.sgst}, sgst_amt={((data.price*data.sgst)/100).toFixed(2)}, qty={data.qty}, modified_by='admin', modified_dt='{formatted_dt}'" if ({data.purchase_id}.pop())>0 else "purchase_id, comp_id, br_id, item_id, price, cgst_prtg, cgst_amt, sgst_prtg, sgst_amt, qty, unit_name, created_by, created_dt"
            values1 = f"{receipt}, {data.comp_id}, {data.brn_id}, {data.item_id}, {data.price}, {data.cgst}, {((data.price*data.cgst)/100).toFixed(2)}, {data.sgst}, {((data.price*data.sgst)/100).toFixed(2)}, {data.qty}, '{data.unit_name}','admin','{formatted_dt}'"
            where1 = f"purchase_id = {receipt} AND item_id = {data.item_id} AND unit_name = '{data.unit_name}'" if ({data.purchase_id}.pop())>0 else None
            flag1 = 1 if ({data.purchase_id}.pop())>0 else 0
            res_dt = await db_Insert(table_name,fields,values,where,flag)
    if res_dt["suc"]>0:
        table_name = "td_purchase"
        fields = f"supplier_id='{data.sup_id}',pay_mode='{data.pay_mode}',modified_by='Admin',modified_at='formatted_dt'" if ({data.purchase_id}.pop())>0 else "purchase_id,comp_id,br_id, supplier_id,invoice_no,invoice_date,pay_mode,created_by,created_at"
        values = f"{receipt},{data.comp_id},{data.br_id},{data.sup_id}, '{data.invoice_no}','date({formatted_dt})','{data.pay_mode}','admin','{formatted_dt}'"
        where = f"comp_id={data.comp_id} and purchase_id = {data.purchase_id}" if ({data.purchase_id}.pop())>0 else None
        flag = 1 if ({data.purchase_id}.pop())>0 else 0
        purchase_dt = await db_Insert(table_name,fields,values,where,flag)

    return purchase_dt
