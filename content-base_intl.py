import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyodbc
import csv
import pandas as pd

from db_connection import connect_to_mongodb

class ContentBasedRecommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix

    def _print_message(self, job, recom_job):
        rec_items = len(recom_job)
        
        print(f'The {rec_items} recommended job for {job} are:')
        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(f"{recom_job[i][1]} by {recom_job[i][2]} with {round(recom_job[i][0], 3)} similarity score") 
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