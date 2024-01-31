import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "syn_billing"

db_config = {
    "host": MYSQL_HOST,
    "database": MYSQL_DB,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
}

# Connect to MySQL
def connect():
    # db = mysql.connector.pooling.MySQLConnectionPool(pool_name="timesheet", pool_size=5, pool_reset_session=True, **db_config)
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    # return db