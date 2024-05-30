from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import EditHeaderFooter,DiscountSettings,GSTSettings,GeneralSettings
# from models.otp_model import generateOTP
from datetime import datetime

# testing git
setRouter = APIRouter()

# Receipt settings
#-------------------------------------------------------------------------------------------------------------
@setRouter.get('/receipt_settings/{comp_id}')
async def show_items(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.* FROM md_receipt_settings a, md_header_footer b WHERE a.comp_id=b.comp_id AND a.comp_id={comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

#Select items with rate
'''@setRouter.get('/item_rate/{item_id}')
async def show_item_rate(item_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.id, a.item_name, c.price, c.discount, c.sale_price, c.hsn_code, c.cgst, c.sgst FROM md_items a, md_company b, md_item_rate c WHERE a.comp_id=b.id AND a.id=c.item_id AND a.id={item_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result'''

# Generate receipt no.
# Edit header-footer option for 'M' user type
#-------------------------------------------------------------------------------------------------------------
@setRouter.post('/edit_header_footer')
async def edit_header_footer(edit:EditHeaderFooter):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_header_footer SET header1 = '{edit.header1}', on_off_flag1 = '{edit.on_off_flag1}', header2 = '{edit.header2}', on_off_flag2 = '{edit.on_off_flag2}', footer1 = '{edit.footer1}', on_off_flag3 = '{edit.on_off_flag3}', footer2 = '{edit.footer2}', on_off_flag4 = '{edit.on_off_flag4}', created_by = '{edit.created_by}', created_at = '{formatted_datetime}' WHERE comp_id = {edit.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    # print(query)
    if cursor.rowcount>0:
        resData= {
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# Edit Settings
#-------------------------------------------------------------------------------------------------------------
@setRouter.post('/edit_discount_settings')
async def edit_discount_settings(rcp_set:DiscountSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET discount_flag='{rcp_set.discount_flag}', discount_type='{rcp_set.discount_type}', discount_position='{rcp_set.discount_position}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# GST Settings
#-----------------------------

@setRouter.post('/edit_gst_settings')
async def edit_gst_settings(rcp_set:GSTSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET gst_flag='{rcp_set.gst_flag}', gst_type='{rcp_set.gst_type}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData

# General Settings
#-----------------------------

@setRouter.post('/edit_general_settings')
async def edit_general_settings(rcp_set:GeneralSettings):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_receipt_settings SET rcv_cash_flag='{rcp_set.rcv_cash_flag}', rcpt_type='{rcp_set.rcpt_type}', unit_flag='{rcp_set.unit_flag}', cust_inf='{rcp_set.cust_inf}', pay_mode='{rcp_set.pay_mode}', stock_flag='{rcp_set.stock_flag}', price_type='{rcp_set.price_type}', refund_days='{rcp_set.refund_days}', kot_flag='{rcp_set.kot_flag}', modified_by='{rcp_set.modified_by}', modified_at='{formatted_dt}' WHERE comp_id={rcp_set.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount>0:
        resData= {  
        "status":1,
        "data":"data edited successfully"
        }
    else:
        resData= {"status":0, "data":"data not edited"}
       
    return resData