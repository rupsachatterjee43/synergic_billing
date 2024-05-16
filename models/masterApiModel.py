from config.database import connect
import mysql.connector
from models.master_model import createResponse

async def db_select(select, schema, where, order, flag):
    whr = f"WHERE {where}" if where != '' else ''
    sql = f"SELECT {select} FROM {schema} {whr} {order}"
    res_dt = {}
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall() if flag > 0 else cursor.fetchone()
        if(records is not None):
            result = createResponse(records, cursor.column_names, flag)
            res_dt = {"suc": 1, "msg": result}

        else:
            res_dt = {"suc": 2, "msg": "No Data Found"}
        conn.close()
        cursor.close()    
        
    except mysql.connector.Error as err:
        # conn.close()
        # cursor.close()
        res_dt = {"suc": 0, "msg": err}
    
    finally:
        return res_dt

async def db_Insert(table_name, fields, values, whr, flag):
    res_dt = {}
    sql = ''
    msg = ''
    errMsg = ''

    if (flag > 0):
        sql = f"UPDATE {table_name} SET {fields} {whr}"

        msg = "Updated Successfully !!"
        errMsg = "Data not inserted Updated !!"
    else:
        sql = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
        msg = "Inserted Successfully !!"
        errMsg = "Data not inserted Inserted !!"

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(sql)

        conn.commit()
        conn.close()
        cursor.close()

        if cursor.rowcount>0:
            res_dt = {"suc":1, "msg":msg}
        else:
            res_dt = {"suc":0, "msg":errMsg}
    except mysql.connector.Error as err:
        # conn.close()
        # cursor.close()
         res_dt =  {"suc": 0, "msg": err}

    finally:
        return res_dt