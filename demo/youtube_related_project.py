# -*- coding: utf-8 -*-
"""youtube-related-project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1woKaCYWW8-TQXnBERodyLXWJmpkBysAQ
"""

#youtube data v3 api service initialization
from googleapiclient import discovery
API_KEY = "AIzaSyDi-LpZo5ULSVY3ZcS9gb8Errn-JCgrugQ"
youtube = discovery.build("youtube","v3",developerKey=API_KEY)

#get parsed youtube video info using video id 
def getParsedVideoInfo(video_id):
    request = youtube.videos().list(part="snippet,contentDetails,snippet,statistics",id=video_id)
    response = request.execute()
    items = response["items"][0]
    kind = items["kind"]
    video_id = items["id"]
    #snippet
    published_date = items["snippet"]["publishedAt"]
    channel_id = items["snippet"]["channelId"]
    video_title = items["snippet"]["title"]
    video_description = items["snippet"]["description"]
    #thumbnail_url = items["snippet"]["thumbnails"]["maxres"]["url"]
    channel_title = items["snippet"]["channelTitle"]
    meta_tags = items["snippet"]["tags"]
    category_id = items["snippet"]["categoryId"]
    #content details
    duration = items["contentDetails"]["duration"][2:]
    #stats
    view_count = items["statistics"]["viewCount"]
    like_count = items["statistics"]["likeCount"]
    dislike_count = items["statistics"]["dislikeCount"]
    #favorite_count = items["statistics"]["favoriteCount"]
    #comment_count = items["statistics"]["commentCount"]
    
    parsed_response = dict(kind=kind,
                           video_id=video_id,
                           published_date =published_date,
                           channel_id=channel_id,
                           video_title=video_title,
                           video_description=video_description,
                           #thumbnail_url=thumbnail_url,
                           channel_title=channel_title,
                           meta_tags=meta_tags,
                           category_id=category_id,
                           duration=duration,
                           view_count=view_count,
                           like_count=like_count,
                           dislike_count=dislike_count,
                           #favorite_count=favorite_count,
                           #comment_count=comment_count
                           )
    return parsed_response

#get youtube channel info using channel id
def getChannelInfoUsingChannelId(channel_id):
  request = youtube.channels().list(part="contentDetails,snippet,statistics", id=channel_id)
  response = request.execute()
  return response

#get playlists info using playlist id
def getPlaylistItemsInfo(playlist_id,page_token):
  request = youtube.playlistItems().list(part="contentDetails",playlistId=playlist_id,pageToken=page_token)
  response = request.execute()
  return response

#get list of all video id from playlist using playlist id
def getAllVideoIdFromPlaylist(playlist_id):
  
  page_token = None
  video_id_list = []
  while True:
    response = getPlaylistItemsInfo(playlist_id,page_token)
    items = response["items"]
    for vid_id in items:
      video_id_list.append(vid_id['contentDetails']["videoId"])

    if "nextPageToken" in response:
      page_token = response.get("nextPageToken")
      response = getPlaylistItemsInfo(playlist_id,page_token)
      items = response["items"]
    else:
      break

  return video_id_list

#get video id from youtube channel using channel id
def getAllVideoIdUsingChannelId(channel_id):
  uploads = getChannelInfoUsingChannelId(channel_id)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
  vid_id_list = getAllVideoIdFromPlaylist(uploads)
  return video_id_list

#get channel id uing video id
def getChannelIdUsingVideoId(video_id):
  return getParsedVideoInfo(video_id)["channel_id"]

import pandas as pd
video_id_list = 0
video_id_list = getAllVideoIdUsingChannelId("UCV0qA-eDDICsRR9rPcnG7tw")
data = []
for i in video_id_list:
  val = getParsedVideoInfo(i)
  data.append(val)

print(data)

df = pd.read_csv("report.csv")
df = df[['video_title','view_count','like_count','dislike_count']]
df.view_count.astype(int)
df.like_count.astype(int)
df.dislike_count.astype(int)
df.like_count.max()