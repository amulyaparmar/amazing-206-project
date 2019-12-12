#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import urllib.request

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData.db')


cur.execute('DROP TABLE IF EXISTS Gtrend_MEAN')
cur.execute('DROP TABLE IF EXISTS Gtrend_DELTA')

cur.execute("CREATE TABLE Gtrend_MEAN (id INT PRIMARY KEY, name TEXT, onemonth REAL, threemonth REAL, oneday REAL, sevenday REAL, fiveyear REAL)")
cur.execute("CREATE TABLE Gtrend_DELTA (id INT PRIMARY KEY, name TEXT, onemonth REAL, threemonth REAL, oneday REAL, sevenday REAL, fiveyear REAL)")

#SETUP CANDIDATES   
candidates = [
 
["Andrew Yang", "yang2020.com"],
["Kamala Harris", "kamalaharris.org"],
["Bernie Sanders","berniesanders.com"],
["Mike Bloomberg", "www.mikebloomberg.com"],
["Joe Biden",	"joebiden.com"],
["Pete Buttigieg", "peteforamerica.com"],
["Elizabeth Warren",	"elizabethwarren.com"],
["Tulsi Gabbard", "tulsi2020.com"],
["Amy Klobucher", "amyklobuchar.com"],
["Tom Steyer", "www.tomsteyer.com/"],
["Donald Trump", "donaldjtrump.com"]
]

candidates_df = pd.DataFrame(candidates)
candidates_df.columns = ["Candidate", "Website"]

#!pip install pytrends


from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
mean = []
delta = []
candidate_count = 0;
for row in candidates:
  # print("full name: ", row[0])
  name = row[0]
  pytrends.build_payload([row[0]], cat=0, timeframe='today 1-m', geo='', gprop='')
  df = pytrends.interest_over_time()
  pytrends.build_payload([row[0]], cat=0, timeframe='today 3-m', geo='', gprop='')
  df2 = pytrends.interest_over_time()
  pytrends.build_payload([row[0]], cat=0, timeframe='now 1-d', geo='', gprop='')
  df3 = pytrends.interest_over_time()
  pytrends.build_payload([row[0]], cat=0, timeframe='now 7-d', geo='', gprop='')
  df4 = pytrends.interest_over_time()
  pytrends.build_payload([row[0]], cat=0, timeframe='today 5-y', geo='', gprop='')
  df5 = pytrends.interest_over_time()
  print('candidate: : ', row[0], " | 30 day mean: ", df[row[0]].mean() )
  print('candidate: : ', row[0], " | 90 day mean: ", df2[row[0]].mean() )
  print('candidate: : ', row[0], " | 1 day  mean: ", df3[row[0]].mean() )
  print('candidate: : ', row[0], " | 7 day mean: ", df4[row[0]].mean() )
  print('candidate: : ', row[0], " | 5 yr mean: ", df5[row[0]].mean() )
  cur.execute("INSERT INTO Gtrend_MEAN (id, name, onemonth, threemonth, oneday, sevenday, fiveyear) VALUES (?, ?, ? ,?,?, ?, ?)", (candidate_count, name, df[row[0]].mean(), df2[row[0]].mean(), df3[row[0]].mean(), df4[row[0]].mean(), df5[row[0]].mean() ))

  print('candidate: : ', row[0], " | 30 day delta: ", df.iloc[:,0][-1] - df.iloc[:,0][0] )
  print('candidate: : ', row[0], " | 90 day delta: ", df2.iloc[:,0][-1] - df2.iloc[:,0][0])
  print('candidate: : ', row[0], " | 1 day delta: ", df3.iloc[:,0][-1] - df3.iloc[:,0][0] )
  print('candidate: : ', row[0], " | 7 day delta: ", df4.iloc[:,0][-1] - df4.iloc[:,0][0] )
  print('candidate: : ', row[0], " | 5 yr delta: ", df5.iloc[:,0][-1] - df5.iloc[:,0][0] )
  cur.execute("INSERT INTO Gtrend_DELTA (id, name, onemonth, threemonth, oneday, sevenday, fiveyear) VALUES (?, ?, ? ,?,?, ?, ?)", (candidate_count, name,  df.iloc[:,0][-1] - df.iloc[:,0][0],  df2.iloc[:,0][-1] - df2.iloc[:,0][0],  df3.iloc[:,0][-1] - df3.iloc[:,0][0],  df4.iloc[:,0][-1] - df4.iloc[:,0][0],  df5.iloc[:,0][-1] - df5.iloc[:,0][0] ))

  candidate_count += 1
  #mean.append(df[row[0]].mean())
  # print('delta: ', df.iloc[:,0][-1] - df.iloc[:,0][0])
  #delta.append(df.iloc[:,0][-1] - df.iloc[:,0][0])

