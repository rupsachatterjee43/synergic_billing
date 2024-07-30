from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import EditItem,AddItem,SearchByBarcode,SearchByCategory
# from models.otp_model import generateOTP
from datetime import datetime

# testing git
itmRouter = APIRouter()


#Select items
#-------------------------------------------------------------------------------------------------------------
@itmRouter.get('/items/{comp_id}')
async def show_items(comp_id:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.*, c.unit_name, d.category_name FROM md_items a JOIN md_item_rate b on a.id=b.item_id JOIN md_category d on d.sl_no = a.catg_id LEFT JOIN md_unit c on c.sl_no=a.unit_id WHERE a.comp_id={comp_id}"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result

# Edit item_rate
#-------------------------------------------------------------------------------------------------------------
@itmRouter.post('/edit_item')
async def edit_items(edit_item:EditItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_item_rate JOIN md_items ON md_items.id=md_item_rate.item_id SET md_items.item_name = '{edit_item.item_name}', md_item_rate.price = {edit_item.price}, md_item_rate.discount = {edit_item.discount}, md_item_rate.cgst = {edit_item.cgst}, md_item_rate.sgst = {edit_item.sgst}, md_items.unit_id={edit_item.unit_id}, md_items.catg_id={edit_item.catg_id}, md_item_rate.modified_by = '{edit_item.modified_by}', md_item_rate.modified_dt = '{formatted_dt}', md_items.modified_by = '{edit_item.modified_by}', md_items.modified_dt = '{formatted_dt}' WHERE md_item_rate.item_id={edit_item.item_id} AND md_items.comp_id={edit_item.comp_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(query,"[[[[[[]]]]]]")
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

# Add items
#---------------------------------------------------------------------------------------------------------------------------
@itmRouter.post('/add_item')
async def add_items(add_item:AddItem):
    current_datetime = datetime.now()
    formatted_dt = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO md_items(comp_id, hsn_code, item_name, unit_id, catg_id, created_by, created_dt) VALUES ({add_item.comp_id}, '{add_item.hsn_code}', '{add_item.item_name}', {add_item.unit_id}, {add_item.catg_id},'{add_item.created_by}', '{formatted_dt}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    # print(query)
    if cursor.rowcount>0:
        conn1 = connect()
        cursor1 = conn1.cursor()
        query1 = f"INSERT INTO md_item_rate (item_id, price, discount, cgst, sgst, created_by, created_dt) VALUES ({cursor.lastrowid}, {add_item.price}, {add_item.discount}, {add_item.cgst}, {add_item.sgst}, '{add_item.created_by}', '{formatted_dt}')"
        cursor1.execute(query1)
        conn1.commit()
        conn1.close()
        cursor1.close()
        if cursor1.rowcount>0:
            conn2 = connect()
            cursor2 = conn2.cursor()
            query2 = f"INSERT INTO td_stock (comp_id, br_id, item_id, stock, created_by, created_dt) VALUES ({add_item.comp_id}, {add_item.br_id}, {cursor.lastrowid}, '0', '{add_item.created_by}', '{formatted_dt}')"
            cursor2.execute(query2)
            conn2.commit()
            conn2.close()
            cursor2.close()
            if cursor2.rowcount>0:
                resData={"status":1, "data": "Item and Stock Added Successfully"}
            else:
                resData={"status":0, "data": "No Stock Added"}
        else:
            resData= {"status":0, "data":"Item Rate not Added"}
    else:
        resData={"status":-1, "data":"No Data Added"}
       
    return resData

#===============================================================================================
#==================================================================================================
# Search item info by barcode

@itmRouter.post('/search_by_barcode')
async def search_by_barcode(bar:SearchByBarcode):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.id, a.comp_id, a.hsn_code, a.item_name, a.description, a.unit_id, a.bar_code, a.created_by, a.created_dt, a.modified_by, a.modified_dt, b.item_id, b.price, b.discount, b.cgst, b.sgst, c.unit_name FROM md_items a JOIN md_item_rate b on a.id=b.item_id LEFT JOIN md_unit c on c.sl_no=a.unit_id WHERE a.comp_id={bar.comp_id} and a.bar_code='{bar.bar_code}'"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        res_dt={"status":1, "msg":result}
    else:
        res_dt={"status":0, "msg":[]}
    return res_dt

#===============================================================================================

