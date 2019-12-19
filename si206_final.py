# -*- coding: utf-8 -*-
"""SI206-FINAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tlqv7GDjZyp7DS6RP6CjRlrAGJbG5iiH
"""

#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import urllib.request
import plotly.express as px

# from google.colab import files
# files.upload()

#library and API import statements
#NOTE: WE WILL NEED USE CACHING WITH API REQUESTS for https://www.sitetrafficapi.com/ | Google Trends (pytrends)

#https://docs.google.com/spreadsheets/d/1yYtDt0Eg6-u8GrPw0f7kru1ru-cd5HefIojkdyUn6ds/edit#gid=0

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

candidates_df.head()

def sample(df) :

    my_new_row = []

    for index, row in df.iterrows():
      #it is easy to access a single row at a time
      print(index, " ", row) 

      #to create a new column it is easy just type the name of the column and voila
      my_new_row.append( row['Website'] + 'Amulya' )

    df['demo'] = my_new_row
    return df


sample(candidates_df).head()
#once done just save it to the original df



#WHAT IS THE OPTIMIZED WAY OF ORGANIZING ALL OUR WORK HERE

#WHAT DO WE CACHE. WE SHOULD BE ABLE TO SAVE MORE WORK 
# import sqlite3
# import pandas as pd
# # Create your connection.
# cnx = sqlite3.connect('file.db')

# df = pd.read_sql_query("SELECT * FROM table_name", cnx)

# !pip install pytrends

from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

#GOOGLE TRENDS

mean = []
delta = []

for row in candidates:
  # print("full name: ", row[0])
  pytrends.build_payload([row[0]], cat=0, timeframe='today 1-m', geo='', gprop='')
  df = pytrends.interest_over_time()
  print(df)
  mean.append(df[row[0]].mean())
  # print('delta: ', df.iloc[:,0][-1] - df.iloc[:,0][0])
  delta.append(df.iloc[:,0][-1] - df.iloc[:,0][0])

print(mean[1])

candidates_df['mean_30_days'] = mean
candidates_df['delta_30_days'] = delta


candidates_df['mean_30_days'].tolist()

# layout = go.Layout(title='Mean Interest Over 30 Days')
fig = go.FigureWidget(data=go.Bar( x=candidates_df['Candidate'],y=candidates_df['mean_30_days'] ))
fig.layout.title = 'Mean Interest in Candidates Over 30 Days'
fig.update_layout(title_x=0.5)
fig.update_layout(xaxis_title="Candidate", yaxis_title="Interest")

fig.show()

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data. 
    If the file doesn’t exist, it returns an empty dictionary.
    """

    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
    except:
        CACHE_DICTION = {}
    
    return CACHE_DICTION

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
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Daily Visitors', score))
      data_id += 1
    score = data['data']['estimations']['visitors']['monthly']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Monthly Visitors', score))
      data_id += 1
    score = data['data']['estimations']['visitors']['yearly']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Yearly Visitors', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['daily']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Daily Pageviews', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['monthly']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Monthly Pageviews', score))
      data_id += 1
    score = data['data']['estimations']['pageviews']['yearly']
    if (score != None):
      score = int(score.replace(',',''))
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
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 3 Months', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['1_month']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 1 Month', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['7_days']
    if (score != None):
      score = int(score.replace(',',''))
      cur.execute("INSERT INTO WebsiteData (id, candidate, category, score) VALUES (?,?,?,?)", (data_id, candidate[0], 'Pageviews Over 1 Week', score))
      data_id += 1
    score = data['data']['alexa']['pageviews']['1_day']
    if (score != None):
      score = int(score.replace(',',''))    
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
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reacb Over 3 Months', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['1_month']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 1 Month', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['7_days']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Reach Over 1 Week', score))
    delta_id += 1
    score = data['data']['alexa']['reach_delta']['1_day']
    cur.execute("INSERT INTO WebsiteDelta (id, candidate, category, score) VALUES (?,?,?,?)", (delta_id, candidate[0], 'Recah Over 1 Day', score))
    delta_id += 1
  conn.commit()

# get_data_with_caching("https://yang2020.com/")

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

# !pip install realclearpolitics

from rcp import get_polls, get_poll_data, to_csv
import re
import sqlite3

def get_real_clear_politics(candidates, cur, conn):
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


# cur, conn = setUpDatabase('CandidateData.db')
# get_real_clear_politics(candidates, cur, conn)

cur, conn = setUpDatabase('CandidateData1.db')
cur.execute("SELECT candidate, category, score  FROM WebsiteData WHERE category='Yearly Visitors'")
yearly_visitor= cur.fetchall()
yearly_df = pd.DataFrame(yearly_visitor)
yearly_df.columns = ["Candidate", "Category", "Yearly Visitors"]
print(yearly_df)
print(yearly_visitor)
fig = go.FigureWidget(data=go.Bar( x=yearly_df['Candidate'],y=yearly_df['Yearly Visitors'] ))
fig.layout.title = 'Yearly Visitors to Candidates\' Sites'
fig.update_layout(title_x=0.5)
fig.update_layout(xaxis_title="Candidate", yaxis_title="Yearly Visitors")
fig.show()


primary_averages = []
for candidate in candidates:
  name = candidate[0]
  cur.execute("SELECT * FROM DemPrimary WHERE name=?", (name,))
  average = 0
  results = cur.fetchall()
  if (len(results) != 0):
    for row in results:
      average += row[2]
    average /= len(results)
    primary_averages.append((name, average))
print(primary_averages)
primary_df = pd.DataFrame(primary_averages)
primary_df.columns = ["Candidate", "Average Percent"]
print(primary_df)

fig_prim = go.FigureWidget(data=go.Bar( x=primary_df['Candidate'],y=primary_df['Average Percent'] ))
fig_prim.layout.title = 'Average Percent Support of Candidates in the Primary'
fig_prim.update_layout(title_x=0.5)
fig_prim.update_layout(xaxis_title="Candidate", yaxis_title="Average Percent Support")
fig_prim.show()

general_averages = []
for candidate in candidates:
  name = candidate[0]
  cur.execute("SELECT * FROM DemGeneral WHERE name=?", (name,))
  dem_average = 0
  trump_average = 0
  results = cur.fetchall()
  if (len(results) != 0):
    for row in results:
      dem_average += row[2]
      trump_average += row[3]
    dem_average /= len(results)
    trump_average /= len(results)      
    general_averages.append((name, dem_average, trump_average))
gen_df = pd.DataFrame(general_averages)
gen_df.columns = ["Democrat", "Democrat Percent", "Trump Percent"]  

gen_fig = go.Figure(data=[
    go.Bar(name='Candidate Percent', x=gen_df["Democrat"], y=gen_df["Democrat Percent"]),
    go.Bar(name='Trump Percent', x=gen_df["Democrat"], y=gen_df["Trump Percent"])
])
gen_fig.layout.title = 'Average Percent Support of Democrat Candidates Against Trump in the Primary'
# Change the bar mode
gen_fig.update_layout(barmode='group')
gen_fig.update_layout(title_x=0.5)
gen_fig.update_layout(xaxis_title="Candidate", yaxis_title="Average Percent Support")
gen_fig.show()