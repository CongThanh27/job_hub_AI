
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 
from db_connection import connect_to_mongodb

class CF(object):
   
    def __init__(self, Y_data, k, dist_func = cosine_similarity, uuCF = 1):
        self.uuCF = uuCF 
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        self.Y_data = np.nan_to_num(self.Y_data)
        # Tính số lượng người dùng
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1 
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1
    
    def add(self, new_data):
        self.Y_data = np.concatenate((self.Y_data, new_data), axis = 0)
    
    def normalize_Y(self):
        users = self.Y_data[:, 0] 
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_users,))
        for n in range(self.n_users):
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.Y_data[ids, 1] 
            ratings = self.Y_data[ids, 2]
            m = np.mean(ratings) 
            if np.isnan(m):
                m = 0 
            self.mu[n] = m
            self.Ybar_data[ids, 2] = ratings - self.mu[n]

        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
            (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        eps = 1e-6
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
    
        
    def refresh(self):
        self.normalize_Y()
        self.similarity() 
        
    def fit(self):
        self.refresh()
        
    def __pred(self, u, i, normalized = 1):

        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        sim = self.S[u, users_rated_i]
        a = np.argsort(sim)[-self.k:] 
        nearest_s = sim[a]
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)
        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]
    
    def pred(self, u, i, normalized = 1):
        if self.uuCF: return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)
             
    def recommend(self, u):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()              
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0: 
                    recommended_items.append(i)
        
        return recommended_items 
    
    def recommend2(self, u):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()              
        recommended_items = []
    
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0: 
                    recommended_items.append(i)
        
        return recommended_items 
    
    def print_recommendation(self):
        db_mongo = connect_to_mongodb()
        if self.uuCF:
            collection_user = db_mongo['recommendations_job_by_user']  
            collection_user.delete_many({})
        else: 
            collection_job = db_mongo['recommendations_user_by_job']  
            collection_job.delete_many({}) 
        # Chèn dữ liệu vào MongoDB
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                collection = db_mongo['data_after']
                query = {'user_id_encoded': u}
                result = collection.find_one(query)
                user_id = -1
                if result:
                    user_id = result['user_id']
                 
                query = {'job_id_encoded': {'$in': recommended_items}}
                results1 = collection.find(query)

                job_ids = []
               
                for result_for in results1:
                    job_ids.append(result_for['job_id'])
                collection_user_new = db_mongo['recommendations_job_by_user']             
                recommendation_data = {
                    'user_id': user_id,
                    'recommended_items': job_ids
                }
                collection_user_new.insert_one(recommendation_data)
                
            else: 
                collection = db_mongo['data_after']
            
                query = {'job_id_encoded': u}
                result = collection.find_one(query)
                job_id = -1
                if result:
                    job_id = result['job_id']
                  
                query = {'user_id_encoded': {'$in': recommended_items}}
                results1 = collection.find(query)
              
                user_ids = []
               
                for result_for in results1:
                    user_ids.append(result_for['job_id'])
                collection_job_new = db_mongo['recommendations_user_by_job']     
                recommendation_data1 = {
                    'job_id': job_id,
                    'recommended_users': user_ids
                }
                collection_job_new.insert_one(recommendation_data1)
        db_mongo.client.close()        
                

