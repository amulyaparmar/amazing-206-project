#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import urllib.request

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData.db')


candidates = [
 
["Andrew Yang", "yang2020.com"],
["Kamala Harris", "kamalaharris.org"],
["Bernie Sanders","berniesanders.com"],
["Mike Bloomberg", "mikebloomberg.com"],
["Joe Biden",	"joebiden.com"],
["Pete Buttigieg", "peteforamerica.com"],
["Elizabeth Warren",	"elizabethwarren.com"],
["Tulsi Gabbard", "tulsi2020.com"],
["Amy Klobucher", "amyklobuchar.com"],
["Tom Steyer", "tomsteyer.com"],
["Donald Trump", "donaldjtrump.com"]
]


import requests

def get_sitetraffic(candidates, cur, conn):
  cur.execute("DROP TABLE IF EXISTS WebsiteData")
  cur.execute("DROP TABLE IF EXISTS WebsiteDelta")
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
    request_url    = "https://endpoint.sitetrafficapi.com/pay-as-you-go/?key=4042b83167e850cb15abd025611917b802556ddd&host={}".format(candidate_website)
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


get_sitetraffic(candidates, cur, conn)