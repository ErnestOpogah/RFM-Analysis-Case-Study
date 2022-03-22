#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd


# In[16]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


## Read the sample order files showing all purchases


# In[19]:


orders = pd.read_csv('sample-orders.csv', sep = ',')


# In[20]:


orders.head()


# In[21]:


##Create the RFM Table


# In[22]:


#Recency is calculated for a point in time and the last order is Dec 31 2014, we will use that date for calcuations


# In[23]:


import datetime as dt
NOW = dt.datetime(2014,12,31)


# In[24]:


# Create the date of order as datetime


# In[25]:


orders['order_date'] = pd.to_datetime(orders['order_date'])


# In[26]:


orders.head()


# In[27]:


## Create the RFM Table


# In[31]:


rfmTable = orders.groupby('customer').agg({'order_date': lambda x: (NOW - x.max()).days, #Recency
                                          'order_id' : lambda x: len(x), #Frequency
                                           'grand_total' : lambda x: x.sum()}) #Monetary Value


# In[32]:


rfmTable['order_date'] = rfmTable['order_date'].astype(int)
rfmTable.rename(columns= {'order_date' : 'recency',
                          'order_id' : 'frequency',
                          'grand_total' : 'monetary_value'}, inplace=True)


# In[35]:


rfmTable.head()


# In[37]:


## Customer Aaron Bergman has recency 415 days, frequency 3, monetary value $887 


# In[39]:


aaron = orders[orders['customer']=='Aaron Bergman']


# In[40]:


aaron


# In[41]:


## Confirm date of Aaron purchase and compare to the recency in the rfmTable


# In[42]:


(NOW - dt.datetime(2013,11,11)).days == 415


# In[43]:


## Determining RFM Quartiles


# In[45]:


quantiles = rfmTable.quantile(q = [0.25,0.5,0.75])


# In[46]:


quantiles


# In[47]:


## Exporting quantiles to dictionary for easier use


# In[48]:


quantiles = quantiles.to_dict()


# In[49]:


quantiles


# In[50]:


## Creating the RFM Segementation Table


# In[51]:


rfmSegmentation = rfmTable


# In[ ]:





# In[52]:


## Two classes for teh RFM Segmentation since high recency is bad, while high frequency and monetary value is good 


# In[64]:


# Arguments ( x = value, p = recency, monetary_value, frequency, k = quantiles dict)
def RClass(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4
    

# Arguments ( x = value, p = recency, monetary_value, frequency, k = quantiles dict)
def FMClass(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1
    


# In[65]:


rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(RClass, args=('recency', quantiles,))
rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(FMClass, args=('frequency', quantiles,))
rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary_value'].apply(FMClass, args = ('monetary_value', quantiles))


# In[66]:


rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str)                             + rfmSegmentation.F_Quartile.map(str)                             + rfmSegmentation.M_Quartile.map(str) 


# In[67]:


rfmSegmentation.head()


# In[68]:


rfmSegmentation.to_clipboard()


# In[69]:


rfmSegmentation.to_csv('rfm-table.csv', sep=',')


# In[70]:


## Top 5 best customers? by RFM Class(111), high spender who buy recently and frequently?


# In[80]:


rfmSegmentation[rfmSegmentation['RFMClass']=='111'].sort_values('monetary_value', ascending = False).head(5)


# In[ ]:




