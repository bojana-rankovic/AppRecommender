# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:36:36 2017

@author: bojana-rankovic
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


rating_headers = ['user', 'item', 'cnt']
dtypes = {'user':'int64','item':'int64','cnt':'int64','daytime':'str','weekday':'str', 'isweekend':'str',	'homework':'str','cost':'str','weather':'str','country':'str','city':'int64'}
ratings = pd.read_csv('frappe/frappe/frappe.csv', sep='\t',  dtype=dtypes)
ratings=ratings[3:]
item_headers = ['item', 'category', 'name']
dtypes = {'item':'int64','category':'str','name':'str'}
movies = pd.read_csv('frappe/frappe/meta.csv',
                       sep='\t',dtype = dtypes)

#movie_titles = movies.title.tolist()

#data = pd.read_csv('C:/Users/Nikola/Documents/Bojana/MS/frappe/frappe/frappe.csv',sep='\t', dtype=dtypes)
#print(movies)
df = movies.loc[(movies['name']=='unknown')]
listUnknown = df[df.columns[0]]

df = ratings[~ratings['item'].isin(listUnknown)]
#df=df.groupby(['user','item']).count()
df=df.groupby( [ 'user', 'item'] ).size().to_frame(name = 'count').reset_index()
print(df)


