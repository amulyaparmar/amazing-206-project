# In[ ]:


#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import urllib.request
from textwrap import wrap


1
# In[ ]:



def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData.db')


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

# cur.execute("SELECT * FROM Gtrend_MEAN WHERE time_period = 'two years' ")
# df2 = pd.DataFrame(cur.fetchall())
# df2 



cur.execute("""

SELECT 
*
FROM
(SELECT * FROM Gtrend_MEAN WHERE time_period = 'one month') as t1
INNER JOIN
(SELECT * FROM Gtrend_MEAN WHERE time_period = 'three months') as t2
ON t1.name = t2.name


""")

df2 = pd.DataFrame(cur.fetchall())[[2, 4, 9]]


df2 = df2.rename(columns={2: 'Candidate', 4: "Google Trends Mean over 1 Month", 9: "Three Month Mean", }, errors="raise")


df2 = df2.set_index('Candidate')
# df2 = df2.iloc[:, 1:]

#df.iloc[1] = df.iloc[:,1] * 100


combined_df = df.merge(df2, left_on='Candidate', right_on='Candidate')
combined_df

pageviews_vs_gtrends = combined_df
corr = pageviews_vs_gtrends.corr(method='pearson')
corr.head()

ax = combined_df.iloc[:, [0, 1]].plot(kind="bar", title="\n".join(wrap("Average Google Trend & Website Pageviews Score across Candidates | Corr {}".format(corr.iloc[0,1]))))
title = ax.set_title("\n".join(wrap("Average Google Trend & Website Pageviews Score across Candidates | Corr {}".format(corr.iloc[0,1]), 60)))

fig = ax.get_figure()
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig('avg_gtrend_vs_pageviews.png')
 



# In[ ]:


#cur.execute("SELECT DISTINCT name, avg(percent) FROM DemPrimary WHERE name='Kamala Harris'")
cur.execute("SELECT name, AVG(percent) FROM DemPrimary GROUP BY name")
df4 = pd.DataFrame(cur.fetchall())

df4 = df4.rename(columns={0: "Candidate", 1: 'Average Polling Percentage'}, errors="raise")

df4 = df4.set_index("Candidate")
df4

combined_df = combined_df.merge(df4, left_on='Candidate', right_on='Candidate')
combined_df

combined_df.loc[:, ['Google Trends Mean over 1 Month', 'Average Polling Percentage', 'Pageviews Over 1 Month (per 100k)']].plot(kind="bar", title="Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")

data = combined_df.loc[:, ['Google Trends Mean over 1 Month', 'Average Polling Percentage', 'Pageviews Over 1 Month (per 100k)']]
corr = data.corr(method='pearson')
print(corr)

# ax = combined_df.loc[:, ['Google Trends Mean over 1 Month', 'Average Polling Percentage', 'Pageviews Over 1 Month (per 100k)']].plot(kind="bar", title="Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")
# fig = ax.get_figure()
# fig.tight_layout()
# fig.subplots_adjust(top=0.88) 
# fig.savefig('avg_gtrend_vs_pageviews_vs_polling_statistics_dems.png')

#ax = combined_df.loc[:, ['Google Trends Mean over 1 Month', 'Average Polling Percentage', 'Pageviews Over 1 Month (per 100k)']].plot(kind="bar", title="Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")
ax = combined_df.loc[:, ['Google Trends Mean over 1 Month', 'Average Polling Percentage', 'Pageviews Over 1 Month (per 100k)']].plot(kind="bar", title="\n".join(wrap("Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates")))
title = ax.set_title("\n".join(wrap("Comparing Average Pageviews, Google Trends, and Polling Statistics across Candidates", 60)))
fig = ax.get_figure()
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig('avg_gtrend_vs_pageviews_vs_polling_statistics_dems.png')




# In[ ]:



# In[ ]:



# In[ ]:


cur.execute("""

SELECT 
*
FROM
(SELECT * FROM Gtrend_MEAN WHERE time_period = 'one month') as t1
INNER JOIN
(SELECT * FROM Gtrend_MEAN WHERE time_period = 'three months') as t2
ON t1.name = t2.name


""")

df2 = pd.DataFrame(cur.fetchall())[[2, 4, 9]]

df2 = df2.rename(columns={2: 'Candidate', 4: "Google Trends Mean over 1 Month", 9: "Three Month Mean", }, errors="raise")
df2 = df2.set_index('Candidate')


# cur.execute("SELECT * FROM Gtrend_MEAN")
# results = cur.fetchall()  

# df = pd.DataFrame(results)

# df = df.set_index(1)
# df = df.iloc[:, 1:]
# df = df.rename(columns={2: "One Month Mean", 3: "Three Month Mean", 4: "One Day Mean",  5: "Seven Day Mean",  6: "Five Year Mean"}, errors="raise")
# df

df2

# In[ ]:


#one month delta
df2.plot(kind="bar", title="Average Google Trend Score across Candidates")
ax = df2.plot(kind="bar", title="Average Google Trend Score across Candidates")
fig = ax.get_figure()
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig('avg_gtrend_all_candidates.png')



# In[ ]:


cur.execute("""

SELECT 
*
FROM
(SELECT * FROM Gtrend_DELTA WHERE time_period = 'one month') as t1
INNER JOIN
(SELECT * FROM Gtrend_DELTA WHERE time_period = 'three months') as t2
ON t1.name = t2.name


""")

df3 = pd.DataFrame(cur.fetchall())[[2, 4, 9]]

df3 = df3.rename(columns={2: 'Candidate', 4: "1 Month Delta", 9: "3 Month Delta", }, errors="raise")
df3 = df3.set_index('Candidate')



# In[ ]:
df3.plot(kind="bar", title="Delta in Google Trend Searches across Candidates")
ax = df3.plot(kind="bar", title="Delta in Google Trend Searches across Candidates")
fig = ax.get_figure()
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig('delta_gtrend_all_candidates.png')



# %%

#BONUS API & CALCULCATION & PRINT OUTPUT
cur.execute('DROP TABLE IF EXISTS twitter_table')

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

# %%

combined_df = combined_df.merge(candidate_df, left_on='Candidate', right_on="Candidate")

combined_df = combined_df.set_index("Candidate")
combined_df.loc[:, ['Average Polling Percentage', 'Twitter Followers']]

# %%

# %%
data2 = combined_df.loc[:, ['Average Polling Percentage', 'Twitter Followers']]
corr = data2.corr(method='pearson')
corr

# %%
ax = combined_df.loc[:, ['Average Polling Percentage', 'Twitter Followers']].plot(kind="bar", title="Average Polling Percentages vs Twitter Followers (per million) | Corr: {}".format(corr.iloc[1, 0]))
fig = ax.get_figure()
fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig('twitter_vs_polling.png')


# %%

#final to csv
corr = combined_df.iloc[:, [0,1, 2, 3, 6]].corr(method='pearson')
corr.to_csv(r'correlations.csv')

# %%


# %%



# %%


# %%
