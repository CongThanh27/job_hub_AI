# pip freeze > requirements.txt 
from flask import Flask, request, jsonify
import schedule
import time
from handle_data import process_data, encode_data
from recommendation import user_user_collaborative_filtering, item_item_collaborative_filtering, get_recommendation_user_by_job, get_recommendation_job_by_user
from collaborative_filtering import CF
from db_connection import connect_to_database_sql, connect_to_mongodb

app = Flask(__name__)

# Dữ liệu mẫu: danh sách các công việc đã được gợi ý cho mỗi user_id

def refresh_data():
    process_data()
    encode_data()
    user_user_collaborative_filtering()
    item_item_collaborative_filtering()
    
# Đặt lịch trình chạy hàm job mỗi 5 phút
schedule.every(15).minutes.do(refresh_data)
# schedule.every(5).seconds.do(job)

# Hàm chạy lịch trình
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
@app.route('/recommendation/jobs/<string:user_id>', methods=['GET'])
def get_recommendation_jobs_by_user_id(user_id):
    list_job_recommend = get_recommendation_job_by_user(user_id)
    return jsonify(list_job_recommend)

@app.route('/recommendation/users/<string:job_id>', methods=['GET'])
def get_recommendation_users_by_job_id(job_id):
    list_user_recommend = get_recommendation_user_by_job(job_id)
    return jsonify(list_user_recommend)
#Hello
@app.route('/', methods=['GET'])
def hello():
    return "Hello World"

if __name__ == '__main__':
    # Khởi chạy lịch trình trong một luồng riêng biệt
    import threading
    threading.Thread(target=run_scheduler).start()
    # Khởi chạy Flask app
    app.run(debug=True)
