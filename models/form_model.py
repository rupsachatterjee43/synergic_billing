from pydantic import BaseModel
from datetime import date

class CreatePIN(BaseModel):
    PIN:str
    phone_no:str

class UserLogin(BaseModel):
    user_id:str
    PIN:str

class Receipt(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    price:float
    dis_pertg:float
    discount_amt:float
    cgst_prtg:float
    cgst_amt:float
    sgst_prtg:float
    sgst_amt:float
    qty:int
    tprice:float
    tdiscount_amt:float
    # tcgst_amt:float
    # tsgst_amt:float
    amount:float
    round_off:float
    net_amt:int
    pay_mode:str
    received_amt:str
    pay_dtls:str
    cust_name:str
    phone_no:str
    created_by:str

class DashBoard(BaseModel):
    trn_date:date
    comp_id:int
    br_id:int
    user_id:str

class SearchBill(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int
    user_id:str

class SaleReport(BaseModel):
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
    item_id:int
    user_id:str

class EditHeaderFooter(BaseModel):
    comp_id:int
    header1:str
    on_off_flag1:str
    header2:str
    on_off_flag2:str
    footer1:str
    on_off_flag3:str
    footer2:str
    on_off_flag4:str
    created_by:str

class EditItem(BaseModel):
    com_id:int
    item_id:int
    price:float
    discount:float
    cgst:float
    sgst:float
    modified_by:str
    
class EditRcpSettings(BaseModel):
    comp_id:int
    rcpt_type:str
    gst_flag:str
    cust_inf:str
    pay_mode:str
    discount_type:str
    created_by:str
    modified_by:str