
#basic import statements
import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import urllib.request



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
print(candidate_df.head())


import requests
import json
import tweepy 			# need to pip install tweepy
import twitter_info		# you need to initialize this file with your Tweet app info

# Fill these in in the twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) 


# for i in range(len(candidate_df[0])):
    # print(candidate_df.iloc[i, 0], " getting following count")
    # user = tweepy.api.get_user(candidate_df.iloc[i, 0])
    # print(user.followers_count)

# import tweepy
# import sys

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# user = tweepy.api.get_user('bbresults')
# #print(user.followers_count)
# print(user.followers_count)

# OAuth process, using the keys and tokens
# auth = tweepy.OAuthHandler(ckey, csecret)
# auth.set_access_token(atoken, asecret)
# Creation of the actual interface, using authentication
# api = tweepy.API(auth)
# collect tweets on #MRT
# for tweet in tweepy.Cursor(api.search,q="MRT",count=100,
#                            lang="en",rpp=100,
#                            since="2017-04-03").items():
#   print (tweet.created_at, tweet.text)

#   user = tweepy.api.get_user(31536003)
# Tweepy OAuthHandler

import tweepy
import numpy as np

consumer_key = "nDbRA7vy5j0nxhBtZloHn7xee"
consumer_secret = "aIEVKKPeFjbjqZoyjRObUoMSsTcTXzxfzrBWr4g8T9coIUyNev"
access_token = "703356714-BaFvjE2YkCCB5zJkyFZCCNDTfnmWnwSVKEXh7cXR"
access_token_secret = "N75fvl0rPehgtO7v5oNZcdI3GAUzqGMqhnmcMVW3ttWGM"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

candidate_df.set_index(0)
candidate_df['Twitter Followers'] = np.nan

for index, val in candidate_df[2].iteritems():
    user = api.get_user(val)
    candidate_df['Twitter Followers'][index] = user.followers_count

    print(user.name, user.followers_count)


print(candidate_df.head())