import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import urllib.request
import plotly.express as px
from rcp import get_polls, get_poll_data, to_csv
import re
import sqlite3
from pytrends.request import TrendReq
import requests

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def get_gtrends(candidates):
    cur, conn = setUpDatabase("CandidateData.db")
    candidates_df = pd.DataFrame(candidates)
    candidates_df.columns = ["Candidate", "Website"]
    cur.execute("CREATE TABLE Gtrend_MEAN (row_number INT PRIMARY KEY, id INT, name TEXT, time_period TEXT, score REAL)")
    cur.execute("CREATE TABLE Gtrend_DELTA (row_number INT PRIMARY KEY, id INT, name TEXT, time_period TEXT, score REAL)")

    #!pip install pytrends

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


def get_sitetraffic(candidates):
  cur, conn = setUpDatabase('CandidateData.db')
  cur.execute("CREATE TABLE WebsiteData (id INT PRIMARY KEY, candidate TEXT, category TEXT, score REAL)")
  cur.execute("CREATE TABLE WebsiteDelta (id INT PRIMARY KEY, candidate TEXT, category TEXT, score REAL)")
    # api_c_code  = country_code      # country code (e.g. "USA", "USA;CAN")
    # api_type    = "EN.ATM.CO2E.PC"  # CO2 emissions data (metric tons per capita)
    # api_year    = year              # year (e.g. 2000)
    # api_per_page= per_page          # maximum return items (the default value is 50)
  data_id = 0
  delta_id = 0
  for candidate in candidates:
    candidate_website = candidate[1]
    request_url    = "https://endpoint.sitetrafficapi.com/pay-as-you-go/?key=746a4db232cc1d838ee0f9634011d9062d3a1216&host={}".format(candidate_website)
    data = requests.get(request_url).json()
    print(data)
    print(candidate[0])
    score = data['data']['estimations']['visitors']['daily']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Daily Visitors', score))
      data_id += 1
    score = data['data']['estimations']['visitors']['monthly']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Monthly Visitors', score))
      data_id += 1
    score = data['data']['estimations']['visitors']['yearly']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Yearly Visitors', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['daily']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Daily Pageviews', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['monthly']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Monthly Pageviews', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['yearly']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Yearly Pageviews', score))
      data_id += 1
    score = data['data']['alexa']['rank']['3_months']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Rank Over 3 Months', score))
      data_id += 1
    score = data['data']['alexa']['rank']['1_month']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Rank Over 1 Month', score))
      data_id += 1
    score = data['data']['alexa']['rank']['7_days']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Rank Over 1 Week', score))
      data_id += 1
    score = data['data']['alexa']['rank']['1_day']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Rank Over 1 Day', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['3_months']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 3 Months', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['1_month']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 1 Month', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['7_days']
    if (score != None):
      score = float(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 1 Week', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['1_day']
    if (score != None):
      score = float(score.replace(',',''))    
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 1 Day', score))
      data_id += 1
    score = data['data']['alexa']['reach']['3_months']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Reach Over 3 Months', score))
      data_id += 1
    score = data['data']['alexa']['reach']['1_month']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Reach Over 1 Month', score))
      data_id += 1
    score = data['data']['alexa']['reach']['7_days']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Reach Over 1 Week', score))
      data_id += 1
    score = data['data']['alexa']['reach']['1_day']
    if (score != None):
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Reach Over 1 Day', score))
      data_id += 1
    score = data['data']['alexa']['rank_delta']['3_months']
    if (score != None):
      if (score[0] == '+'):
        score = score[1:]
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Rank Over 3 Months', score))
    delta_id += 1
    score = data['data']['alexa']['rank_delta']['1_month']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Rank Over 1 Month', score))
    delta_id += 1
    score = data['data']['alexa']['rank_delta']['7_days']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Rank Over 1 Week', score))
    delta_id += 1
    score = data['data']['alexa']['rank_delta']['1_day']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Rank Over 1 Day', score))
    delta_id += 1
    score = data['data']['alexa']['pageviews_delta']['3_months']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Pageviews Over 3 Months', score))
    delta_id += 1
    score = data['data']['alexa']['pageviews_delta']['1_month']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Pageviews Over 1 Month', score))
    delta_id += 1
    score = data['data']['alexa']['pageviews_delta']['7_days']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Pageviews Over 1 Week', score))
    delta_id += 1
    score = data['data']['alexa']['pageviews_delta']['1_day']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Pageviews Over 1 Day', score))
    delta_id += 1    
    score = data['data']['alexa']['reach_delta']['3_months']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 3 Months', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['1_month']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 1 Month', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['7_days']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 1 Week', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['1_day']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 1 Day', score))
    delta_id += 1
  conn.commit()

