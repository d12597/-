# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:12:19 2021

@author: 80686
"""
import pymysql
import os
from sklearn import cluster, datasets 
import numpy as np 

def load_text():
    directory = 'C:/Users/80686/Desktop/数据挖掘大实验/20news-18828'
    category_names = os.listdir(directory)
    content1=[]
    f=[]
    for i in range(len(category_names)):
        category = category_names[i]
        category_dir = os.path.join(directory, category)
        for file_name in os.listdir(category_dir):
            f.append(file_name.replace("'",''))
            file_path = os.path.join(category_dir,file_name)
            contents = open(file_path, encoding='latin1').read().strip()
            content1.append(contents[:100].replace("\n","").replace("'",''))
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `text`(`id` INT(10),`item1` varchar(255),`item2` varchar(255));")
    for i in range(len(f)):
        cur.execute("INSERT INTO text VALUES (%d, '%s', '%s');"%(i,f[i].replace("'",""),str(content1[i]).replace("'","").replace("\\","").replace("/","")))
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    
#载入iris数据集
def load_iris():
    iris = datasets.load_iris()
    X = np.array(iris.data)
    y = iris.target
    
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `iris`(`id` INT(10),`item1` float,`item2` float,`item3` float,`item4` float,`target` int);")
    for i in range(len(X)):
        cur.execute("INSERT INTO iris VALUES (%d, %f, %f, %f, %f, %d);"%(i,X[i][0],X[i][1],X[i][2],X[i][3],y[i]))
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')

def load_number():
    n_samples = 500# 产生的样本点数目为500个
    #模拟数据
    #n_samples样本数，n_features特征数，n_informative生成输出的特征数量，noise应用于输出的高斯噪声的标准差，coef如果为真，则返回基础线性模型的系数
    #random_state确定数据集创建的随机数生成。跨多个函数调用传递可重复输出的int
    x, y, coef = datasets.make_regression(n_samples=n_samples, 
                                          n_features=1,
                                          n_informative=1, 
                                          noise=10,coef=True,
                                          random_state=0)
        

    n_outliers = 100# 前100个设为异常点
    # 添加异常数据
    np.random.seed(0)#用于指定随机数生成时所用算法开始的整数值，如果使用相同的seed( )值，则每次生成的随即数都相同
    x[:n_outliers] = 4 + 0.5 * np.random.normal(size=(n_outliers, 1))
    y[:n_outliers] = -20 + 20 * np.random.normal(size=n_outliers)
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `number`(`id` INT(10),`item1` float,`item2` float);")
    for i in range(len(y)):
        cur.execute("INSERT INTO number VALUES (%d, %f, %f);"%(i,x[i][0].item(),y[i].item()))
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    
def load_apriori():
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    c=[['面包','可乐','麦片'], ['牛奶', '可乐'], ['牛奶', '面包', '麦片'],
            ['牛奶', '可乐'],['面包','鸡蛋','麦片'],['牛奶','面包','可乐'],
            ['牛奶','面包','鸡蛋','麦片'],['牛奶','面包','可乐'],['面包','可乐']]
    cur.execute("drop table apriori;")
    cur.execute("CREATE TABLE IF NOT EXISTS `apriori`(`id` INT(10),`item1` varchar(255),`item2` varchar(255),`item3` varchar(255),`item4` varchar(255));")
    for i in range(len(c)):
        if len(c[i])==2:
            cur.execute("INSERT INTO apriori VALUES (%d, '%s', '%s','',' ');"%(i,c[i][0].replace("'",""),c[i][1].replace("'","")))
        if len(c[i])==3:
            cur.execute("INSERT INTO apriori VALUES (%d, '%s', '%s', '%s',' ');"%(i,c[i][0].replace("'",""),c[i][1].replace("'",""),c[i][2].replace("'","")))
        if len(c[i])==4:
            cur.execute("INSERT INTO apriori VALUES (%d, '%s', '%s', '%s', '%s');"%(i,c[i][0].replace("'",""),c[i][1].replace("'",""),c[i][2].replace("'",""),c[i][3].replace("'","")))
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')

def mysqltest(x):
    a={}
    conn=pymysql.connect('localhost','root','9705165')
    conn.select_db('hdzz')
    cur=conn.cursor()

    cur.execute("select post from test where id =%d;"%x)
    res=cur.fetchone()
    a.update({'post':res[0]})
    cur.execute("select level from test where id =%d;"%x)
    res=cur.fetchone()
    a.update({'level':res[0]})
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    return a

def mysqlapriori():
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    a=[]
    for i in range(8):
        b={}
        b.update({'id':i})
        for j in range(1,5):
            cur.execute("select item%d from apriori where id = %d;"%(j,i))
            res=cur.fetchone()
            b.update({"item%d"%j:res[0]})
        a.append(b)
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    return a

def mysqlnumber():
    conn=pymysql.connect('10.120.51.229','root','123456')
    conn.select_db('hdzz')
    cur=conn.cursor()
    a=[]
    for i in range(10):
        b={}
        b.update({'id':i})
        for j in range(1,3):
            cur.execute("select item%d from number where id = %d;"%(j,i))
            res=cur.fetchone()
            b.update({"item%d"%j:res[0]})
        a.append(b)
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    return a

def mysqliris():
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
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
    return a