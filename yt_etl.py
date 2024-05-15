import pandas as pd
import json
from datetime import datetime
# import s3fs
from googleapiclient.discovery import build
# from google import googleapiclient.discovery
# from google import googleapiclient.errors


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC_t1W-rv-JHoyIcPRypT6Asw0vTT5rB98"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="snippet,replies",
    videoId="-mDvD9fE3hA&ab_channel=CarHaru",
    maxResults=100
)
response = request.execute()

for item in response['items']:
    print(item['snippet']['topLevelComment']['snippet']['textDisplay'])

