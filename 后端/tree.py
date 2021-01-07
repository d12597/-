# from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
# from sklearn.metrics import precision_score,  recall_score, f1_score
# import matplotlib.pyplot as plt  
import graphviz
import os
import fitz



def tree(x,y):
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
    etree_clf = DecisionTreeClassifier(criterion='entropy')
    gtree_clf = DecisionTreeClassifier(criterion='gini')
    etree_clf.fit(x_train, y_train)
    gtree_clf.fit(x_train, y_train)
    dot_data = export_graphviz(gtree_clf,out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("tree")  #tree是命名的pdf名称

def get_file(pdf_dir):
    docunames = os.listdir()
    for docuname in docunames:
        if os.path.splitext(docuname)[1] == '.pdf':#目录下包含.pdf的文件
            pdf_dir.append(docuname)
    return pdf_dir
            
def conver_img(pdf_dir):
    for pdf in pdf_dir:
        doc = fitz.open(pdf)
        pdf_name = os.path.splitext(pdf)[0]
        for pg in range(doc.pageCount):
            page = doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 2.0
            zoom_y = 2.0
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)
            pm.writePNG('%s.png' % pdf_name)
            
