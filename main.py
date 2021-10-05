import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth

# Define your Client_ID, Client_Secret, and Redirect_URI
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="",
                                               scope="user-library-read"))

first_user_data = []
second_user_data = []

artists_ids = []

def get_tracks(results, data):
    for i, item in enumerate(results['items']):
        track = item['track']
        if track:
            if (track["artists"][0]["type"] == "artist"):
                artists_ids.append(track["artists"][0]["id"])
            if (len(track["album"]["images"]) >= 1):
                data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                ,track["popularity"], track["duration_ms"],track["album"]["images"][0]["url"]])
        
first_user_id = input("Enter the user id for the first user ")
second_user_id = input("Enter the user id for the second user ")

first_user_playlists = sp.user_playlists(first_user_data)
second_user_playlists = sp.user_playlists(second_user_data)

first_user_playlists_ids = []
second_user_playlists_id = []

# First user data crawler
for i, playlist in enumerate(first_user_playlists['items']):
    first_user_playlists_ids.append(playlist['id'])

for playlistId in first_user_playlists_ids:
    results = sp.playlist(playlistId, fields="tracks,next")
    tracks = results['tracks']
    get_tracks(tracks, first_user_data)

    while tracks['next']:
        tracks = sp.next(tracks)
        get_tracks(tracks, first_user_data)


for i,artistId in enumerate(artists_ids):
    results = sp.artist(artistId)
    first_user_data[i].append(results["genres"])

# Second user data crawler
artists_ids = []

for i, playlist in enumerate(second_user_playlists['items']):
    second_user_playlists_id.append(playlist["id"])

for playlistId in second_user_playlists_id:
    results = sp.playlist(playlistId, fields="tracks,next")
    tracks = results['tracks']
    get_tracks(tracks, second_user_data)

    while tracks['next']:
        tracks = sp.next(tracks)
        get_tracks(tracks, second_user_data)

for i,artistId in enumerate(artists_ids):
    results = sp.artist(artistId)
    second_user_data[i].append(results["genres"])

# File writing
headers = ["id","song","artist","album","popularity","duration","img_url","genres"]
first_user_file = "first_user_data.csv"
second_user_file = "second_user_data.csv"
    
with open(first_user_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(first_user_data)

with open(second_user_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(second_user_data)




