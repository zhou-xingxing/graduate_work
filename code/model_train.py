# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:22:11 2020

@author: lenovo
"""
#弹幕片段机器学习部分

import numpy as np
from sklearn import svm,tree
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
import pandas as pd
import time

def svm_train_test():
    # 分三类
    # 读取数据
    feature=pd.read_csv(r'../data/ml_danmu_frag.csv')    
    feature=feature.iloc[:, 2:9]
    # 标准化
    feature['num']=(feature['num']-feature['num'].mean())/(feature['num'].std())
    # display(feature)
    num_group=feature.groupby(['flag'])
    print(num_group.size())

    # -1变0
#    flag=feature['flag'].tolist()
#    new_flag=[]
#    for i in flag:
#        if i==-1:
#            new_flag.append(0)
#        else:
#            new_flag.append(i)
#    feature['flag']=new_flag    
       
    data=np.array(feature)
    rate=[]
    Kernel='linear'
    epoch=100
    maxrate=0
    meanrate=0
    minrate=1
    meantime=0
    for k in range(epoch):
        # 划分训练集测试集
        X_train,X_test, y_train, y_test  = train_test_split(data[:, 1:7], data[:, 0], test_size=0.2, random_state=k)   
        # 搭建svm模型
        svm_clf=svm.SVC(C=1, kernel=Kernel, degree=3, gamma='auto', coef0=0.0, shrinking=True, \
                        probability=False,tol=0.001, cache_size=400, class_weight=None, verbose=False, \
                        max_iter=-1, decision_function_shape=None,random_state=None)
        # 训练模型
        print('Training begin...')
        start=time.clock()
        svm_clf.fit(X_train, y_train) 
        end=time.clock()
        print('Training finish')
        print('Train Time: ',end-start)
        meantime=meantime+(end-start)
        # 测试模型
        y_pre = svm_clf.predict(X_test)
        
        # 计算准确率
        sum=0
        for i in range(len(y_test)):
            if y_pre[i]==y_test[i]:
                sum=sum+1
            else:
                print('the predict is ',y_pre[i],', but the true is ',y_test[i])
        print('测试集大小', len(y_test))
        print('预测正确个数', sum)
        print('epoch[', k+1, '] ', sum/len(y_test))
        rate.append(sum/len(y_test))
        print('')
        meanrate+=rate[k]
        if rate[k]>maxrate:
            maxrate=rate[k];
        if rate[k]<minrate:
            minrate=rate[k];    
    print('所用核为：',Kernel)
    print('最高准确率：', maxrate)
    print('最低准确率：', minrate)
    print('平均准确率：', meanrate/epoch)
    print('平均训练用时：', meantime/epoch)

#svm_train_test()    
    
    
def tree_tain_test():
    # 读取数据
    feature=pd.read_csv(r'../data/ml_danmu_frag.csv')
    feature=feature.iloc[:, 2:9]
    # display(feature)
    # 归一化
    # feature['num']=(feature['num']-feature['num'].min())/(feature['num'].max()-feature['num'].min())
    # 标准化
    feature['num']=(feature['num']-feature['num'].mean())/(feature['num'].std())
    
    # 分两类
    # -1变0
    flag=feature['flag'].tolist()
    new_flag=[]
    for i in flag:
        if i==-1:
            new_flag.append(0)
        else:
            new_flag.append(i)
    feature['flag']=new_flag        
#    
    num_group=feature.groupby(['flag'])   
    print(num_group.size())    
    data=np.array(feature)
    # display(data)
    rate=[]
    epoch=100
    maxrate=0
    meanrate=0
    minrate=1
    meantime=0
    importance=np.array([0.,0.,0.,0.,0.,0.])
    # importance=np.array([0.,0.,0.,0.,0.])
    
    for k in range(epoch):
        # 划分训练集测试集
        X_train,X_test, y_train, y_test  = train_test_split(data[:, 1:7], data[:, 0], test_size=0.2, random_state=k)   
        # 搭建svm模型
        clf = tree.DecisionTreeClassifier(criterion='entropy')  
        # 训练模型
        print('Training begin...')
        start=time.clock()
        clf.fit(X_train, y_train) 
    #     特征重要性
        importance+=clf.feature_importances_
    #     print(clf.feature_importances_)  
        end=time.clock()
        print('Training finish')
        print('Train Time: ',end-start)
        meantime=meantime+(end-start)
        # 测试模型
        y_pre = clf.predict(X_test)
        # 计算准确率
        sum=0
        for i in range(len(y_test)):
            if y_pre[i]==y_test[i]:
                sum=sum+1
    
        print('预测正确个数', sum)    
        rate.append(sum/len(y_test))    
        meanrate+=rate[k]
        if rate[k]>maxrate:
            maxrate=rate[k];
        if rate[k]<minrate:
            minrate=rate[k];    
    print('特征重要性：',importance/epoch)        
    print('最高准确率：', maxrate)
    print('最低准确率：', minrate)
    print('平均准确率：', meanrate/epoch)
    print('平均训练用时：', meantime/epoch)

#tree_tain_test()   
    
def svm_model_train():
    model_save_path = "./model_save/"
    feature=pd.read_csv(r'../data/ml_danmu_frag.csv')    
    feature=feature.iloc[:, 2:9]
    # 标准化
    feature['num']=(feature['num']-feature['num'].mean())/(feature['num'].std())
    # display(feature)
    num_group=feature.groupby(['flag'])
    print(num_group.size())
    data=np.array(feature)
    Kernel='linear'
    # 划分训练集测试集
    X,Y=(data[:, 1:7], data[:, 0])   
    # 搭建svm模型
    svm_clf=svm.SVC(C=1, kernel=Kernel, degree=3, gamma='auto', coef0=0.0, shrinking=True, \
                    probability=False,tol=0.001, cache_size=400, class_weight=None, verbose=False, \
                    max_iter=-1, decision_function_shape=None,random_state=None)
    # 训练模型
    print('Training begin...')
    start=time.clock()
    svm_clf.fit(X, Y) 
    end=time.clock()
    print('Train Time: ',end-start)
    save_path_name=model_save_path+"svm_"+"train_model.model"
    joblib.dump(svm_clf, save_path_name)
    
#svm_model_train()   
    
def svm_model_test(fin,fout):
    data=pd.read_csv(fin)
   
    model_save_path = r"../code/model_save/"   
    save_path_name=model_save_path+"svm_"+"train_model.model"
    svm_clf = joblib.load(save_path_name)
    
    feature=data.iloc[:, 2:8]
    # 标准化
    feature['num']=(feature['num']-feature['num'].mean())/(feature['num'].std())
    X=np.array(feature)
    label=svm_clf.predict(X)
    data['predict']=label
    data.to_csv(fout,index=None)
    print('情感分析：',fout)
    
fin=r'../data/room911/feature_frag_room911danmu0209.csv'
fout=r'../data/room911/senti_feature_frag_room911danmu0209.csv'
    
#svm_model_test(fin,fout)    
     