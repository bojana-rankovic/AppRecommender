# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 20:14:00 2017

@author: 05t0J4X
"""
import pandas as pd
users = {}

def manhattan(rating1, rating2):
    distance=0
    for key in rating1:
        if key in rating2:
            distance+=abs(rating1[key]-rating2[key])
    return distance        


def minkowski(rating1, rating2, r):
    distance = 0
    commonRating = False
    for key in rating1:
        if key in rating2:
            distance+=pow(rating1[key]-rating2[key],r)
            commonRating = True
    if commonRating: return pow(distance,1/r)
    else: return 0



    
class recommender:
    def __init__(self, data, k=1, metric='pearson', n=5):
        self.data = data
        self.k = k
        self.n = n
        self.itemId2ItemName = {}
      
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson

        if type(data).__name__ == 'dict':
            self.data = data
    
    #loading the dataset
    def loadDataset(self):
        
        self.data = {}
        dtypes = {'user':'int64','item':'int64','cnt':'int64','daytime':'str',	'weekday':'str', 'isweekend':'str',	'homework':'str','cost':'str','weather':'str','country':'str','city':'int64'}
        read_data = pd.read_csv('C:/Users/Nikola/Documents/Bojana/MS/Inteligentni/frappe/frappe/frappe.csv',sep='\t',dtype = dtypes)
        row_count = len(read_data)
        
        
        for i in range(1, row_count):
            user = read_data.loc[i,'user']   
            item = read_data.loc[i, 'item']                 
            count = read_data.loc[i, 'cnt']
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[item]=count
            self.data[user]=currentRatings
            
        dtypes_item ={'item':'int64','package':'str','category':'str'}    
        item_data = pd.read_csv('C:/Users/Nikola/Documents/Bojana/MS/Inteligentni/frappe/frappe/meta.csv',sep='\t',dtype = dtypes_item)
        row_count = len(item_data)
        print(item_data)
        print(row_count)
 
        for i in range(1, row_count):
             item_id = item_data.loc[i,'item']
             package = item_data.loc[i,'package']
             category = item_data.loc[i,'category']
             title = package + ' in category: '+category
             self.itemId2ItemName[item_id]=title
        
       
        
            
        
        

    #pearson metric for distance   
    def pearson(self, rating1, rating2):
        from math import sqrt
        sum_x = 0
        sum_y = 0
        sum_xy= 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                x = rating1[key]
                y = rating2[key]
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
            #distance = manhattan(users[instance], users[username])
            #distance = minkowski(users[instance], users[username], 2)
             distance = self.fn(self.data[username],self.data[instance])
             distances.append((instance, distance))
        distances.sort(key = lambda artistTuple: artistTuple[1],reverse=True)
        return distances


    def convertItemId2ItemName(self, itemId):
        if itemId in self.itemId2ItemName:
            return self.itemId2ItemName[itemId]
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
        recommendations = [(self.convertItemId2ItemName(k), v) for (k, v) in recommendations]

        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        return recommendations[:self.n]

r = recommender(users)
r.loadDataset()
print(r.recommend(5))
