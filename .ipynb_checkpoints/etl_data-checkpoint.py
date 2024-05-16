dev = "AIzaSyC_t1W-rv-JHoyIcPRypT6Asw0vTT5rB98"

import googleapiclient.discovery
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = dev

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="HrnrqYxYrbk",
    maxResults=100
)

comments = []

# Execute the request.
response = request.execute()

# Get the comments from the response.
for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    public = item['snippet']['isPublic']
    comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['likeCount'],
        comment['textOriginal'],
        public
    ])

while (1 == 1):
  try:
   nextPageToken = response['nextPageToken']
  except KeyError:
   break
  nextPageToken = response['nextPageToken']
  # Create a new request object with the next page token.
  nextRequest = youtube.commentThreads().list(part="snippet", videoId="-GJgqIJsTME", maxResults=100, pageToken=nextPageToken)
  # Execute the next request.
  response = nextRequest.execute()
  # Get the comments from the next response.
  for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    public = item['snippet']['isPublic']
    comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['likeCount'],
        comment['textOriginal'],
        public
    ])

df = pd.DataFrame(comments, columns=['author', 'published_at', 'like_count', 'text','public'])
df.info()
