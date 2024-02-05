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
    comp_id:str
    br_id:str
    item_id:str
    price:str
    discount_amt:str
    cgst_amt:str
    sgst_amt:str
    qty:int

# class Receipt(BaseModel):
#     data:dict
    
# class Receipt(BaseModel):
#     comp_id:str
#     br_id:str
#     item_id:str
#     price:str
#     discount_amt:str
#     cgst_amt:str
#     sgst_amt:str
#     qty:int