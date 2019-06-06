import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def melter():
    df1 = pd.read_csv('tables/2016Census_G04A_SA_POA.csv')
    df2 = pd.read_csv('tables/2016Census_G04B_SA_POA.csv')
    df = pd.merge(df1, df2, how = 'inner', on = 'POA_CODE_2016')
    df.head()
    df.shape
    df_melt = pd.melt(df, id_vars = 'POA_CODE_2016', var_name = 'Melted_Categories', value_name = 'Number of People')
    df_melt.index = df_melt['POA_CODE_2016']
    df_melt['Label_List'] = df_melt['Melted_Categories'].str.split('_')
    df_melt['1st'] = df_melt['Label_List'].str.get(0)
    df_melt['2nd'] = df_melt['Label_List'].str.get(1)
    df_melt['Age_From'] = df_melt['Label_List'].str.get(2)
    df_melt['Age_To'] = df_melt['Label_List'].str.get(-2)
    df_melt['Gender'] = df_melt['Label_List'].str.get(-1)
    df_melt.head()
    df_melt.shape
    df_melt_categories = df_melt[df_melt['1st']== 'Age']
    df_melt_categories = df_melt_categories.loc[:,['Number of People', 'Age_From', 'Age_To', 'Gender']]
    df_melt_totals = df_melt[df_melt['1st']=='Tot']
    df_melt_totals = df_melt_totals.loc[:,['Number of People', '2nd']]
    df_melt_totals['Gender'] = df_melt_totals['2nd']
    del df_melt_totals['2nd']
    df_melt_totals = df_melt_totals.sort_index(0)
    df_melt_categories['Postal Code'] = df_melt_categories.index.str.extract('(\d{4})')
    df_melt_categories = df_melt_categories.sort_values(by = ['Postal Code', 'Age_From'])
    df_melt_totals.head()
    df_melt_categories.head()
    return(list(df_melt_categories))