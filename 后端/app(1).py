# -*- coding: UTF-8 -*- 
from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, request
import threading
import time
import pymysql
from ariori import apriori,draw,loadDataSet
from mysql import mysql_test,mysql_apriori,mysql_number,mysql_iris
from iris import load_iris,cluster1,iris_data_scatter1
from tree import tree,get_file,conver_img
from number import load_number,number

# configurations
DEBUG = False

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/testapipost', methods=['post'])
def test():
    jobs=[{}]
    data = request.get_json(silent=True)
    x = data['firstName']
    x = int(x)
    a=mysql_test(x)
    print(x)
    jobs[0]=a    
    print (jobs)
    return jsonify({'jobs':jobs})
    
@app.route('/aprioriget', methods=['get'])
def aprioriget():    
    ad=loadDataSet()
    apriori_data=mysql_apriori()
    L, supportData = apriori(ad,minSupport=0.2)
    apriori_draw=draw(L[1],supportData)
    return jsonify({'aprioridata':apriori_data,'aprioridraw':apriori_draw})

@app.route('/irisget', methods=['get'])
def irisget():    
    iris_data=mysql_iris()
    X,y = load_iris()
    x,iris_result_scatter,bar_num = cluster1(X,y)
    iris_data_scatter=iris_data_scatter1(x,y)
    return jsonify({'irisdata':iris_data,'irisdatascatter':iris_data_scatter,
                    'barnum':bar_num,'irisresultscatter':iris_result_scatter
                    })

@app.route('/numberget', methods=['get'])
def numberget():    
    number_data=mysql_number()
    x,y=load_number()
    inlier,outlier,test_data,l1,l2,l3,l4=number(x,y)
    return jsonify({'numberdata':number_data,"inlier":inlier,
                    'outlier':outlier,'test_data':test_data,
                    'l1':l1,'l2':l2,'l3':l3,'l4':l4
                    })

@app.route('/treeget', methods=['get'])
def treeget():  
    iris_data=mysql_iris()
    X,y = load_iris()
    tree(X,y)
    pdf_dir=[]
    pdf_dir=get_file(pdf_dir)
    conver_img(pdf_dir)
    return jsonify({'irisdata':iris_data})

if __name__ == '__main__':

    # 运行flask app
    app.run(host='127.0.0.1',port=5000) #debug=True
