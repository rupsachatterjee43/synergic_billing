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