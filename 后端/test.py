# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:39:36 2021

@author: 80686
"""


import pymysql
import time 
import numpy as np 
import pandas as pd
import matplotlib. pyplot as plt
from sklearn import cluster, datasets 
from sklearn.decomposition  import PCA
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from sklearn import metrics 


iris = datasets.load_iris()
X = np.array(iris.data)
y = iris.target
print(type(X[0]))
print(type(y))
print('sql执行成功')

