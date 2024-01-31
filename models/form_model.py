from pydantic import BaseModel, datetime_parse
from datetime import date

class UserRegistration(BaseModel):
    comp_id:str
    br_id:str
    user_name:str
    phone_no:str
    email_id:str
    device_id:str
    password:str

class UserLogin(BaseModel):
    user_id:str
    password:str