# -*- coding: UTF-8 -*- 
from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, request
import threading
import time
import pymysql
from ariori import apriori,draw,loadDataSet
from mysql import mysqltest,mysqlapriori,mysqlnumber,mysqliris

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
    a=mysqltest(x)
    print(x)
    jobs[0]=a    
    print (jobs)
    return jsonify({'jobs':jobs})
    
@app.route('/testget', methods=['get'])
def testget():    
    ad=loadDataSet()
    aprioridata=mysqlapriori()
    L, supportData = apriori(ad,minSupport=0.2)
    aprioridraw=draw(L[1],supportData)
    numberdata=mysqlnumber()
    irisdata=mysqliris()
    return jsonify({'aprioridata':aprioridata,'aprioridraw':aprioridraw
                    ,'numberdata':numberdata
                    ,'irisdata':irisdata})

if __name__ == '__main__':

    # 运行flask app
    app.run(host='10.120.203.67',port=5000) #debug=True
