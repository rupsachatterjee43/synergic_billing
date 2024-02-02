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

# class VerifyUser(BaseModel):
#     phone_no:str
#     active_flag:str

class UserLogin(BaseModel):
    user_id:str
    password:str

class Receipt(BaseModel):
    receipt_no:int
    comp_id:str
    br_id:str
    item_id:str
    price:str
    discount_amt:str 
    cgst_amt:str 
    sgst_amt:str 
    created_by:str 
    