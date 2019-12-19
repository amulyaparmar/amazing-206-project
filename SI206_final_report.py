#!/usr/bin/env python
# coding: utf-8

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


import os
# os.path.isfile("drive/Colab Notebooks/CandidateData.db")


# In[ ]:


# https://qiita.com/Rowing0914/items/51a770925653c7c528f9

# RUN BELOW CODE ONLY ONCE

# get_ipython().system('apt-get install -y -qq software-properties-common python-software-properties module-init-tools')
# get_ipython().system('add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null')
# get_ipython().system('apt-get update -qq 2>&1 > /dev/null')
# get_ipython().system('apt-get -y install -qq google-drive-ocamlfuse fuse')
# from google.colab import auth
# auth.authenticate_user()
# from oauth2client.client import GoogleCredentials
# creds = GoogleCredentials.get_application_default()
# import getpass
# get_ipython().system('google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL')
# vcode = getpass.getpass()
# get_ipython().system('echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}')


# In[ ]:


# get_ipython().system('mkdir drive')
# get_ipython().system('google-drive-ocamlfuse drive')
# get_ipython().system('ls drive/"Colab Notebooks"')


# In[ ]:


import os
# os.path.isfile("drive/Colab Notebooks/CandidateData.db")


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


cur.execute("SELECT * FROM WebsiteData")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM WebsiteDelta")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM DemPrimary")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM DemGeneral")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM Gtrend_DELTA")
results = cur.fetchall()  

df = pd.DataFrame(results)

df = df.set_index(1)
#df.rename(columns={"A": "a", "B": "b", "C": "c"}, errors="raise")
df


# In[ ]:


#one month delta
df[2].plot(kind="bar")


# In[ ]:


#three month delta
df[3].plot(kind="bar")


# In[ ]:


cur.execute("SELECT * FROM Gtrend_MEAN")
cur.fetchall()


# In[ ]:


cur.execute("SELECT * FROM Gtrend_DELTA")
results = cur.fetchall()

df = pd.DataFrame(results)

df = df.set_index(1)
#df.rename(columns={"A": "a", "B": "b", "C": "c"}, errors="raise")
df


# In[ ]:




