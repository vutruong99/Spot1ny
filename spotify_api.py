import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth
import urllib.request

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog = True, client_id="70d38d6792fd47338dcb482fc2aba603",
                                                    client_secret="0920bf226b40474bb49c1aca271b6de5",
                                                    redirect_uri="http://localhost:8888/callback",
                                                    scope="user-library-read"))

 
first_user_id = "lwqh6n22yf8j1esekvl1dghpj"
second_user_id = "hc7cn89l7knx2wknggi5g6c8j"
# first_user_id = "22b6thxi5ucw3wzjsw3hihhiy"
# second_user_id = "ouhb2zru9tnwe0ncyvuyrq3s8"

def spotify_user_info_scraper():

    first_user = sp.user(first_user_id)
    first_user_data = []
    first_user_data.append([first_user["id"], first_user["display_name"], first_user["images"][0]["url"]])

    second_user = sp.user(second_user_id)
    second_user_data = []
    second_user_data.append([second_user["id"], second_user["display_name"], second_user["images"][0]["url"]])

    headers = ["id","display_name","image_url"]
    first_user_info = "data/user_info_1.csv"
    second_user_info = "data/user_info_2.csv"

    with open(first_user_info, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(first_user_data)

    with open(second_user_info, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(second_user_data)

    retrieve_avatars()

def spotify_playlists_scraper(mode):
    
    first_user_data = []
    second_user_data = []
    headers = ["id","song","artist","album","popularity","duration","genres"]
    artists_ids = []

    def get_tracks(results, data):
        if mode == "partial":
            for i, item in enumerate(results['items']):
                if i == 5:
                    break
                track = item['track']
                if track:
                    if (track["artists"][0]["type"] == "artist" and track["artists"][0]["id"] != None):
                        artists_ids.append(track["artists"][0]["id"])
                        # data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                        #     ,track["popularity"], track["duration_ms"],track["album"]["images"][0]["url"]])
                        data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                                ,track["popularity"], track["duration_ms"]])
        else:
            for i, item in enumerate(results['items']):
                track = item['track']
                if track:
                    if (track["artists"][0]["type"] == "artist" and track["artists"][0]["id"] != None):
                        artists_ids.append(track["artists"][0]["id"])
                        # data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                        #     ,track["popularity"], track["duration_ms"],track["album"]["images"][0]["url"]])
                        data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                                ,track["popularity"], track["duration_ms"]])
   
    # Uncomment the two lines below if you wish to enter your own ids and test
    # first_user_id = input("Enter the user id for the first user ")
    first_user_playlists = sp.user_playlists(first_user_id)
    # second_user_id = input("Enter the user id for the second user ")
    second_user_playlists = sp.user_playlists(second_user_id)

    first_user_playlists_ids = []
    second_user_playlists_id = []

    print("Scraping first user's playlists\n")
    # First user data crawler
    for i, playlist in enumerate(first_user_playlists['items']):
        first_user_playlists_ids.append(playlist['id'])

    for playlistId in first_user_playlists_ids:
        results = sp.playlist(playlistId, fields="tracks,next")
        tracks = results['tracks']
        get_tracks(tracks, first_user_data)

        if mode == "partial":
            break
        
        while tracks['next']:
            tracks = sp.next(tracks)
            get_tracks(tracks, first_user_data)

    for i,artistId in enumerate(artists_ids):
        results = sp.artist(artistId)
        first_user_data[i].append(results["genres"])

    print(headers)
    for i,res in enumerate(first_user_data):
        if i == 5:
            break
        print(res)
        
    print("\nThe first user's dataset has " + str(len(first_user_data)) + " rows and 7 columns\n")
    
    print("Scraping second user's playlists\n")

    # Second user data crawler
    artists_ids = []

    for i, playlist in enumerate(second_user_playlists['items']):
        second_user_playlists_id.append(playlist["id"])

    for playlistId in second_user_playlists_id:
        results = sp.playlist(playlistId, fields="tracks,next")
        tracks = results['tracks']
        get_tracks(tracks, second_user_data)

        if mode == "partial":
            break
        
        while tracks['next']:
            tracks = sp.next(tracks)
            get_tracks(tracks, second_user_data)

    for i,artistId in enumerate(artists_ids):
        results = sp.artist(artistId)
        second_user_data[i].append(results["genres"])

    print(headers)
    for i,res in enumerate(second_user_data):
        if i == 5:
            break
        print(res)
    print("\nThe second user's dataset has " + str(len(second_user_data)) + " rows and 7 columns\n")
    
    # File writing
    first_user_file = "data/user_songs_1.csv"
    second_user_file = "data/user_songs_2.csv"
            
    with open(first_user_file, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(first_user_data)

    with open(second_user_file, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(second_user_data)

def spotify_audio_features_scraper():
    ids1 = []
    ids2 = []

    headers = ["id","danceability","energy","key","loudness","mode","speechiness","acousticness",
    "instrumentalness", "liveness", "valance", "tempo"]

    with open("data/user_songs_1.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            ids1.append(row[0])

    with open("data/user_songs_2.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            ids2.append(row[0])

    audio_features_1 = []
    audio_features_2 = []

    print("Scraping first user's songs' audio features\n")
    for i in range(0, len(ids1), 100):
        chunk = ids1[i:i+100]
        features = sp.audio_features(chunk)
        for feature in features:
            if (feature is not None):
                audio_features_1.append([feature["id"], feature["danceability"], feature["energy"], feature["key"],
                feature["loudness"], feature["mode"], feature["speechiness"], feature["acousticness"], 
                feature["instrumentalness"], feature["liveness"], feature["valence"], feature["tempo"]])
    
    print(headers)
    for i,res in enumerate(audio_features_1):
        if i == 5:
            break
        print(res)
    print("\nThe first audio features dataset has " + str(len(audio_features_1)) + " rows and 12 columns\n")
    
    print("Scraping second user's songs' audio features\n")
    for i in range(0, len(ids2), 100):
        chunk = ids2[i:i+100]
        features = sp.audio_features(chunk)
        for feature in features:
            if (feature is not None):
                audio_features_2.append([feature["id"], feature["danceability"], feature["energy"], feature["key"],
                feature["loudness"], feature["mode"], feature["speechiness"], feature["acousticness"], 
                feature["instrumentalness"], feature["liveness"], feature["valence"], feature["tempo"]])

    print(headers)
    for i,res in enumerate(audio_features_2):
        if i == 5:
            break
        print(res)
    print("\nThe second audio features dataset has " + str(len(audio_features_2)) + " rows and 12 columns\n")

    audio_features_1_file = "data/audio_features_1.csv"
    audio_features_2_file = "data/audio_features_2.csv"
        
    with open(audio_features_1_file, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(audio_features_1)

    with open(audio_features_2_file, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(audio_features_2)

def billboard_to_spotify_id():  
    billboard_100_ids = []
    songs_artists = []
    with open("data/billboard_100.csv", encoding=  "utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader,None)
        for row in reader:
            songs_artists.append(row)

    for item in songs_artists:
        item[1] = item[1].replace("Featuring","")

    for song, artist in songs_artists:
        result = sp.search(song + " " + artist.replace("Featuring",""), limit = 1)   
        try:
            billboard_100_ids.append([result["tracks"]["items"][0]["id"]])
        except:
            continue
    headers = ["id"]

    with open("data/billboard_100_spotify.csv", 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(billboard_100_ids)

def retrieve_avatars():
    with open("data/user_info_1.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            urllib.request.urlretrieve(row[2], "images/user1_avatar.jpg")
        
    with open("data/user_info_2.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            urllib.request.urlretrieve(row[2], "images/user2_avatar.jpg")