import unittest
import sqlite3
import json
import os
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import urllib.request
import plotly.express as px
from textwrap import wrap

def setUpDatabase(db_name):
    #path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def visualize_real_clear_politics(candidates):
    cur, conn = setUpDatabase('CandidateData.db')
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
    primary_df.to_csv (r'primary_averages.csv', index = None, header=True)
    fig_prim = go.FigureWidget(data=go.Bar( x=primary_df['Candidate'],y=primary_df['Average Percent'] ))
    fig_prim.layout.title = 'Average Percent Support of Candidates in the Primary'
    fig_prim.update_layout(title_x=0.5)
    fig_prim.update_layout(xaxis_title="Candidate", yaxis_title="Average Percent Support")
    fig_prim.show()
    fig_prim.write_image("avg_primary_polling_results.png")

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
    gen_df.to_csv (r'general_averages.csv', index = None, header=True)
    gen_fig.write_image("avg_general_polling_results.png")

def visualize_site_traffic(candidates):
    cur, conn = setUpDatabase('CandidateData.db')
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
    fig.write_image("yearly_website_visitors.png")

def visualize_gtrends(candidates):
    cur, conn = setUpDatabase('CandidateData.db')
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
    return combined_df

def visualize_twitter(candidates, combined_df):



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

def main():
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
    combined_df = visualize_gtrends(candidates)
    visualize_real_clear_politics(candidates)
    visualize_site_traffic(candidates)
    visualize_twitter(candidates, combined_df)            

if __name__ == "__main__":
    main()