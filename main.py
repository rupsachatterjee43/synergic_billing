from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.database import connect
from models.master_model import createResponse
from models.form_model import UserRegistration,UserLogin
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=3003, reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return "Welcome to the billing app"

# user registration
@app.post('/api/register')
def register(data:UserRegistration):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_datetime)
    conn = connect()
    cursor = conn.cursor()
    query = f"INSERT INTO md_user (comp_id, br_id, user_name, user_id, phone_no, email_id, device_id, password, created_by, created_dt) VALUES('{data.comp_id}','{data.br_id}','{data.user_name}','{data.phone_no}','{data.phone_no}','{data.email_id}', '{data.device_id}', '{data.password}', '{data.user_name}', '{formatted_datetime}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    print(cursor.rowcount)
    if cursor.rowcount==1:
        return "registered successfully"
    else:
        return "invalid date!"
    
@app.post('/api/login')
def login(data_login:UserLogin):
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT a.comp_id, c.company_name, a.br_id, b.branch_name, a.user_id, a.user_name, a.phone_no, a.email_id, a.device_id, a.password, a.created_by, a.created_dt, a.active_flag FROM md_user a, md_branch b, md_company c WHERE a.user_id='{data_login.user_id}' AND b.id=a.br_id AND c.id=a.comp_id"
    cursor.execute(query)
    print(cursor.rowcount)
    records = cursor.fetchone()
    conn.close()
    cursor.close()
    if(records is not None):
        result = createResponse(records, cursor.column_names, 0)
        # print(result)
        res_dt = ''
        if(result['password'] == data_login.password):
            res_dt = {"suc": 1, "msg": result}
        else:
            res_dt = {"suc": 0, "msg": "Please check your userid or password"}
    else:
        res_dt = {"suc": 0, "msg": "No user found"}

    return res_dt

#Select location
@app.get('/api/location')
async def show_location():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT 'sl_no', 'location_name' FROM md_location"
    cursor.execute(query)
    records = cursor.fetchall()
    result = createResponse(records, cursor.column_names, 1)
    conn.close()
    cursor.close()
    return result