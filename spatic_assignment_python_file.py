# -*- coding: utf-8 -*-
"""Spatic_Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KexnPIh6i3qLOMXnJxpFTNiyLKIxEd5i
"""

#importing required packages
import numpy as np
import pandas as pd
import math 
from geopy.distance import geodesic
from collections import OrderedDict

#read csv file
dataset = pd.read_csv("/content/assignment_data_spatic.csv")
dataset.shape

dataset.head(10)

#store the given dataset in an ordered dictionary having keys as country names and values as longitude and latitudes
Countries = OrderedDict()
for values in range(dataset.shape[0]):
  Countries[str(dataset.iloc[values][0])] = tuple(dataset.iloc[values][1:3])

#sort the countries dictionary 
Countries_sorted = {i:Countries[i] for i in sorted(Countries)}

#By using Levenshtein distance formula we can calculate the text similarity between two strings 
def levestein(str1,str2,m,n):
  d = [[0 for i in range(n)] for j in range(m)] 
  for i in range(1,m):
    d[i][0] = i
  for j in range(1,n):
    d[0][j] = j 
  for j in range(1,n):
    for i in range(1,m):
      if str1[i] == str2[j]:
        Cost = 0
      else:
        Cost = 1
      d[i][j] = min(d[i-1][j] + 1,                   
                         d[i][j-1] + 1,                   
                         d[i-1][j-1] + Cost)  
 
  return d[m-1][n-1]

#add new attribute is_similar to existing dataset
dataset["is_similar"] = [0] * dataset.shape[0] 
dataset.tail(30)

Countries_sorted

#we can use Geopy package which uses Haversine Distance formula to calculate distance between two points from its latitude and longitude update the Countries dictionary  
from geopy.distance import great_circle
for key1 in Countries_sorted: 
  for key2 in Countries_sorted: 
    #considering only strings which has same 3 sized prefix
    if key1[0:2] == key2[0:2]:
      if key1 != key2 and levestein(key1,key2,len(key1),len(key2)) < 5:
        distance = great_circle(Countries_sorted[key1],Countries_sorted[key2]).meters 
        if distance < 200: 
          dataset.loc[dataset["name"] == key1,"is_similar"] = 1  
          dataset.loc[dataset["name"] == key2,"is_similar"] = 1

#store updated dataset in .csv file
dataset.to_csv("/content/assignment_data_spatic_output.csv")