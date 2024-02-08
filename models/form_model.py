from pydantic import BaseModel, datetime_parse
from datetime import date

# class UserRegistration(BaseModel):
#     comp_id:str
#     br_id:str
#     user_name:str
#     phone_no:str
#     email_id:str
#     device_id:str
#     password:str

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
    discount_amt:float
    cgst_amt:float
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
    

# class Receipt(BaseModel):
#     data:dict
    
# class FinalRcp(BaseModel):
#     price:str
#     discount_amt:str
#     cgst_amt:str
#     sgst_amt:str
#     round_off:str
#     amount:str
#     pay_mode:str
#     received_amt:str
#     pay_dtls:str

class DashBoard(BaseModel):
    trn_date:date
    comp_id:int
    br_id:int
    user_id:str