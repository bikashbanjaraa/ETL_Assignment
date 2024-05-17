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


# loading the data into db has been done locally from ipynb file. since i no cloud access, so i will save the file in csv and schedule the task.
# now we need to save this as a new file name for every time it runs.



import datetime

# Get the current date and time
now = datetime.datetime.now()

# Format as a string
timestamp_str = now.strftime("%Y%m%d_%H%M%S")

# Create a unique filename
filename = f"final_data_{timestamp_str}.csv"

# Save your data to this unique filename
channel_data.to_csv(filename, index=False)




