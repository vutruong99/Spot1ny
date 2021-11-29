from bs4 import BeautifulSoup
import requests
import csv
import sys
from requests.api import head
import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog = True, client_id="",
                                                    client_secret="",
                                                    redirect_uri="",
                                                    scope="user-library-read"))
def billboard_scraper(mode):
    print("Scraping Billboard's The Hot 100\n")
    songs = []
    artists = []
    content = requests.get('https://www.billboard.com/charts/hot-100/')
    soup = BeautifulSoup(content.content, 'html.parser')

    top_song = soup.find_all('h3', {"class" : "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"})
    top_artist = soup.find_all('span', {"class" : "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet"})
    next_songs = soup.find_all("h3", {"class" : "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"})
    next_artists = soup.find_all("span", {"class" : "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"})
    
    for ts in top_song:
        songs.append(ts.get_text().strip())
    for ta in top_artist:
        artists.append(ta.get_text().strip())
    for song in next_songs:
        songs.append(song.get_text().strip())
    for artist in next_artists:
        artists.append(artist.get_text().strip())

    headers = ["song","artists"]

    results = list(zip(songs,artists))

    if mode == "partial":
        results = results[:5]

    print(headers)
    for i,res in enumerate(results):
        if i == 5:
            break
        print(res)

    print("\nThe Hot 100 - Billboard dataset has " + str(len(results)) + " rows and 2 columns\n")

    billboard_100 = "billboard_100.csv"

    with open(billboard_100, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(results)

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
    
    first_user_id = "lwqh6n22yf8j1esekvl1dghpj"
    second_user_id = "hc7cn89l7knx2wknggi5g6c8j"

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
    first_user_file = "user_songs_1.csv"
    second_user_file = "user_songs_2.csv"
            
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

    with open("user_songs_1.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            ids1.append(row[0])

    with open("user_songs_2.csv", encoding="utf-8-sig") as f:
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
    print("\nThe second audio features dataset has " + str(len(audio_features_2)) + " rows and 12 columns")

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

def static_scrape(filepath):
    with open(filepath, "r", encoding = "utf-8-sig", newline = "") as csvfile:
        csvreader = csv.reader(csvfile)
        cols = 0
        rows = -1
        for i,row in enumerate(csvreader):
            cols = len(row)
            if i < 6:
                print(row)
            rows = rows + 1
            
        print("\nThe dataset has " + str(rows) + " rows and " + str(cols) + " columns")

# Main driver
if __name__ == "__main__":
    if len(sys.argv) == 1:
        billboard_scraper("normal")
        spotify_playlists_scraper("normal")
        spotify_audio_features_scraper()

    elif sys.argv[1] == "--scrape":
        billboard_scraper("partial")
        spotify_playlists_scraper("partial")
        spotify_audio_features_scraper()

    elif sys.argv[1] == "--static":
        if len(sys.argv) == 3:
            static_scrape(sys.argv[2])
        else:
            print("Please provide a path for this mode")
else:
    print("Please run this program from the command line")

