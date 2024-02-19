# -*- coding: utf-8 -*-
"""Twitter_Analysis.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W6I9yZN16CjzOx9vAnhdSNTq6vFL0nIO
"""

!pip install pandas
!pip install numpy
!pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
!pip install snscrape
!pip install networkx

import pandas as pd
import numpy as np
import os
import networkx as ntw
import matplotlib.pyplot as plt
import json



import snscrape.modules.twitter as sntwitter
import pandas

proVaccine_tweets = []
antiVaccine_tweets = []

for i,tweet in enumerate(sntwitter.TwitterSearchScraper('GetVaccinatedOrGetCovid').get_items()):
    if i>210:
        break
    proVaccine_tweets.append([tweet.date, tweet.id, tweet.content, tweet.username])

for i,tweet in enumerate(sntwitter.TwitterSearchScraper('SayNoToVaccines').get_items()):
    if i>210:
        break
    antiVaccine_tweets.append([tweet.date, tweet.id, tweet.content, tweet.username])

proVaccine_df = pd.DataFrame(proVaccine_tweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
proVaccine_df.to_json('proVaccine.json', orient = 'split', compression = 'infer', index = 'true')
antiVaccine_df = pd.DataFrame(antiVaccine_tweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
antiVaccine_df.to_json('antiVaccine.json', orient = 'split', compression = 'infer', index = 'true')





import json
import re
import nltk
from nltk import bigrams
from nltk.corpus import stopwords
nltk.download('stopwords')
import itertools
import collections
import matplotlib.pyplot as plt

def readJsonReturnBigrams(file):
  tweet_df = pd.read_json(file, orient ='split', compression = 'infer')
  tweets = tweet_df.to_json(orient = 'split')
  tweets_json = json.loads(tweets)
  tweet_data = tweets_json["data"]
  tweet_words = [tweet[2].lower().split() for tweet in tweet_data]
  stop_words = set(stopwords.words('english'))
  final_words = [[word for word in words if not word in stop_words]
              for words in tweet_words]
  co_occurence = [list(bigrams(tweet)) for tweet in final_words]
  bigramsList = list(itertools.chain(*co_occurence))
  occurence_count = collections.Counter(bigramsList).most_common(250)
  occurence_df = pd.DataFrame(occurence_count,
                             columns=['words', 'occurence'])
  return occurence_df.set_index('words').T.to_dict('records')


antiVaccineWords = readJsonReturnBigrams('antiVaccine.json')
proVaccineWords = readJsonReturnBigrams('proVaccine.json')

AntiGraph = ntw.DiGraph()
for k, v in antiVaccineWords[0].items():
    AntiGraph.add_node(k[0])
    AntiGraph.add_node(k[1])
    AntiGraph.add_edge(k[0], k[1])

ntw.draw(
    AntiGraph,
    with_labels=True
)
plt.rcParams["figure.figsize"] = (30,40)
plt.show()
plt.savefig('Anti_Vaccine.png')
ProGraph = ntw.DiGraph()
for k, v in proVaccineWords[0].items():
    ProGraph.add_node(k[0])
    ProGraph.add_node(k[1])
    ProGraph.add_edge(k[0], k[1])
ntw.draw(
    ProGraph,
    with_labels=True
)
plt.show()
plt.savefig('Pro_Vaccine.png')



import collections

def networkMeasures(network):
  deg_seq = sorted([d for n, d in network.in_degree()])
  count = collections.Counter(deg_seq)
  deg, cnt = zip(*count.items())

  
  fig, ax = plt.subplots()
  plt.bar(deg, cnt, width=0.60, color='black')

  plt.title("Degree Distribution Histogram")
  plt.ylabel("Count")
  plt.xlabel("Degree")
  plt.rcParams["figure.figsize"] = (10,10)
  plt.show()
  print("clustering", ntw.clustering(network))
  print("Closeness centrality", ntw.closeness_centrality(network))
  print("Betweenness centrality", ntw.betweenness_centrality(network))

networkMeasures(AntiGraph)
networkMeasures(ProGraph)

