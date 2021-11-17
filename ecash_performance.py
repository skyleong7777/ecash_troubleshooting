# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:07:41 2021

@author: skyleong
"""

#import package
import streamlit as st
import pandas as pd
import numpy as np
st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="ecash troubleshooting", page_icon=":chart_with_upwards_trend:", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

#1 title and subheader
st.title(':chart_with_upwards_trend:Suspecting data of ecash point')
st.subheader('Data analysis')

#2 upload dataset
upload=st.file_uploader('Please upload a dataset for analysis:(in CSV format)',type='csv')

if upload is not None:
    df = pd.read_csv(upload,parse_dates=['GamingDt'])


#Date range max/min   
       

if upload is not None:
    if st.checkbox('Preview the date range'):
            st.write(df['GamingDt'].min(), df['GamingDt'].max())
            
# total number transaction of ecash

if upload is not None:
    tol_ecash_count=df.TranCode.value_counts()
    tol_ecash_count=pd.DataFrame(tol_ecash_count)
    tol_ecash_count=tol_ecash_count.reset_index()
    tol_ecash_count=tol_ecash_count.rename(columns={'index':'TranCode','TranCode':'Total_records'})
    trancode_dict={'CSHWDPR':'Point_Reuqest','CSHSTLPR':'Point_Settle','CSHWDCR':'Promo_Request','CSHSTLCR':'Promo_Settle','CSHDEPCR':'ECash_Deposite'}
    tol_ecash_count['TranType']=tol_ecash_count['TranCode'].map(trancode_dict)
    tol_ecash_count=tol_ecash_count[['TranCode','TranType','Total_records']]
    if st.checkbox('Total number transaction of ecash'):
            st.write(tol_ecash_count)    

#suspecting data of ecash       
if upload is not None:
    if st.checkbox('suspecting data of ecash'):
        sus_ecash=df.loc[np.where((df['AuthAward']-df['AwardUsed']==0 ) & (df['TranCode']!='CSHDEPCR'))]
        st.write(sus_ecash) 
        st.write('Total records of suspecting ecash transaction ')
        st.write(len(df.loc[np.where((df['AuthAward']-df['AwardUsed']==0 ) & (df['TranCode']!='CSHDEPCR'))]))
        st.download_button(label='Download transaction of suspecting ecash as csv', data=sus_ecash.to_csv(), mime='text/csv')
        
# Number of case per day
if upload is not None:
            sus_ecash=df.loc[np.where((df['AuthAward']-df['AwardUsed']==0 ) & (df['TranCode']!='CSHDEPCR'))]        
            case_ecash=sus_ecash.groupby('GamingDt')['Acct'].count()
            case_ecash1=pd.DataFrame(case_ecash)
            if st.checkbox('Number of case per day'):
                st.bar_chart(data=case_ecash1)


#clear pending eCash
if upload is not None:
    df1=df.drop_duplicates(subset ='ItemID',keep = False)
    df2=df1[df1['TranCode']!='CSHDEPCR']
    if st.checkbox('Total number clear pending transaction of ecash'):
            st.write(df2)
            st.download_button(label='Download the transaction of clear pending ecash as csv', data=df2.to_csv(), mime='text/csv')
                
# number of total download point
if upload is not None:
    value_counts_plt_wd=df.loc[df.TranCode=='CSHWDPR'][['TranCode','AuthAward','RedeemPts']].value_counts().sort_values(ascending=False).head(10)
    value_counts_plt_wd=value_counts_plt_wd.reset_index()
    value_counts_plt_wd=value_counts_plt_wd.rename(columns={0:'number_of_point_download'})
    value_counts_plt_wd=value_counts_plt_wd.drop(['TranCode'],axis=1)
    if st.checkbox('Top 10 of ecash $ of point'):
            st.write(value_counts_plt_wd) 

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        