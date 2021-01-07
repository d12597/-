# import time 
import numpy as np 
# import pandas as pd
# import matplotlib. pyplot as plt
from sklearn import cluster, datasets 
from sklearn.decomposition  import PCA
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from sklearn import metrics 
import pymysql

#载入iris数据集
def load_iris():
    conn=pymysql.connect('127.0.0.1','root','9705165')
    conn.select_db('hdzz')
    cur=conn.cursor()
    X=[]
    y=[]
    cur.execute("select * from iris;")
    res=cur.fetchall()
    for i in range(len(res)):
        a=[]
        for j in range(1,5):
            a.append(res[i][j])
        a=np.array(a)
        X.append(a)
        y.append(res[i][5])
    return np.array(X),np.array(y)

def cluster1(X,y):
    a={}
    pca = PCA(n_components = 2) #降为2维
    pca = pca.fit(X)
    X_dr = pca.transform(X)
    
    #聚类种类及名称
    clustering_names = ['MiniBatchKMeans',  'MeanShift', 'AgglomerativeClustering','DBSCAN', 'Birch']
    
    x = X_dr 
    #规范化数据集以便于参数选择
    x = StandardScaler().fit_transform(x)
    #均值漂移估计带宽
    bandwidth = cluster.estimate_bandwidth(x, quantile=0.3)    
    #kneighbors_graph类返回用KNN时和每个样本最近的K个训练集样本的位置
    connectivity = kneighbors_graph(x, n_neighbors=10, include_self=False)    
    #使连接对称 
    connectivity = 0.5 * (connectivity + connectivity.T)
    
    # 创建聚类估计器
    
    two_means = cluster.MiniBatchKMeans(n_clusters=3,n_init=10)     #MiniBatchKMeans
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)   #MeanShift
    average_linkage = cluster.AgglomerativeClustering(n_clusters=3) #AgglomerativeClustering
    dbscan = cluster.DBSCAN(eps=0.5)                                #DBSCAN
    birch = cluster.Birch(n_clusters=3)                             #Birch
    
    #聚类算法
    clustering_algorithms = [two_means,ms,average_linkage,dbscan, birch]
    
    colors = np.array([x for x in  "bgrcmykbgrcmykbgrcmykbgrcmyk"])
    #hstack()函数水平把数组堆叠起来
    colors = np.hstack([colors] * 20)

    num = []
    for name, algorithm in zip(clustering_names, clustering_algorithms):
        r=[]
        g=[]
        b=[]
        # t0 = time.time() #time()函数返回当前时间的时间戳
        algorithm.fit(X)
        # t1 = time.time()
        #hasattr（）函数用于判断对象是否包含对应的属性
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(x)
            
        # if hasattr(algorithm, 'cluster_centers_'):
            # centers = algorithm.cluster_centers_
            # center_colors = colors[:len(centers)]
            
        for i in range(len(colors[y_pred].tolist())):   #循环获取聚类结果的各个点的x,y,color
            if colors[y_pred].tolist()[i] == 'r':
                r.append([x[:, 0][i], x[:, 1][i]])
            if colors[y_pred].tolist()[i] == 'g':
                g.append([x[:, 0][i], x[:, 1][i]])
            if colors[y_pred].tolist()[i] == 'b':
                b.append([x[:, 0][i], x[:, 1][i]])
        #创建聚类名称与结果的键值对
        a.update({"%s"%name:{'r':r,'g':g,'b':b}})         
        num.append(metrics.v_measure_score(y,y_pred))
    return x,a,num

def iris_data_scatter1(X_dr,y):
    b={}
    for j in range(3):
        a=[]
        for i in range(len(X_dr[y==j,0])):
            if j == 0:
                a.append([X_dr[y==0,0][i],X_dr[y==0,1][i]])
            if j == 1:
                a.append([X_dr[y==1,0][i],X_dr[y==1,1][i]])
            if j == 2:
                a.append([X_dr[y==2,0][i],X_dr[y==2,1][i]])
        if j == 0:
            b.update({'red':a})
        if j == 1:
            b.update({'blue':a})
        if j == 2:
            b.update({'black':a})
    return b
