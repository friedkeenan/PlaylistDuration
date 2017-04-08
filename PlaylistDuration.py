import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
import datetime as dt
import isodate
from functools import reduce
from config import *
message="Woops"
scope="https://www.googleapis.com/auth/youtube"
name="youtube"
version="v3"
yt=build(name,version, developerKey=apiKey)
playlistId=input("Playlist IDs (separated by commas): ").split(",")
delta=[]
for pId in playlistId:
  pId=pId.strip(",")
  playlistItemsRequest=yt.playlistItems().list(part="contentDetails",playlistId=pId,maxResults=50)
  playlistVids=[]
  print("Getting playlistItems of playlist "+str(playlistId.index(pId)+1)+"...")
  while playlistItemsRequest:
      playlistItems=playlistItemsRequest.execute()
      playlistVids+=playlistItems["items"]
      playlistItemsRequest=yt.playlistItems().list_next(playlistItemsRequest,playlistItems)
  print("Done")
  vids=[]
  print("Converting to videos...")
  for v in playlistVids:
      video=yt.videos().list(part="contentDetails",id=v["contentDetails"]["videoId"]).execute()["items"][0]
      vids.append(video)
      print("Converted "+str(playlistVids.index(v)+1)+"/"+str(len(playlistVids)))
  print("Done")
  total=dt.timedelta()
  print("Getting total duration...")
  for v in vids:
      duration=isodate.parse_duration(v["contentDetails"]["duration"])
      total+=duration
  print("Done")
  delta.append(total)
deltatotal=reduce(lambda x,y:x+y,delta)
for d in delta:
  print("Duration of playlist "+str(delta.index(d)+1)+": "+str(d))
print("Total Duration: "+str(deltatotal))
