import pyodbc
from pymongo import MongoClient
def connect_to_database_sql():
    # Chuỗi kết nối SQL Server
    server = 'jobhub-kltn.database.windows.net'
    database = 'jobhub-kltn'
    username = 'jobhub'
    password = '28072002Thanh@'
    driver= '{ODBC Driver 17 for SQL Server}'

    # Tạo chuỗi kết nối
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Kết nối đến cơ sở dữ liệu
    conn = pyodbc.connect(connection_string)
    return conn


def connect_to_mongodb():
    # Chuỗi kết nối MongoDB
    uri = "mongodb+srv://toannguyen7202:kltn2024@cluster0.m9xmsj8.mongodb.net/"
    client = MongoClient(uri)
    # Kết nối đến cơ sở dữ liệu
    db = client['jobhub']  # Thay thế 'your_database_name' bằng tên của cơ sở dữ liệu MongoDB của bạn
    return db
