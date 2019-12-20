#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import urllib.request
from datetime import datetime

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData.db')


cur.execute('DROP TABLE IF EXISTS Gtrend_MEAN')
cur.execute('DROP TABLE IF EXISTS Gtrend_DELTA')

cur.execute("CREATE TABLE Gtrend_MEAN (row_number INT PRIMARY KEY, id INT, name TEXT, time_period TEXT, score REAL)")
cur.execute("CREATE TABLE Gtrend_DELTA (row_number INT PRIMARY KEY, id INT, name TEXT, time_period TEXT, score REAL)")

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

pytrends = TrendReq(hl='en-US', tz=360, retries=20, backoff_factor=10)
mean = []
delta = []
candidate_count = 0
row_number=0
delta_row_number=0
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
  pytrends.build_payload([row[0]], cat=0, timeframe='2015-12-19 2019-12-19', geo='', gprop='')
  df7 = pytrends.interest_over_time() 
  pytrends.build_payload([row[0]], cat=0, timeframe='2016-12-19 2019-12-19', geo='', gprop='')
  df8 = pytrends.interest_over_time() 
  pytrends.build_payload([row[0]], cat=0, timeframe='2017-12-19 2019-12-19', geo='', gprop='')
  df9 = pytrends.interest_over_time() 
  pytrends.build_payload([row[0]], cat=0, timeframe='2018-12-18 2019-12-18', geo='', gprop='')
  df10 = pytrends.interest_over_time() 
  pytrends.build_payload([row[0]], cat=0, timeframe='2019-11-27 2019-12-18', geo='', gprop='')
  df11 = pytrends.interest_over_time() 

  print('candidate: : ', row[0], " | 1 day  mean: ", df3[row[0]].mean() )
  print('candidate: : ', row[0], " | 7 day mean: ", df4[row[0]].mean() )
  print('candidate: : ', row[0], " | 30 day mean: ", df[row[0]].mean() )
  print('candidate: : ', row[0], " | 90 day mean: ", df2[row[0]].mean() )
  print('candidate: : ', row[0], " | 5 yr mean: ", df5[row[0]].mean() )
  
  


  #cur.execute("INSERT INTO Gtrend_MEAN (id, name, onemonth, threemonth, oneday, sevenday, fiveyear) VALUES (?, ?, ? ,?,?, ?, ?)", (candidate_count, name, df[row[0]].mean(), df2[row[0]].mean(), df3[row[0]].mean(), df4[row[0]].mean(), df5[row[0]].mean() ))
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "one day", df3[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "seven days", df4[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "three weeks", df11[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number,candidate_count, name, "one month", df[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number,candidate_count, name, "three months", df2[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "three years", df8[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "one year", df10[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "two years", df9[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "three years", df8[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "four years", df7[row[0]].mean()))
  row_number+=1
  cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "five years", df5[row[0]].mean()))
  row_number+=1
  
  if (row[0]=="Kamala Harris"):
    pytrends.build_payload([row[0]], cat=0, timeframe='2019-12-01 2019-12-08', geo='', gprop='')
    df6 = pytrends.interest_over_time()
    for i in range(0,len(df6)):
      cur.execute("INSERT INTO Gtrend_MEAN (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(row_number, candidate_count, name, "December 1-8", float(df6[row[0]][i])))
      row_number+=1

 

  
  print('candidate: : ', row[0], " | 30 day delta: ",  df[row[0]][-1] - df[row[0]][0] )
  print('candidate: : ', row[0], " | 90 day delta: ",  df2[row[0]][-1] - df2[row[0]][0])
  print('candidate: : ', row[0], " | 1 day delta: ", df3[row[0]][-1] - df3[row[0]][0] )
  print('candidate: : ', row[0], " | 7 day delta: ", df4[row[0]][-1] - df4[row[0]][0] )
  print('candidate: : ', row[0], " | 5 yr delta: ", df5[row[0]][-1] - df5[row[0]][0] )

  #cur.execute("INSERT INTO Gtrend_DELTA (id, name, onemonth, threemonth, oneday, sevenday, fiveyear) VALUES (?, ?, ? ,?,?, ?, ?)", (candidate_count, name,  float(df.iloc[:,0][-1] - df.iloc[:,0][0]),  float(df2.iloc[:,0][-1] - df2.iloc[:,0][0]),  float(df3.iloc[:,0][-1] - df3.iloc[:,0][0]), float(df4.iloc[:,0][-1] - df4.iloc[:,0][0]),  float(df5.iloc[:,0][-1] - df5.iloc[:,0][0]) ))
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "one day", float(df3.iloc[:,0][-1] - df3.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "seven days", float(df4.iloc[:,0][-1] - df4.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "three weeks", float(df11.iloc[:,0][-1] - df11.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "one month", float(df.iloc[:,0][-1] - df.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number, candidate_count, name, "three months", float(df2.iloc[:,0][-1] - df2.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "one years", float(df10.iloc[:,0][-1] - df10.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "two years", float(df9.iloc[:,0][-1] - df9.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "three years", float(df8.iloc[:,0][-1] - df8.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "four years", float(df7.iloc[:,0][-1] - df7.iloc[:,0][0])))
  delta_row_number+=1
  cur.execute("INSERT INTO Gtrend_DELTA (row_number, id, name, time_period, score) VALUES (?,?,?,?,?)",(delta_row_number,candidate_count, name, "five years", float(df5.iloc[:,0][-1] - df5.iloc[:,0][0])))
  delta_row_number+=1
  
  


  candidate_count += 1
  #mean.append(df[row[0]].mean())
  # print('delta: ', df.iloc[:,0][-1] - df.iloc[:,0][0])
  #delta.append(df.iloc[:,0][-1] - df.iloc[:,0][0])

conn.commit()
