# In[ ]:


#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import urllib.request


1
# In[ ]:



def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData1.db')


# In[ ]:



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

candidate_df = pd.DataFrame(candidates)
candidate_df = candidate_df.rename(columns={0: "Candidate", 1: 'Website', 2: 'Twitter Handle'}, errors="raise")


# In[ ]:

#VISUALIZATIONS

cur.execute("SELECT * FROM WebsiteData WHERE category='Pageviews Over 1 Month'")
df = pd.DataFrame(cur.fetchall())

df = df.rename(columns={1: "Candidate", 2: 'Website Statistic', 3: "Pageviews Over 1 Month (per 100k)"}, errors="raise")


df = df.set_index("Candidate")
df = df.iloc[:, 2:]
df = df * 10

cur.execute("SELECT * FROM Gtrend_MEAN")
df2 = pd.DataFrame(cur.fetchall())
df2 = df2.rename(columns={1: 'Candidate', 2: "Google Trends Mean over 1 Month", 3: "Three Month Mean", 4: "One Day Mean",  5: "Seven Day Mean",  6: "Five Year Mean"}, errors="raise")

df2 = df2.set_index('Candidate')
df2 = df2.iloc[:, 1:]

#df.iloc[1] = df.iloc[:,1] * 100

combined_df = df.merge(df2, left_on='Candidate', right_on='Candidate')

pageviews_vs_gtrends = combined_df.iloc[:, [0, 1]]
corr = pageviews_vs_gtrends.corr(method='pearson')
print(corr)

combined_df.iloc[:, [0, 1]].plot(kind="bar", title="Average Google Trend & Website Pageviews Score across Candidatess | Corr {}".format(corr.iloc[0,1]))



ax = combined_df.iloc[:, [0, 1]].plot(kind="bar", title="Average Google Trend & Website Pageviews Score across Candidates | Corr {}".format(corr.iloc[0,1]))
fig = ax.get_figure()
fig.savefig('avg_gtrend_vs_pageviews.png')
 

# In[ ]:


#cur.execute("SELECT DISTINCT name, avg(percent) FROM DemPrimary WHERE name='Kamala Harris'")
cur.execute("SELECT name, AVG(percent) FROM DemPrimary GROUP BY name")
df3 = pd.DataFrame(cur.fetchall())

df3 = df3.rename(columns={0: "Candidate", 1: 'Average Polling Percentage'}, errors="raise")

df3 = df3.set_index("Candidate")
df3

combined_df = combined_df.merge(df3, left_on='Candidate', right_on='Candidate')
combined_df

combined_df.iloc[:, [0, 1, 6]].plot(kind="bar", title="Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")

data = combined_df.iloc[:, [0, 1, 6]]
corr = data.corr(method='pearson')
print(corr)

ax = combined_df.iloc[:, [0, 1, 6]].plot(kind="bar", title="Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")
fig = ax.get_figure()
fig.savefig('avg_gtrend_vs_pageviews_vs_polling_statistics_dems.png')

# In[ ]:


cur.execute("SELECT * FROM DemPrimary")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM DemGeneral")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM Gtrend_MEAN")
results = cur.fetchall()  

df = pd.DataFrame(results)

df = df.set_index(1)
df = df.iloc[:, 1:]
df = df.rename(columns={2: "One Month Mean", 3: "Three Month Mean", 4: "One Day Mean",  5: "Seven Day Mean",  6: "Five Year Mean"}, errors="raise")
df


# In[ ]:


#one month delta
df.iloc[:, [0,1,3]].plot(kind="bar", title="Average Google Trend Score across Candidates")
ax = df.iloc[:, [0,1,3]].plot(kind="bar", title="Average Google Trend Score across Candidates")
fig = ax.get_figure()
fig.savefig('avg_gtrend_all_candidates.png')

df

# In[ ]:



cur.execute("SELECT * FROM Gtrend_DELTA")
results = cur.fetchall()  

df = pd.DataFrame(results)

df = df.set_index(1)
df = df.iloc[:, 1:]
df = df.rename(columns={2: "One Month Delta", 3: "Three Month Delta", 4: "One Day Delta",  5: "Seven Day Delta",  6: "Five Year Delta"}, errors="raise")
df


# In[ ]:
df.iloc[:, [0,1,3]].plot(kind="bar", title="Delta in Google Trend Searches across Candidates")




# %%

#BONUS API & CALCULCATION & PRINT OUTPUT


import tweepy
import numpy as np

consumer_key = "nDbRA7vy5j0nxhBtZloHn7xee"
consumer_secret = "aIEVKKPeFjbjqZoyjRObUoMSsTcTXzxfzrBWr4g8T9coIUyNev"
access_token = "703356714-BaFvjE2YkCCB5zJkyFZCCNDTfnmWnwSVKEXh7cXR"
access_token_secret = "N75fvl0rPehgtO7v5oNZcdI3GAUzqGMqhnmcMVW3ttWGM"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

candidate_df = candidate_df.set_index("Candidate")
candidate_df['Twitter Followers'] = np.nan

for index, val in candidate_df["Twitter Handle"].iteritems():
    user = api.get_user(val)
    candidate_df['Twitter Followers'][index] = user.followers_count / 1000000


# %%

combined_df = combined_df.merge(candidate_df, left_on='Candidate', right_on="Candidate")
combined_df.head()


# %%

# %%
data2 = combined_df.loc[:, ['Average Polling Percentage', 'Twitter Followers']]
corr = data2.corr(method='pearson')
print("Correlation between Twitter Followers & Avg. Polling Perc: ", corr.iloc[1, 0])
# %%
ax = combined_df.loc[:, ['Candidate','Average Polling Percentage', 'Twitter Followers']].set_index("Candidate").plot(kind="bar", title="Average Polling Percentages vs Twitter Followers (per million) | Corr: {}".format(corr.iloc[1, 0]))
fig = ax.get_figure()
fig.savefig('twitter_vs_polling.png')


# %%

# %%
