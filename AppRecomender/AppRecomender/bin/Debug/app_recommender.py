# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 20:14:00 2017

@author: bojana-rankovic
"""
import math
import pandas as pd


users = {}

     




   

class recommender:
    def __init__(self, data, k=1, metric='pearson', n=5):
        self.data = data
        self.k = k
        self.n = n
        self.itemId2ItemName = {}
        self.itemId2ItemIcon = {}
        self.maxValue = 0
        self.minValue = 0
        self.frape_csv = 0
        self.meta_csv = 0
        self.recommendations_icons = 0
      
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if self.metric == 'cosine':
            self.fn = self.cosine_distance
        if self.metric == 'minkowski':
            self.fn = self.minkowski
        if self.metric == 'manhattan':
            self.fn = self.manhattan
            

        if type(data).__name__ == 'dict':
            self.data = data
    
    def cleanDataset(self, frape_csv, meta_csv):
        df = meta_csv.loc[(meta_csv['name']=='unknown')]
        listUnknown = df[df.columns[0]]
        self.frape_csv = frape_csv[~frape_csv['item'].isin(listUnknown)]
   
    #loading the dataset
    def loadDataset(self):
        
        self.data = {}
        dtypes = {'user':'int64','item':'int64','cnt':'int64','daytime':'str',	'weekday':'str', 'isweekend':'str',	'homework':'str','cost':'str','weather':'str','country':'str','city':'int64'}
        self.frape_csv = pd.read_csv('frappe/frappe/frappe.csv',sep='\t',dtype = dtypes)
        
        dtypes_item ={'icon':'str','item':'int64','package':'str','category':'str','name':'str'}    
        self.meta_csv = pd.read_csv('frappe/frappe/meta.csv',sep='\t',dtype = dtypes_item)
        
        self.cleanDataset(self.frape_csv,self.meta_csv)
        self.frape_csv = self.frape_csv.groupby( [ 'user', 'item'] ).size().to_frame(name = 'count').reset_index()

        row_count_frape = len(self.frape_csv)
        
        row_count_meta = len(self.meta_csv)
        self.maxValue = self.frape_csv['count'].max()
        self.minValue = self.frape_csv['count'].min()
        
        for i in range(0,row_count_frape):
            user = self.frape_csv.iloc[i, 0]             
            item = self.frape_csv.iloc[i, 1]                            
            count = self.frape_csv.loc[i, 'count']
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[item]=count
            self.data[user]=currentRatings
            
       
       
 
        for i in range(0, row_count_meta):
             item_id = self.meta_csv.iloc[i,0]
             category = self.meta_csv.iloc[i,2]
             name = self.meta_csv.iloc[i,8]
             title = str(item_id) +' ' + name +  ' in category: ' + category
             self.itemId2ItemName[item_id]= title
             self.itemId2ItemIcon[item_id] = self.meta_csv.iloc[i,5] 
       
    def manhattan(self, rating1, rating2):
        distance=0
        for key in rating1:
            if key in rating2:
                x = rating1[key]#1 + (rating1[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                y = rating2[key]#1 + (rating2[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                distance+=abs(x-y)
        return distance 
    
    def minkowski(self, rating1, rating2, r=2):
        distance = 0
        commonRating = False
        for key in rating1:
            if key in rating2:
                x = rating1[key]#1 + (rating1[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                y = rating2[key]#1 + (rating2[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                distance+=pow((x-y),r)
                commonRating = True
        if commonRating: return pow(distance,1/r)
        else: return 0
    
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
       
    def cosine_distance(self,rating1,rating2):
        sumxx, sumxy, sumyy = 0, 0, 0
        commonRating = False
        for key in rating1:
            if key in rating2:
                x = rating1[key]#1 + ((rating1[key]-self.minValue)*(10-1))/(self.maxValue-self.minValue)
                y = rating2[key]#1 + ((rating2[key]-self.minValue)*(10-1))/(self.maxValue-self.minValue)
                sumxx += x*x
                sumyy += y*y
                sumxy += x*y
                commonRating = True
        if commonRating: return sumxy/math.sqrt(sumxx*sumyy)
        else: return 0
    
    #pearson metric for distance 
    
    def pearson(self, rating1, rating2):
        from math import sqrt
        sum_x = 0
        sum_y = 0
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                x =rating1[key] #1 + (rating1[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                y =rating2[key] #1 + (rating2[key]-self.minValue)*(10-1)/(self.maxValue-self.minValue)
                sum_x += x
                sum_x2 += x**2
                sum_xy += x*y
                sum_y += y
                sum_y2 += y**2
                n+=1
        if n == 0: return 0 
        denominator = (sqrt(sum_x2-sum_x*sum_x/n)*sqrt(sum_y2-sum_y*sum_y/n))
        if denominator == 0:
            return 0  
        else: return (sum_xy-sum_x*sum_y/n)/(sqrt(sum_x2-sum_x*sum_x/n)*sqrt(sum_y2-sum_y*sum_y/n))

    def computeNearestNeighbour(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
            #distance = manhattan(self.data[instance], self.data[username])
            #distance = minkowski(self.data[username], self.data[instance], 2)
             distance = self.fn(self.data[username],self.data[instance])
            #distance = self.cosine_distance(self.data[username], self.data[instance])
             distances.append((instance, distance))
        distances.sort(key = lambda artistTuple: artistTuple[1],reverse=True)
        return distances


    def convertItemId2ItemName(self, itemId):
        if itemId in self.itemId2ItemName:
            return self.itemId2ItemName[itemId]
        else: 
            return itemId
        
    def convertItemId2ItemIcon(self, itemId):
        if itemId in self.itemId2ItemIcon:
            return self.itemId2ItemIcon[itemId]
        else: 
            return itemId
    
    def recommend(self, user):
        recommendations = {}
        nearest = self.computeNearestNeighbour(user)
        userRatings = self.data[user]
        totalDistance = 0
        for i in range(self.k):
            totalDistance+=nearest[i][1]
        for i in range(self.k):
            if(totalDistance!=0):
                weight = nearest[i][1]/totalDistance
                name = nearest[i][0]
                neighbourRatings = self.data[name]
                for artist in neighbourRatings:
                    if not artist in userRatings:
                        if not artist in recommendations:
                            recommendations[artist] = (neighbourRatings[artist]*weight)
                        else:
                            recommendations[artist] = (recommendations[artist]+neighbourRatings[artist]*weight)
        recommendations = list(recommendations.items())
        self.recommendations_icons = [(self.convertItemId2ItemIcon(k), v) for (k, v) in recommendations]
        recommendations =  [(self.convertItemId2ItemName(k), v) for (k, v) in recommendations]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        self.recommendations_icons.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

        return recommendations[:self.n]

import sys

if __name__ == "__main__":
    r = recommender(users,metric='pearson')
    r.loadDataset()
    f = open('pearson_file', 'w')
    recommendations = r.recommend(int(sys.argv[1]))
    recommendations_icons_list = r.recommendations_icons
    f.write('\n'.join('%s %s' % x for x in recommendations_icons_list)) 
    f.close()
    r = recommender(users, metric='manhattan')
    r.loadDataset()
    f = open('manhattan_file', 'w')
    recommendations = r.recommend(int(sys.argv[1]))
    recommendations_icons_list = r.recommendations_icons
    f.write('\n'.join('%s %s' % x for x in recommendations_icons_list)) 
    f.close()
    r = recommender(users, metric='cosine')
    r.loadDataset()
    f = open('cosine_file', 'w')
    recommendations = r.recommend(int(sys.argv[1]))
    recommendations_icons_list = r.recommendations_icons
    f.write('\n'.join('%s %s' % x for x in recommendations_icons_list)) 
    f.close()
    r = recommender(users, metric='minkowski')
    r.loadDataset()
    f = open('minkowski_file', 'w')
    recommendations = r.recommend(int(sys.argv[1]))
    recommendations_icons_list = r.recommendations_icons
    f.write('\n'.join('%s %s' % x for x in recommendations_icons_list))
    f.close()
    print('done')