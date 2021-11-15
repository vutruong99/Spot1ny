import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth
import pprint

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="",
                                               scope="user-library-read"))

first_user_id = input("Enter the user id for the first user ")
second_user_id = input("Enter the user id for the second user ")

first_user = sp.user(first_user_id)
first_user_data = []
first_user_data.append([first_user["id"], first_user["display_name"], first_user["images"][0]["url"]])

second_user = sp.user(second_user_id)
second_user_data = []
second_user_data.append([second_user["id"], second_user["display_name"], second_user["images"][0]["url"]])

headers = ["id","display_name","image_url"]
first_user_info = "first_user_info.csv"
second_user_info = "second_user_info.csv"

with open(first_user_info, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(first_user_data)

with open(second_user_info, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(second_user_data)