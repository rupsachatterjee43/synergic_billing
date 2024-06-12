from fastapi import APIRouter
from config.database import connect
from models.master_model import createResponse
from models.form_model import LoginFlag, UserLogin,LoginStatus,CreatePIN
# from models.otp_model import generateOTP
from utils import get_hashed_password

# testing git
userRouter = APIRouter()


# Verify Phone no and active status
#------------------------------------------------------------------------------------------------------
@userRouter.post('/verify_phone/{phone_no}')
async def verify(phone_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*)phone_no FROM md_user WHERE user_id=phone_no AND user_type in ('U','M') AND phone_no={phone_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    # return result
    if records==[(0,)]:
       resData= {"status":0, "data":"invalid phone"}
    else:
        resData= {
        "status":1,
        "data":"valid phone no."
        }
    return resData
     
   
@userRouter.post('/verify_active/{phone_no}')
async def verify(phone_no:int):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT COUNT(*)active_flag FROM md_user WHERE active_flag='N' AND user_id={phone_no}"
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    # result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    if records==[(0,)]:
        resData= {"status":-1, "data":"Already registered or invalid phone"}
    else:
        resData= {
        "status":1,
        "data":"registered successfully"
        }
    return resData 

# Create PIN
#-------------------------------------------------------------------------------------------------------------
@userRouter.post('/create_pin')
async def register(data:CreatePIN):
    password=data.PIN
    haspass=get_hashed_password(password)
    conn = connect()
    cursor = conn.cursor()
    query = f"UPDATE md_user SET password='{haspass}', active_flag='Y' where user_id='{data.phone_no}'"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount==1:
        resData= {"status":1, "data":"Pin inserted"}
    else:
        resData= {
        "status":0,
        "data":"invalid phone"
        }
    return resData 

# Generate OTP
#-------------------------------------------------------------------------------------------------------------
@userRouter.post('/otp/{phone_no}') 
async def OTP(phone_no:int):
    return {"status":1, "data":"1234"}

# USER LOGIN

@userRouter.post('/update_login_status')
async def update_login_status(data:LoginStatus):
    conn = connect()
    cursor = conn.cursor()
    query = f"update md_user set login_flag = 'Y' where user_id = '{data.user_id}'"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData={"suc":1, "msg":"User login flag updated"}
    else:
        resData={"suc":0, "msg":"failed to update login_flag"}

    return resData

#-----------------------------------------------------------------------------------------------------------  
@userRouter.post('/login')
async def login(data_login:UserLogin):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.*, b.*, c.* FROM md_user a, md_branch b, md_company c WHERE a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id AND a.active_flag='Y' AND a.user_type in ('U','M')"
    cursor.execute(query)
    records = cursor.fetchone()
    # print(cursor.rowcount)
    

    if cursor.rowcount>0:
        print(len(records),"oooooooooo")
        result = createResponse(records, cursor.column_names, 0)
        conn.close()
        cursor.close()

        conn = connect()
        cursor = conn.cursor()
        query = f"select count(*)no_of_user from md_user where comp_id = {result['comp_id']} AND user_type in ('U','M') and login_flag = 'Y'"
        cursor.execute(query)
        records = cursor.fetchone()
        result1 = createResponse(records, cursor.column_names, 0)
        conn.close()
        cursor.close()
       
        if cursor.rowcount>0:
            if result1['no_of_user'] < result['max_user']:
                res_dt = {"suc": 1, "msg": result, "user": result1['no_of_user']+1}
               
            else:
                 res_dt = {"suc": 0, "msg": "Max user limit reached"}
        
        else:
            res_dt = {"suc": 0, "msg": "error while selecting no_of_user"}
    else:
        res_dt = {"suc": 0, "msg": "No user found"}

    return res_dt

#=================================================================================================
#Logout 
@userRouter.post('/logout')
async def logout(flag:LoginFlag):
    conn = connect()
    cursor = conn.cursor()

    query = f"update md_user set login_flag = 'N' where comp_id={flag.comp_id} and br_id={flag.br_id} and user_id='{flag.user_id}' and user_type in ('U','M')"

    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    if cursor.rowcount>0:
        resData = {
            "status":1,
            "data":"logged out successfully"
        }
    else:
        resData = {
            "status":0,
            "data":"No user Found"
        }

    return resData