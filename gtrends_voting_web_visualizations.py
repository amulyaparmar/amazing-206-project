# In[ ]:


#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import urllib.request



# In[ ]:



def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn
cur, conn = setUpDatabase('CandidateData1.db')


# In[ ]:



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

combined_df.iloc[:, [0, 1]].plot(kind="bar", title="Average Google Trend Score across Candidates")

pageviews_vs_gtrends = combined_df.iloc[:, [0, 1]]
corr = pageviews_vs_gtrends.corr(method='pearson')
print(corr)

# In[ ]:


#cur.execute("SELECT DISTINCT name, avg(percent) FROM DemPrimary WHERE name='Kamala Harris'")
cur.execute("SELECT name, AVG(percent) FROM DemPrimary GROUP BY name")
df3 = pd.DataFrame(cur.fetchall())

df3 = df3.rename(columns={0: "Candidate", 1: 'Average Polling Percentage'}, errors="raise")

df3 = df3.set_index("Candidate")
df3

combined_df = combined_df.merge(df3, left_on='Candidate', right_on='Candidate')
combined_df

combined_df.iloc[:, [0, 1, 6]].plot(kind="bar", title="Comparing Average Pageviews, Googel Trends, and Polling Statistics across Candidates")

data = combined_df.iloc[:, [0, 1, 6]]
corr = data.corr(method='pearson')
print(corr)


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
