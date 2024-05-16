#!/usr/bin/env python
# coding: utf-8

# In[4]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[36]:


api_key = 'AIzaSyC_t1W-rv-JHoyIcPRypT6Asw0vTT5rB98'
# channel_id = 'UCnz-ZXXER4jOvuED5trXfEA'
channel_ids = ['UCnz-ZXXER4jOvuED5trXfEA',#techtfq
               'UCLLw7jmFsvfIVaUFsLs8mlQ', #luke barousse
               'UCiT9RITQ9PW6BhXK0y2jaeg', #ken jee
               'UC7cs8q-gJRlGwj4A8OmCmXg', #alex the analyst
               'UC2UXDak6o7rBm23k3Vv5dww'] #tina huang

api_service_name = "youtube"
api_version = "v3"
youtube = build(
    api_service_name, api_version, developerKey=api_key) #created youtube service.


# In[52]:


#now extracting the channel details.
def get_channel_stats(youtube,channel_ids):
    all_data=[]
    request  = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response =request.execute()
    # for i in range(len(response['items'])):
    #     data =dict(channel_name = response['items'][i]['snippet']['title'],
    #                subscirbers = response['items'][i]['statistics']['subscriberCount'], #check in jsonformatter and validator
    #                views = response['items'][i]['statistics']['viewCount'],
    #                total_video = response['items'][i]['statistics']['videoCount']
    #           )
    #     all_data.append(data)
        
    return response


# In[53]:


get_channel_stats(youtube,channel_ids)


# # we dont need all these json files. 
# * we used json formattor and validator [link](https://jsonformatter.curiousconcept.com/#) and filter only those information that we need

# # Function to get channel statistics

# In[40]:


#now extracting the channel details.
def get_channel_stats(youtube,channel_ids):
    all_data=[]
    request  = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response =request.execute()
    for i in range(len(response['items'])):
        data =dict(channel_name = response['items'][i]['snippet']['title'],
                   subscirbers = response['items'][i]['statistics']['subscriberCount'], #check in jsonformatter and validator
                   views = response['items'][i]['statistics']['viewCount'],
                   total_video = response['items'][i]['statistics']['videoCount']
              )
        all_data.append(data)
        
    return all_data  # return response if want json file.


# In[43]:


channel_statistics = get_channel_stats(youtube,channel_ids)


# In[45]:


channel_data =pd.DataFrame(channel_statistics)


# In[46]:


channel_data


# In[47]:


#coverted these data to integer and do further visualization because these data are boject type


# In[48]:


channel_data.dtypes


# In[51]:


channel_data['subscirbers'] = pd.to_numeric(channel_data['subscirbers'])
channel_data['views'] = pd.to_numeric(channel_data['views'])
channel_data['total_video'] = pd.to_numeric(channel_data['total_video'])
channel_data.dtypes


# # bar plot: who has highest subscribers

# In[60]:


# sns.set(rc={'figure.figsize':(10,8)})
# ax=sns.barplot(x='channel_name',y='subscribers',data=channel_data) 


# # who has more videos?

# In[62]:


# sns.set(rc={'figure.figsize':(10,8)})
# ax=sns.barplot(x='channel_name',y='total_video',data=channel_data) 


# In[63]:


# now for etl purpose we need to load this database into postgres db


# In[64]:


import psycopg2


# In[65]:


try:
    connection = psycopg2.connect(
        user = "biki",
        password = "bikash123",
        host = "localhost",
        port = "5432",
        database = "etl_assignment"
    )
    cursor = connection.cursor()
    print("Connected to the database")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)


# In[69]:


channel_data


# In[71]:


record_inserting_to_db= list(channel_data.itertuples(index=False,name=None))


# *
# * since pandas df cannot be directly added to the db.because execute method wants tuples values and df is providing series  instead of single values

# In[74]:


record_inserting_to_db  


# # inserting into a db.

# In[79]:


insert_query = """ INSERT INTO youtube_analysis (Channel_name, Subscriber,Views,Total_videos) VALUES (%s,%s,%s,%s)"""

for record in record_inserting_to_db:
    record_to_insert = (record[0], record[1], record[2], record[3])  
    try:
        cursor.execute(insert_query, record_to_insert)
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        continue

connection.commit()


# ![ksnip_20240516-163521.png](attachment:23de3b94-76f7-4c49-b222-319893dc6823.png)

# In[ ]:


# insert_query = """ INSERT INTO youtube_analysis (Channel_name, Subscriber,Views,Total_videos) VALUES (%s,%s,%s,%s)"""

# for record in record_inserting_to_db:
#     record_to_insert = (record[0], record[1], record[2], record[3])  
#     cursor.execute(insert_query, record_to_insert)

# # connection.commit()


# In[80]:


# # inserting into a db.
# insert_query = """ INSERT INTO videos (Channel_name, Subscriber,Views,Total_videos) VALUES (%s,%s,%s,%s,%s)"""
# record_to_insert = (record_inserting_to_db['channel_name'], record_inserting_to_db['subscribers'], record_inserting_to_db['views'],record_inserting_to_db['total_video'])

# cursor.execute(insert_query, record_to_insert)
# connection.commit()
# print("Record inserted successfully")


# # data has been stored in the postgres.
# * since we have hosted this in local machine. we cannot use it to store data after running manually from the github workflow, so we will store the updated data as CSV file with different file name 

# # saving data as the csv

# In[81]:


channel_data.to_csv("final_data_in_csv")


# In[82]:


# but we need to save this as a new file name for every time it runs.


# In[84]:


import datetime

# Get the current date and time
now = datetime.datetime.now()

# Format as a string
timestamp_str = now.strftime("%Y%m%d_%H%M%S")

# Create a unique filename
filename = f"final_data_{timestamp_str}.csv"

# Save your data to this unique filename
channel_data.to_csv(filename, index=False)


# In[ ]:




