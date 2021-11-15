import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth
import time
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="",
                                               scope="user-library-read"))

ids1 = []
ids2 = []

with open("first_user_data.csv", encoding="utf-8-sig") as f:
   reader = csv.reader(f)
   next(reader, None)
   for row in reader:
      ids1.append(row[0])

with open("second_user_data.csv", encoding="utf-8-sig") as f:
   reader = csv.reader(f)
   next(reader, None)
   for row in reader:
      ids2.append(row[0])

audio_features_1 = []
audio_features_2 = []

for i in range(0, len(ids1), 100):
    chunk = ids1[i:i+100]
    features = sp.audio_features(chunk)
    for feature in features:
        if (feature is not None):
            audio_features_1.append([feature["id"], feature["danceability"], feature["energy"], feature["key"],
            feature["loudness"], feature["mode"], feature["speechiness"], feature["acousticness"], 
            feature["instrumentalness"], feature["liveness"], feature["valence"], feature["tempo"]])

for i in range(0, len(ids2), 100):
    chunk = ids2[i:i+100]
    features = sp.audio_features(chunk)
    for feature in features:
        if (feature is not None):
            audio_features_2.append([feature["id"], feature["danceability"], feature["energy"], feature["key"],
            feature["loudness"], feature["mode"], feature["speechiness"], feature["acousticness"], 
            feature["instrumentalness"], feature["liveness"], feature["valence"], feature["tempo"]])

headers = ["id","danceability","energy","key","loudness","mode","speechiness","acousticness",
"instrumentalness", "liveness", "valance", "tempo"]
audio_features_1_file = "audio_features_1.csv"
audio_features_2_file = "audio_features_2.csv"
    

with open(audio_features_1_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(audio_features_1)

with open(audio_features_2_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(audio_features_2)

print("Finishes loading data")
