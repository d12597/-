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


conn=pymysql.connect('10.120.51.229','root','123456')
conn.select_db('hdzz')
cur=conn.cursor()
a=[]
for i in range(10):
    b={}
    b.update({'id':i})
    for j in range(1,5):
        cur.execute("select item%d from iris where id = %d;"%(j,i))
        res=cur.fetchone()
        b.update({"item%d"%j:res[0]})
    cur.execute("select target from iris where id = %d;"%i)
    res=cur.fetchone()
    b.update({"target":res[0]})
    a.append(b)
print(a)
cur.close()
conn.commit()
conn.close()