def get_real_clear_politics(candidates):
  cur, conn = setUpDatabase('CandidateData.db')
  cur.execute("SELECT count(name) FROM sqlite_master WHERE type=? AND name=?", ('table', 'DemPrimary'))
  if cur.fetchone()[0] != 1:
    cur.execute("CREATE TABLE DemPrimary (id INT PRIMARY KEY, name TEXT, percent REAL)")
  data = get_poll_data('https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html', csv_output=False)
  test_data = get_poll_data('https://www.realclearpolitics.com/epolls/2020/president/mi/michigan_trump_vs_sanders-6768.html')
  trump_links = {"Joe Biden": ["https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_biden-6247.html", "https://www.realclearpolitics.com/epolls/2020/president/nh/new_hampshire_trump_vs_biden-6779.html", "https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_biden-6755.html", "https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_biden-6849.html", "https://www.realclearpolitics.com/epolls/2020/president/nv/nevada_trump_vs_biden-6867.html", "https://www.realclearpolitics.com/epolls/2020/president/nc/north_carolina_trump_vs_biden-6744.html", "https://www.realclearpolitics.com/epolls/2020/president/pa/pennsylvania_trump_vs_biden-6861.html"],
                "Bernie Sanders": ["https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_sanders-6250.html", "https://www.realclearpolitics.com/epolls/2020/president/nh/new_hampshire_trump_vs_sanders-6780.html", "https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_sanders-6880.html", "https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_sanders-6850.html", "https://www.realclearpolitics.com/epolls/2020/president/nv/nevada_trump_vs_sanders-6868.html", "https://www.realclearpolitics.com/epolls/2020/president/nc/north_carolina_trump_vs_sanders-6745.html"],
                "Elizabeth Warren": ["https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_warren-6251.html", "https://www.realclearpolitics.com/epolls/2020/president/nh/new_hampshire_trump_vs_warren-6781.html", "https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_warren-6756.html", "https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_warren-6852.html", "https://www.realclearpolitics.com/epolls/2020/president/nv/nevada_trump_vs_warren-6870.html", "https://www.realclearpolitics.com/epolls/2020/president/nc/north_carolina_trump_vs_warren-6746.html"],
                "Pete Buttigieg": ["https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_buttigieg-6872.html", "https://www.realclearpolitics.com/epolls/2020/president/nh/new_hampshire_trump_vs_buttigieg-6981.html", "https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_buttigieg-6937.html", "https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_buttigieg-6970.html", "https://www.realclearpolitics.com/epolls/2020/president/nv/nevada_trump_vs_buttigieg-6871.html", "https://www.realclearpolitics.com/epolls/2020/president/nc/north_carolina_trump_vs_buttigieg-6907.html"],
                "Kamala Harris": ["https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_harris-6252.html", "https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_harris-6759.html", "https://www.realclearpolitics.com/epolls/2020/president/ga/georgia_trump_vs_harris-6978.html"],
                "Andrew Yang": ["https://www.realclearpolitics.com/epolls/2020/president/nh/new_hampshire_trump_vs_yang-6947.html"],
                "Amy Klobuchar": ["https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_klobuchar-6854.html"],
                "Mike Bloomberg": ["https://www.realclearpolitics.com/epolls/2020/president/ca/california_trump_vs_bloomberg-6985.html","https://www.realclearpolitics.com/epolls/2020/president/us/general_election_trump_vs_bloomberg-6797.html"],
                "Cory Booker": ["https://www.realclearpolitics.com/epolls/2020/president/wi/wisconsin_trump_vs_booker-6982.html"] }
  candidate_count = 0
  poll_count = 0
  cur.execute("SELECT * from DemPrimary WHERE name =?", ('Joe Biden',))
  current_prim_source = len(cur.fetchall())
  cur.execute("SELECT * from DemPrimary")
  prim_count = len(cur.fetchall())
  if (current_prim_source < len(data[0]['data'])):
    for candidate in candidates:
      name = candidate[0]
      if (name != "Donald Trump"):
        surname = re.findall(r"\w+\s(\w+)", name)[0]
        prim_percent = data[0]['data'][current_prim_source].get(surname)
        if ((prim_percent == None) or (prim_percent == '--')):
          continue
        cur.execute("INSERT INTO DemPrimary (id, name, percent) VALUES (?,?,?)", (prim_count, name, prim_percent))
        prim_count += 1      
  else:
    starting_link = ""
    found_start = True
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type=? AND name=?", ('table', 'DemGeneral'))
    if cur.fetchone()[0] != 1:
      cur.execute("CREATE TABLE DemGeneral (id INT PRIMARY KEY, name TEXT, dem_percent REAL, trump_percent REAL, url TEXT)")
    else:
      cur.execute("SELECT url FROM DemGeneral ORDER BY id DESC")
      starting_link = cur.fetchone()[0]
      found_start = False
    cur.execute("SELECT * from DemGeneral")
    past_total = len(cur.fetchall())
    poll_count = past_total
    for candidate in candidates:
      starting_index = 0
      if ((poll_count - past_total) >= 20):
        continue
      name = candidate[0]
      print(name + ": " + str(poll_count - past_total))
      if (name != "Donald Trump"):
        surname = re.findall(r"\w+\s(\w+)", name)[0]
        if (trump_links.get(name) == None):
          continue
        if ((found_start == False) and (starting_link in trump_links[name])):
          found_start = True
          for i in range(len(trump_links[name])):
            if (trump_links[name][i] == starting_link):
              starting_index = i + 1
        elif ((found_start == False) and (starting_link not in trump_links[name])):
          continue
        if (starting_index >= len(trump_links[name])):
          continue
        remaining_polls = trump_links[name][starting_index:]
        # print(remaining_polls)
        for poll in remaining_polls:
          trump_data = get_poll_data(poll)
          for poll_source in trump_data[0]['data']:
            if ((poll_count - past_total) >= 20):
              continue
            dem_percent = poll_source.get(surname + ' (D)', 0.0)
            trump_percent = poll_source['Trump (R)']
            cur.execute("INSERT INTO DemGeneral (id, name, dem_percent, trump_percent, url) VALUES (?,?,?,?,?)", (poll_count, name, dem_percent, trump_percent, poll))
            poll_count += 1
  conn.commit()   

