#!/usr/bin/env python
# coding: utf-8

# <hr style="margin-bottom: 40px;">
# 
# <img src="utilities/911-ecall.jpg"
#     style="width:300px; float: right; margin: 0 40px 40px 40px;"></img>
# 
# # 911 Calls - Basic Data Analysis Project

# For this project I will be analyzing some 911 call data (Montgomery County, PA) from [Kaggle](https://www.kaggle.com/mchirico/montcoalert). The data contains the following fields:
# 
# * lat : String variable, Latitude
# * lng: String variable, Longitude
# * desc: String variable, Description of the Emergency Call
# * zip: String variable, Zipcode
# * title: String variable, Title
# * timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# * twp: String variable, Township
# * addr: String variable, Address
# * e: String variable, Dummy variable (always 1)

# ## Data and Setup

# ____
# **Importing numpy and pandas.**

# In[1]:


import numpy as np
import pandas as pd


# **Importing visualization libraries and setting %matplotlib inline.**

# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# **Reading in the csv file as a dataframe.**

# In[3]:


df = pd.read_csv('911.csv')


# **Check the info() of the df.**

# In[4]:


df.info()


# **Checking the head of df.**

# In[5]:


df.head()


# ## Basic Questions about the dataset

# **What are the top 5 zipcodes for 911 calls?**

# In[6]:


df['zip'].value_counts().head(5)


# **What are the top 5 townships (twp) for 911 calls?**

# In[7]:


df['twp'].value_counts().head()


# **How many unique title codes are there?**

# In[8]:


df['title'].nunique()


# ## Creating new features

# **In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Using .apply() with a custom lambda expression I create a new column called "Reason" that contains this string value.** 
# 
# **For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS.**

# In[9]:


df['title'].apply(lambda x: x.split(':')[0])


# **What is the most common Reason for a 911 call based off of this new column?**

# In[10]:


df['Reason'] = df['title'].apply(lambda x: x.split(':')[0])
df


# **Using seaborn for creating a countplot of 911 calls by Reason.**

# In[11]:


sns.countplot(x='Reason',data=df, palette='BuGn_r')


# ___
# **Dealing with datetime data type.**

# In[12]:


df['timeStamp'].iloc[0]


# In[13]:


type(df['timeStamp'].iloc[0])


# **Using [pd.to_datetime](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html) for converting the column from strings to DateTime objects.**

# In[14]:


df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['timeStamp'].iloc[0]


# **Creating 3 new columns called Hour, Month, and Day of Week based off of the timeStamp column.**

# In[15]:


df['hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['dayofweek'] = df['timeStamp'].apply(lambda time: time.dayofweek)
df['month'] = df['timeStamp'].apply(lambda time: time.month)
df


# **Using the .map() method with the following dictionary to map the actual string names to the day of the week:**
# 
#     dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[16]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
dmap


# In[17]:


df['dayofweek'] = df['dayofweek'].map(dmap)
df


# **Creating a countplot of the day of week column with the hue based off of the Reason column**

# In[18]:


sns.countplot(x='dayofweek',data=df,hue='Reason',palette='BuGn_r')
plt.legend(bbox_to_anchor=(1.05,1),loc=2, borderaxespad=0.)


# **Creating a countplot of the month column with the hue based off of the Reason column**

# In[19]:


sns.countplot(x='month',data=df,hue='Reason',palette='viridis')
plt.legend(bbox_to_anchor=(1.05,1),loc=2, borderaxespad=0.)


# _____
# 
# **Drawing a simple line plot that fills in the missing months**

# ** Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame. **

# In[20]:


byMonth = df.groupby('month').count()
byMonth


# In[21]:


byMonth['lat'].plot()


# **Creating a linear fit on the number of calls per month.**

# In[23]:


sns.lmplot(x='month',y='twp',data=byMonth.reset_index())


# **Creating a new column called 'Date' that contains the date from the timeStamp column.** 

# In[25]:


df['date'] = pd.to_datetime(df['timeStamp']).apply(lambda x: x.date())
df.sample(5)


# In[31]:


df.groupby(by='date').count()['lat'].plot()
plt.tight_layout()


# **Quantity of calls over time, separated by reason.**

# In[32]:


df[df['Reason']=='Traffic'].groupby('date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[33]:


df[df['Reason']=='EMS'].groupby('date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[34]:


df[df['Reason']=='Fire'].groupby('date').count()['lat'].plot()
plt.title('FireEms')
plt.tight_layout()


# ____
# **Creating a heatmap.**

# In[50]:


date_hour = df.groupby(by=['dayofweek','hour']).count


# **After analyzing the data I can say:**
# 
# - the most commom reason is EMS(Emergy Medical Services) followed by Traffic.
# - Looking at the simple regression line, it seems that the quantity emergency calls decreases over the months of a year.
# - Analyzing the heatmap I could infer that there are more call done between 7am and 6pm, mostly from monday to Friday.
