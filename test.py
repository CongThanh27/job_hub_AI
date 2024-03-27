import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyodbc
print(pyodbc.drivers())

import pyodbc
import csv
import pandas as pd

# Chuỗi kết nối SQL Server
server = 'job-hub-kltn.database.windows.net'
database = 'job-hub-database'
username = 'jobhub'
password = '28072002Thanh'
driver = '{ODBC Driver 17 for SQL Server}'

# Tạo chuỗi kết nối
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Kết nối đến cơ sở dữ liệu
conn = pyodbc.connect(connection_string)

# Tạo một đối tượng cursor để thực thi các truy vấn SQL
cursor = conn.cursor()

# Ví dụ truy vấn SQL
query = """
SELECT * FROM job
"""
cursor.execute(query)

# Lấy tất cả các hàng từ cursor
rows = cursor.fetchall()

# Ghi dữ liệu vào tệp CSV
with open('data_sql.csv', 'w', newline='', encoding='utf-8') as f:
    # Tạo đối tượng ghi CSV
    writer = csv.writer(f)
    
    # Ghi tiêu đề của các cột
    writer.writerow([column[0] for column in cursor.description])
    
    # Ghi dữ liệu từ các hàng
    writer.writerows(rows)

# Đóng kết nối đến cơ sở dữ liệu
conn.close()

# Đọc dữ liệu từ tệp CSV vào DataFrame
job_df = pd.read_csv('data_sql.csv')

songs = job_df

songs['name'] = songs['name'].str.replace(r'\n', '')

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')

lyrics_matrix = tfidf.fit_transform(songs['name'])

cosine_similarities = cosine_similarity(lyrics_matrix) 

similarities = {}

for i in range(len(cosine_similarities)):
    # Now we'll sort each element in cosine_similarities and get the indexes of the songs. 
    similar_indices = cosine_similarities[i].argsort()[:-50:-1] 
    # After that, we'll store in similarities each name of the 50 most similar songs.
    # Except the first one that is the same song.
    similarities[songs['name'].iloc[i]] = [(cosine_similarities[i][x], songs['name'][x], songs['position_position_id'][x]) for x in similar_indices][1:]


class ContentBasedRecommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix

    def _print_message(self, song, recom_song):
        rec_items = len(recom_song)
        
        print(f'The {rec_items} recommended songs for {song} are:')
        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score") 
            print("--------------------")
        
    def recommend(self, recommendation):
        # Get song to find recommendations for
        song = recommendation['song']
        # Get number of songs to recommend
        number_songs = recommendation['number_songs']
        # Get the number of songs most similars from matrix similarities
        recom_song = self.matrix_similar[song][:number_songs]
        # print each item
        self._print_message(song=song, recom_song=recom_song)

recommedations = ContentBasedRecommender(similarities)

recommendation = {
    "song": songs['name'].iloc[13],
    "number_songs": 10

}


recommendation

recommedations.recommend(recommendation)