def get_twitter():
    candidates = [
    
    ["Andrew Yang", "yang2020.com", "AndrewYang"],
    ["Kamala Harris", "kamalaharris.org", "KamalaHarris"],
    ["Bernie Sanders","berniesanders.com", "BernieSanders"],
    ["Mike Bloomberg", "mikebloomberg.com", "MikeBloomberg"],
    ["Joe Biden",	"joebiden.com", "JoeBiden"],
    ["Pete Buttigieg", "peteforamerica.com", "PeteButtigieg"],
    ["Elizabeth Warren",	"elizabethwarren.com", "ewarren"],
    ["Tulsi Gabbard", "tulsi2020.com", "TulsiGabbard"],
    ["Amy Klobucher", "amyklobuchar.com", "amyklobuchar"],
    ["Tom Steyer", "tomsteyer.com", "TomSteyer"],
    ["Donald Trump", "donaldjtrump.com","realDonaldTrump"]
    ]
    cur, conn = setUpDatabase('CandidateData.db')
    cur.execute("CREATE TABLE twitter_table (name TEXT, followers REAL)")
    import tweepy
    import numpy as np

    consumer_key = "nDbRA7vy5j0nxhBtZloHn7xee"
    consumer_secret = "aIEVKKPeFjbjqZoyjRObUoMSsTcTXzxfzrBWr4g8T9coIUyNev"
    access_token = "703356714-BaFvjE2YkCCB5zJkyFZCCNDTfnmWnwSVKEXh7cXR"
    access_token_secret = "N75fvl0rPehgtO7v5oNZcdI3GAUzqGMqhnmcMVW3ttWGM"


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    candidate_df = pd.DataFrame(candidates)
    candidate_df = candidate_df.rename(columns={0: "Candidate", 1: 'Website', 2: 'Twitter Handle'}, errors="raise")
    #candidate_df = candidate_df.set_index("Candidate")
    candidate_df['Twitter Followers'] = np.nan

    for index, val in candidate_df["Twitter Handle"].iteritems():
        user = api.get_user(val)
        candidate_df['Twitter Followers'][index] = user.followers_count / 1000000
        cur.execute("INSERT INTO twitter_table (name, followers) VALUES (?,?)",(candidate_df["Candidate"][index], user.followers_count / 1000000))
        #print(candidate_df["Candidate"][index])
    conn.commit()

def main():
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
    ["Tom Steyer", "www.tomsteyer.com"],
    ["Donald Trump", "donaldjtrump.com"]
    ]

    get_gtrends(candidates)
    for i in range(100):
        get_real_clear_politics(candidates)
    get_twitter()
    get_sitetraffic(candidates)

if __name__ == "__main__":
    main()