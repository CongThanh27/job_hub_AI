import pandas as pd
from sklearn.preprocessing import LabelEncoder
from db_connection import connect_to_database_sql
from db_connection import connect_to_mongodb
query = """
SELECT 
    users.user_id,
    job.job_id,
    COALESCE(applied_count, 0) + COALESCE(views_count, 0) + COALESCE(likes_count, 0) AS rating
FROM 
    users
CROSS JOIN job
LEFT JOIN (
    SELECT student_user_id, job_job_id, COUNT(*) AS applied_count
    FROM job_apply
    GROUP BY student_user_id, job_job_id
) AS applied ON users.user_id = applied.student_user_id AND job.job_id = applied.job_job_id
LEFT JOIN (
    SELECT user_id, job_id, COALESCE(SUM(views), 0) AS views_count
    FROM user_job_views
    GROUP BY user_id, job_id
) AS views ON users.user_id = views.user_id AND job.job_id = views.job_id
LEFT JOIN (
    SELECT user_user_id, job_job_id, COUNT(*) AS likes_count
    FROM short_list
    GROUP BY user_user_id, job_job_id
) AS likes ON users.user_id = likes.user_user_id AND job.job_id = likes.job_job_id;

"""
# Hàm xử lý dữ liệu
def process_data():
    # Kết nối đến cơ sở dữ liệu
    conn = connect_to_database_sql()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    db_mongo = connect_to_mongodb()

    # Chèn dữ liệu vào MongoDB
    collection = db_mongo['data_before']  
    collection.delete_many({})
    for row in rows:
        data = {
            'user_id': row[0],
            'job_id': row[1],
            'rating': row[2]
        }
        collection.insert_one(data)
    # Đóng kết nối
    conn.close()
    db_mongo.client.close()
#hàm lấy dữ liệu từ mongodb và in ra màn hình

def get_data(nametable):
    db_mongo = connect_to_mongodb()
    collection = db_mongo[nametable]
    data = collection.find()
    data = pd.DataFrame(list(data))
    return data

    
#Hàm lấy số lượng người dùng và số lượng công việc
def get_number_users():
    conn = connect_to_database_sql()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)
    number_users = cursor.fetchone()[0]
    conn.close()
    return number_users

def get_number_jobs():
    conn = connect_to_database_sql()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM job"
    cursor.execute(query)
    number_jobs = cursor.fetchone()[0]
    conn.close()
    return number_jobs


def encode_data():
    # Lấy data từ mongodb
    original_data = get_data("data_before")
    
    # Sao chép dữ liệu
    data = original_data.copy()
    
    # Khởi tạo một đối tượng LabelEncoder
    label_encoder = LabelEncoder()
    
    # Mã hóa cột 'user_id' và 'job_id'
    data['user_id_encoded'] = label_encoder.fit_transform(data['user_id'])
    data['job_id_encoded'] = label_encoder.fit_transform(data['job_id'])
    
    # Ghép bảng data và data_encoded thành một bảng mới
    data = pd.concat([data, original_data], axis=1)
    # In ra màn hình 5 dòng đầu tiên của dữ liệu đã được mã hóa
    print(data.head(100))
    
    db_mongo = connect_to_mongodb()
    
    # Chèn dữ liệu vào MongoDB
    collection = db_mongo['data_after']
    collection.delete_many({})
    # Chuyển dữ liệu thành định dạng dictionary để chèn vào MongoDB
    data_to_insert = data.to_dict(orient='records')
    
    # Chèn dữ liệu vào MongoDB
    collection.insert_many(data_to_insert)
    
    # Trả về dữ liệu đã được mã hóa
    return data

   
