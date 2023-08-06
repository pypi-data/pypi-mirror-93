#!/usr/bin/env python
# coding: utf-8

"""
##  Function: Feature Group
##  Author: db
##  Version: 0.1
##  Created on Tue Feb  3 14:30:21 2021

"""

import pandas as pd
import numpy as np
import seaborn as sns
import math
from sklearn import preprocessing
from sklearn.decomposition import PCA
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体
#plt.rcParams["font.family"] = 'Arial Unicode MS' ## MAC电脑，输出图片中能显示中文
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.switch_backend('agg')

import warnings
warnings.filterwarnings('ignore')


# 特征相关系数

def corr_analysis(df,xnames):
    # xnames = df.columns.tolist()[1:-1]
    corr = df[xnames].corr()

#     特征相关性系数可视化
#     fig1, ax1 = plt.subplots(figsize=(20,15), nrows=1)
#     sns.heatmap(corr, annot=True, fmt='.2f', ax=ax1, cmap="YlGnBu")
#     ax1.tick_params(axis='x',labelsize=12)
#     ax1.tick_params(axis='y',labelsize=12)
#     fig1.savefig('./corr.png',bbox_inches = 'tight')
    return corr


# 特征分类

# 数据预处理
def data_preprocessing(data,xnames):
    minmax = preprocessing.MinMaxScaler()
    data_minmax = minmax.fit_transform(data[xnames])
    return data_minmax

# 测试数据集是否适合做PCA或因子分析
def adequacy_test(data):
    chi_square_value,p_value=calculate_bartlett_sphericity(data)
    if p_value <= 0.05:
        print('The p_value of Bartlett Test is {0} and the data is suitable to apply factor analysis'.format(p_value))
        result1 = True
    else:
        print('The p_value of Bartlett Test is {0} and the data is not suitable to apply factor analysis'.format(p_value))
        result1 = False

    kmo_all,kmo_model=calculate_kmo(data)
    if kmo_model >= 0.6:
        print('The KMO value is {0} and the data is suitable to apply factor analysis'.format(kmo_model))
        result2 = True
    else:
        print('The KMO value is {0} and the data is not suitable to apply factor analysis'.format(kmo_model))
        result2 = False
    result = result1 or result2
    return result

# 利用sklearn PCA确定因子个数，控制最大个数
def factor_num_calc(data,threshold=0.8,max_factor_num=20):
    pca = PCA(threshold)
    pca.fit(data)
    n_components = pca.n_components_
    print('The number of principal components is at least {0} to ensure 80% explained variance ratio'.format(n_components))
    factor_num = min(n_components,max_factor_num)
    return factor_num

### 进行因子分析，并统计特征分类情况
def variable_cluster(df,xnames,method='minres',rotation='varimax',threshold=0.8,max_factor_num=20): 
    data_minmax = data_preprocessing(df,xnames)
    print('Adequacy Test Result: \n')
    resutl = adequacy_test(data_minmax)
    print('\nDetermine the Number of Factors: \n')
    factor_num = factor_num_calc(data_minmax,threshold,max_factor_num) #确定因子个数

    fa = FactorAnalyzer(n_factors = factor_num, method = method, rotation=rotation)
    fa.fit(data_minmax) #因子分析

    factor_columns = [''.join(['group',str(i+1)]) for i in range(factor_num)]
    df_cm = pd.DataFrame(np.abs(fa.loadings_), index=xnames, columns=factor_columns)
    df_cm['factor_index'] = np.argmax(np.abs(fa.loadings_),axis=1) #根据因子载荷矩阵对特征分类

    return df_cm,factor_num

### 特征分类具体结果输出
def feature_group(df,xnames,threshold=0.8,max_factor_num=20,n_col=4):
    df_cm,factor_num = variable_cluster(df,xnames,threshold=threshold,max_factor_num=max_factor_num)
    empty = 0
    feature_classify = {}
    for num in range(factor_num):
        content = df_cm[df_cm['factor_index']==num].index.tolist()
        rows = math.ceil(len(content)/n_col)
        if rows==0:
            empty += 1
            continue
        tmp = 0
        a = []
        for i in range(rows):   
            for j in range(n_col):
                if tmp==len(content):
                    continue
                a.append(content[tmp])
                tmp += 1
            feature_classify[num+1-empty] = a
            if tmp==len(content):
                break
    # 输出结果为dataframe
    feature_classify_df = pd.DataFrame()
    for k in feature_classify.keys():
        feature_classify_df = pd.concat([feature_classify_df,pd.DataFrame({k:feature_classify[k]})],axis=1)
    return feature_classify_df








