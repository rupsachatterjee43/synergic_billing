from pydantic import BaseModel
from datetime import date

class UserList(BaseModel):
    comp_id:int
    br_id:int

class UserLogin(BaseModel):
    user_id:str

class CompId(BaseModel):
    comp_id:int

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

class PayModeReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int
    pay_mode:str

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

class SearchByDate(BaseModel):
    from_date:date
    to_date:date
    comp_id:int

class SearchByPhone(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    phone_no:str

class SearchByItem(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    item_id:int

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
    rcpt_type:str
    unit_flag:str
    cust_inf:str
    pay_mode:str
    stock_flag:str
    price_type:str
    refund_days:int
    kot_flag:str
    modified_by:str

class AddUnit(BaseModel):
    comp_id:int
    unit_name:str
    unit_id:int
    # created_by:str

class ItemId(BaseModel):
    item_id:int

class AddEditItem(BaseModel):
    comp_id:int
    item_id:int
    item_name:str
    unit_id:int
    price:float
    discount:float
    cgst:float
    sgst:float
    hsn_code:int


