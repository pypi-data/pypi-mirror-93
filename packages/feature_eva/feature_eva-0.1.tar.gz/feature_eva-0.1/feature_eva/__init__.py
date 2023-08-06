
#!/usr/bin/env python

#-*- coding:utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
##  Function: Feature Importance Evaluation
##  Author: zy
##  Version: 1.0
##  Created on Tue Feb  2 15:09:58 2021

@author: zhaoyang
"""

## 导入所需模块包


import pandas as pd
import numpy as np
import math

## 忽略警告信息
import warnings
warnings.filterwarnings('ignore')



##############1.基于统计学方法特征重要性评估###############

#####1.1 IV值计算

# 第一步:变量分箱(等频分箱)


# 对于类别数不大于分箱个数 X的数值型变量, 不做切分，类别数大于指定分箱个数 X，进行等分处理


# 生成lambda表达式，将连续变量粗分成约10等份

def gen_lambda(binning):
    
    """
    将连续变量原有值映射到新区间
    """
    temp = binning
    lambda_list = []
    for i in range(len(temp)):
        if i==0:
            lambda_list = 'lambda x: %d if (x<=%f)'%(temp.loc[i,'coarse_bin'],temp.loc[i,'ub'])
        elif i!=len(binning)-1:
            lambda_list = lambda_list + ' else %d if (x>%f) & (x<=%f)'%(temp.loc[i,'coarse_bin'],temp.loc[i,'lb'],temp.loc[i,'ub'])
        else:
            lambda_list = lambda_list + ' else %d if (x>%f) else np.nan'%(temp.loc[i,'coarse_bin'],temp.loc[i,'lb'])
    return lambda_list

def cut_bin(data,label,exclude_cols):
    
    """
    data:  原始宽表
    label: 标签列
    exclude_col: 需要过滤的变量列名，可写多个
    默认分十箱
    """
    # 剔除非数值型变量 
    var_types = data.drop(exclude_cols,axis=1).dtypes.reset_index()
    var_types.columns = ['var','type'] #float64, int64, object
    numeric_col = var_types[(var_types['type']=='float64')|(var_types['type']=='int64')]['var'].tolist()
    exclude_cols = exclude_cols + var_types[var_types['type']=='object']['var'].tolist()
    
    # 分箱后的data
    data_coarse_bin = data[exclude_cols]
    
    # 对数值型变量依次进行分箱处理
    for col in numeric_col:
        if len(data[col].unique())<10:
            data_coarse_bin[col] =data[col]
        else:
            split_values = data[col].quantile(np.linspace(0.05,0.95,num=9)).reset_index()[col].unique()
            binning = pd.DataFrame({'lb':[-99999]+split_values.tolist(),'ub':split_values.tolist()+[99999]}).reset_index()
            binning.rename(columns={'index':'coarse_bin'},inplace=True)
            binning['var'] = col
            binning = binning[['var','coarse_bin','lb','ub']]
            lambda_list = gen_lambda(binning)
            data_coarse_bin[col] = list(map(eval(lambda_list),data[col]))
    return data_coarse_bin

# 第二步:计算IV

def IV(data,label,exclude_cols):
    data_new = cut_bin(data,label,exclude_cols)
    IV_list=[]
    calc_cols=data_new.drop(exclude_cols,axis=1).columns.values
    for col in calc_cols:
        Xvar = data_new[col]
        Yvar = data_new[label]
        N_0  = np.sum(Yvar==0)
        N_1 = np.sum(Yvar==1)
        N_0_group = np.zeros(np.unique(Xvar).shape)
        N_1_group = np.zeros(np.unique(Xvar).shape)
        for i in range(len(np.unique(Xvar))):
            N_0_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 0)].count()
            N_1_group[i] = Yvar[(Xvar == np.unique(Xvar)[i]) & (Yvar == 1)].count()
        iv = np.sum((N_0_group/N_0 - N_1_group/N_1) * np.log((0.0000000000001+N_0_group/N_0)/(0.0000000000001+N_1_group/N_1)))
        IV_list.append(iv)
    return  IV_list

#####1.1 Gini计算
    
def Gini(data,label,exclude_cols):
    gini_list=[]
    calc_cols=data.drop(exclude_cols,axis=1).columns.values
    data_new = cut_bin(data,label,exclude_cols)
    for col in calc_cols:    
        temp = data_new[[col,label]].reset_index().groupby([col,label]).agg({'index':'count'}).reset_index()
        temp.columns = [col,label,'num']
        temp_wide = temp.pivot_table(index=col,columns=label,values='num').reset_index()
        temp_wide.columns = [col,'count0','count1']
        temp_wide['count0'] = temp_wide['count0'].apply(lambda x: 0 if math.isnan(x) else x)
        temp_wide['count1'] = temp_wide['count1'].apply(lambda x: 0 if math.isnan(x) else x)
        temp_wide['pct0'] = temp_wide['count0'].apply(lambda x: x/temp_wide['count0'].sum())
        pct0_list = temp_wide['pct0'].tolist()

        cum_pct0 = np.cumsum(sorted(np.append(pct0_list, 0)))
        sum_pct0 = cum_pct0[-1]
        xarray = np.array(range(0, len(cum_pct0))) / np.float(len(cum_pct0)-1)
        yarray = cum_pct0 / sum_pct0
        B = np.trapz(y=yarray, x=xarray)
        A = 0.5 - B
        gini = A / (A+B)
        gini_list.append(gini)
    return gini_list


####1.3 卡方计算
    
def select_chi2(data,label,exclude_cols):
    
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2
    gini_list=[]
    cols=data.drop(exclude_cols,axis=1).columns.values
    x = data[cols]
    y = data[label]
    chi2,p=chi2(x, y)
    return chi2


### 1.4 最大信息系数评估

def mine(data,label,exclude_cols):
    from minepy import MINE
    mine = MINE(alpha=0.6, c=15)
    mic_scores = []
    cols=data.drop(exclude_cols,axis=1).columns.values
    data_new = cut_bin(data,label,exclude_cols)
    x = data_new[cols]
    y = data_new[label]
    for i in range(x.shape[1]):
        mine.compute_score(x.iloc[:,i], y)
        m = mine.mic()
        mic_scores.append(m)
    return mic_scores



##############2. 基于学习模型特征重要性评估###############

###2.1 随机森林

def select_rf(data,label,exclude_cols):
    
    from sklearn.ensemble import RandomForestClassifier 
    data_new=data.drop(exclude_cols,axis=1)
    cols=data_new.columns.tolist()
    x = data[cols]
    y = data[label]
    rfmodel = RandomForestClassifier(random_state=0)
    rfmodel = rfmodel.fit(x, y)
    return rfmodel.feature_importances_


##2.2 特征稳定性评估
    
def select_Lasso(data,label,exclude_cols):
    
    from stability_selection import RandomizedLasso
    data_new=data.drop(exclude_cols,axis=1)
    cols=data_new.columns.tolist()
    x = data[cols]
    y = data[label]
    rlasso = RandomizedLasso(alpha=0.025)
    rlasso.fit(x, y)
    return rlasso.coef_

##2.3 递归特征消除排序


def select_rfe(data,label,exclude_cols):
    
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LinearRegression
    data_new=data.drop(exclude_cols,axis=1)
    cols=data_new.columns.tolist()
    x = data[cols]
    y = data[label]
    lr = LinearRegression()
  
    rfe = RFE(lr, n_features_to_select=1)
    rfe.fit(x,y)
    return rfe.ranking_


 
##############3. 结果汇总，特征排序###############   

def Feature_importance(data,exclude_cols,label,methods):

    result = pd.DataFrame()
    exclude_cols.append(label)
    result['feature'] = data.drop(exclude_cols,axis=1).columns.values.tolist()
    result['rank_sum'] = 0
    if 'iv' in methods:        
        result['IV'] = IV(data,label,exclude_cols)
        result['IV_rank'] = result['IV'].rank(ascending=False)
        result['rank_sum'] =result['rank_sum']+result['IV_rank']
    if 'gini' in methods:        
        result['Gini'] = Gini(data,label,exclude_cols)
        result['Gini_rank'] = result['Gini'].rank(ascending=True)
        result['rank_sum'] =result['rank_sum']+result['Gini_rank']
    if 'chi2' in methods:
        result['chi2'] = select_chi2(data,label,exclude_cols)
        result['chi2_rank'] = result['chi2'].rank(ascending=False)
        result['rank_sum'] =result['rank_sum']+result['chi2_rank']
    if 'mic' in methods:
        result['mic'] = mine(data,label,exclude_cols)
        result['mic_rank'] = result['mic'].rank(ascending=False)
        result['rank_sum'] =result['rank_sum']+result['mic_rank']
    if 'rf' in methods:
        result['rf'] = select_rf(data,label,exclude_cols)
        result['rf_rank'] = result['rf'].rank(ascending=False)
        result['rank_sum'] =result['rank_sum']+result['rf_rank']
    if 'Lasso' in methods:
        result['Lasso'] = select_Lasso(data,label,exclude_cols)
        result['Lasso_rank'] = result['Lasso'].rank(ascending=False)
        result['rank_sum'] =result['rank_sum']+result['Lasso_rank']
    if 'rfe' in methods:
        result['rfe'] = select_rfe(data,label,exclude_cols)
        result['rank_sum'] =result['rank_sum']+result['rfe']
    return result

if __name__ == '__main__':

    Feature_importance(data,exclude_cols,label,methods)

