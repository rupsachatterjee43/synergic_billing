from pydantic import BaseModel
import json
from datetime import date
from fastapi import File, UploadFile, Form
from typing import Annotated, Union, Optional, List

# ======================================================================================================
# Common Model 

class CompId(BaseModel):
    comp_id:int

# ======================================================================================================
# Models Used in user.py

class UserList(BaseModel):
    comp_id:int
    br_id:int

class UserLogin(BaseModel):
    user_id:str
    password:str

class UserProfile(BaseModel):
    comp_id:int
    user_id:str

class AddUser(BaseModel):
    comp_id:int
    br_id:int
    user_name:str
    user_type:str
    phone_no:str
    email_id:str | None
    device_id:str | None
    # active_flag:str
    # login_flag:str
    created_by:str

class EditUser(BaseModel):
    comp_id:int
    user_id:str
    user_name:str
    user_type:str
    phone_no:str
    login_flag:str
    active_flag:str

class CheckPassword(BaseModel):
    old_password:str
    comp_id:int
    user_id:str

class ResetPassword(BaseModel):
    old_password:str
    new_password:str
    comp_id:int
    user_id:str

class AddEditOutlet(BaseModel):
    br_id:int
    comp_id:int
    branch_name:str
    branch_address:str
    location:int
    contact_person:str
    phone_no:int
    email_id:str
    user_id:str

# ============================================================================================================
# Models Used in report.py

class SaleReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class CollectionReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int
    user_id:str

class ItemReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class PayModeReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class UserWiseReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class GSTstatement(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class RefundReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class CreditReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class CancelReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class DaybookReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int

class CustomerLedger(BaseModel):
    comp_id:int
    br_id:int
    phone_no:str

class RecveryReport(BaseModel):
    comp_id:int
    br_id:int
    from_date:date
    to_date:date

class DueReport(BaseModel):
    comp_id:int
    br_id:int
    date:date

class dashboard(BaseModel):
    comp_id:int
    from_date:date
    to_date:date

# ======================================================================================================
# Search By Date, Phone and Item

class SearchByDate(BaseModel):
    from_date:date
    to_date:date
    comp_id:int

class SearchByPhone(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    phone_no:str

# class SearchByReceipt(BaseModel):
#     comp_id:int
#     receipt_no:int

class SearchByItem(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    item_id:int

class PrintBill(BaseModel):
    recp_no:int

# ===========================================================================================================
# Settings.py

class DiscountSettings(BaseModel):
    comp_id:int
    discount_flag:str
    discount_type:str
    discount_position:str
    modified_by:str

class GSTSettings(BaseModel):
    comp_id:int
    gst_flag:str
    gst_type:str
    modified_by:str

class GeneralSettings(BaseModel):
    comp_id:int
    rcv_cash_flag:str
    rcpt_type:str
    unit_flag:str
    cust_inf:str
    pay_mode:str
    stock_flag:str
    price_type:str
    refund_days:int
    kot_flag:str
    modified_by:str

# =========================================================================================================
# items.py

class ItemId(BaseModel):
    item_id:int

class AddEditItem(BaseModel):
    comp_id:int
    # br_id:int
    item_id:int
    item_name:str
    unit_id:int 
    price:float 
    discount:float 
    cgst:float 
    sgst:float 
    hsn_code:int 
    catg_id:int
    created_by:str 

class CatgId(BaseModel):
    comp_id:int
    catg_id:int

class UpdateCategory(BaseModel):
    comp_id: Annotated[int, Form()]
    catg_id: Annotated[int, Form()]
    category_name: Annotated[str, Form()]
    file: Annotated[UploadFile, File(...)]
    # catg_picture:str

# ========================================================================================================
# customer.py

class CustomerId(BaseModel):
    comp_id:int
    cust_id:int

class AddEditCustomer(BaseModel):
    comp_id:int
    cust_id:int
    cust_name:str
    phone_no:str
    bill_address:str 
    delivery_address:str 
    email_id:str 
    pay_mode:str 
    date_of_birth:str 
    gender:str 

# =========================================================================================================
# unit.py

class AddUnit(BaseModel):
    comp_id:int
    unit_name:str
    unit_id:int
    # created_by:str

# ===========================================================================================================
# Stock.py

class Stock(BaseModel):
    comp_id:int
    item_id:int

class Fetch(BaseModel):
    comp_id:int
    br_id:int
    item_id:int

class AddStock(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    stock_add:int
    stock_less:int

class StockIn(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    in_price:float | None
    in_cgst:float | None
    in_sgst:float | None
    qty:int
    created_by:str

class StockOut(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    qty:int
    damage_flag:str
    remarks:str | None
    created_by:str

# ============================================================================================================

class SupplierId(BaseModel):
    comp_id:int
    sup_id:int

class AddEditHeaderFooter(BaseModel):
    comp_id:int
    header1:str
    on_off_flag1:str
    header2:str
    on_off_flag2:str
    footer1:str
    on_off_flag3:str
    footer2:str
    on_off_flag4:str

class UpdateSupplier(BaseModel):
    sup_id:int
    comp_id:int
    supplier_name:str
    gstin:str
    address:str   
    
class UpdatePurchase(BaseModel):
    comp_id:int
    br_id:int
    sup_id:int
    pay_mode:str
    purchase_id:int
    invoice_no:str
    price:float
    cgst:float
    sgst:float
    unit_name:str
    item_id:int

# ====================================================================================================
# Manage Super Admin

# -------------------Manage Location---------------
class AddEditLocation(BaseModel):
    sl_no:int
    location_name:str
    user_id:str

# --------------------Manage Shop(Company)----------------
class AddEditCompany(BaseModel):
    id:int
    company_name:str
    mode:str
    address:Optional[str] = None
    location:int | None
    contact_person:Optional[str] = None
    phone_no:int | None
    email_id:Optional[str] = None
    # logo:str | None 
    web_portal:Optional[str] = None
    active_flag:str
    max_user:int
    user_id:str

# ---------------Manage User--------------------
class AddEditUser(BaseModel):
    id:int
    comp_id:int
    br_id:int
    user_name:str
    user_type:str
    user_id:str
    # phone_no:int
    # email_id:str
    # device_id:str | None
    password:str| None
    active_flag:str
    login_flag:str
    created_by:str

# ---------------Manage Outlets---------------

class OneOutlet(BaseModel):
    comp_id:int
    br_id:int

class AddEditOutletS(BaseModel):
    br_id:int
    comp_id:int
    branch_name:str
    branch_address:str | None
    location:int | None
    contact_person:str | None
    phone_no:int | None
    email_id:str | None
    created_by:str

# -------------------Manage Header Footer-------------------

class AddHeaderFooter(BaseModel):
    comp_id:int
    header1:str | None
    on_off_flag1:str
    header2:str | None
    on_off_flag2:str
    footer1:str | None
    on_off_flag3:str
    footer2:str | None
    on_off_flag4:str
    created_by:str

# -------------------Manage Setting Details-------------------

class AddEditSettings(BaseModel):
    comp_id:int
    rcv_cash_flag:str
    rcpt_type:str
    gst_flag:str
    gst_type:str
    unit_flag:str
    cust_inf:str
    pay_mode:str
    discount_flag:str
    stock_flag:str
    discount_type:str
    discount_position:str
    price_type:str
    refund_days:int|None
    kot_flag:str
    created_by:str

class AddEditUnit(BaseModel):
    sl_no:int
    comp_id:int
    unit_name:str
    created_by:str

class Excel(BaseModel):
    comp_id:int
    catg_id:int
    created_by:str

class EditItemDtls(BaseModel):
    comp_id:int
    item_id:int
    item_name:str
    hsn_code:str
    catg_id:int
    unit_id:int
    bar_code:str
    price:float
    discount:float
    cgst:float
    sgst:float
    created_by:str

class Item(BaseModel):
    comp_id: int
    catg_id: int
    item_id: list = []