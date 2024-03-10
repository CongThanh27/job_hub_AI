from collaborative_filtering import CF
from handle_data import get_data
from db_connection import connect_to_mongodb
import pandas as pd 
def user_user_collaborative_filtering():
    data = get_data('data_after')
    ratings = data[['user_id_encoded','job_id_encoded','rating']]
    ratings.columns = ['user_id', 'job_id', 'rating']
    Y_data = ratings.values
    rs = CF(Y_data, k = 10, uuCF = 1)
    rs.fit()
    rs.print_recommendation()
    

def item_item_collaborative_filtering():
    data = get_data('data_after')
    ratings = data[['user_id_encoded','job_id_encoded','rating']]
    ratings.columns = ['user_id', 'job_id', 'rating']
    Y_data = ratings.values
    rs = CF(Y_data, k = 10, uuCF = 0)
    rs.fit()
    rs.print_recommendation()
    
def get_recommendation_user_by_job(job_id):
    db_mongo = connect_to_mongodb()
    collection = db_mongo['recommendations_user_by_job']
    query = {'job_id': job_id}
    result = collection.find_one(query)
    if result:
        return result['recommended_users']
    else:
        return []

def get_recommendation_job_by_user(user_id):
    db_mongo = connect_to_mongodb()
    collection = db_mongo['recommendations_job_by_user']
    query = {'user_id': user_id}
    result = collection.find_one(query)
    if result:
        return result['recommended_items']
    else:
        return []
    
    
     
    



