from pydantic import BaseModel, datetime_parse
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
    tcgst_amt:float
    tsgst_amt:float
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

class ItemReport(BaseModel):
    from_date:date
    to_date:date
    comp_id:int
    br_id:int
    item_id:int