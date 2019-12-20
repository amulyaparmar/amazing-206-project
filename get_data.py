from rcp import get_polls, get_poll_data, to_csv
import re
import sqlite3

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

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

def get_twitter(candidates):
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

    #candidate_df = candidate_df.set_index("Candidate")
    candidate_df['Twitter Followers'] = np.nan

    for index, val in candidate_df["Twitter Handle"].iteritems():
        user = api.get_user(val)
        candidate_df['Twitter Followers'][index] = user.followers_count / 1000000
        cur.execute("INSERT INTO twitter_table (name, followers) VALUES (?,?)",(candidate_df["Candidate"][index], user.followers_count / 1000000))
        #print(candidate_df["Candidate"][index])
    conn.commit()