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
    gst_flag:str
    discount_type:str
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
    comp_id:int
    item_name:str
    item_id:int
    price:float
    discount:float
    cgst:float
    sgst:float
    # unit_name:str
    unit_id:int
    modified_by:str
    
class EditRcpSettings(BaseModel):
    comp_id:int
    rcpt_type:str
    gst_flag:str
    unit_flag:str
    cust_inf:str
    pay_mode:str
    discount_flag:str
    stock_flag:str
    discount_type:str
    price_type:str
    created_by:str
    modified_by:str

class AddItem(BaseModel):
    comp_id:int
    br_id:int
    hsn_code:str
    item_name:str
    unit_id:int
    # unit_name:str
    created_by:str
    price:float
    discount:float
    cgst:float
    sgst:float

class CancelBill(BaseModel):
    receipt_no:int
    user_id:str

class AddUnit(BaseModel):
    comp_id:int
    unit_name:str
    created_by:str

class EditUnit(BaseModel):
    comp_id:int
    sl_no:int
    unit_name:str
    modified_by:str

class InventorySearch(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    user_id:str

class UpdateStock(BaseModel):
    comp_id:int
    br_id:int
    item_id:int
    user_id:str
    added_stock:int
    # flag:int  # 0 = out , 1 = in

class StockReport(BaseModel):
    comp_id:int
    br_id:int

class CancelBillReport(BaseModel):
    from_date:date
    to_date:date

class CancelItem(BaseModel):
    user_id:str
    receipt_no:int
    item_id:int
    qty:int

class RefundItem(BaseModel):
    user_id:str
    receipt_no:int
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
    tot_refund_amt:float
    round_off:float
    net_amt:int
    pay_mode:str
    cust_name:str
    phone_no:str
    gst_flag:str
    discount_type:str