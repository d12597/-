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


def number():
    conn=pymysql.connect('127.0.0.1','root','9705165')
    conn.select_db('hdzz')
    cur=conn.cursor()
    datax=[]
    datay=[]
    cur.execute("select * from number;")
    res=cur.fetchall()
    for i in range(len(res)):
        datax.append([res[i][1]])
        datay.append(res[i][2])
    datay=np.array(datay)
    print(datay)
number()

