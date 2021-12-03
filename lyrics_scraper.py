import csv
import requests
from bs4 import BeautifulSoup
from lyricsgenius import Genius
import re

songs_1 = []
ids_lyrics_1 = []
songs_2 = []
ids_lyrics_2 = []

# Insert token here
genius = Genius("")
with open("user_songs_1.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            songs_1.append([row[1],row[2]])
            ids_lyrics_1.append([row[0]])

with open("user_songs_2.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            songs_2.append([row[1],row[2]])
            ids_lyrics_2.append([row[0]])

lyrics_list_1 = []
lyrics_list_2 = []

for song in songs_1:
    try:
        res = genius.search_song(song[0], song[1])
        lyrics = res.lyrics
        
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        lyrics = lyrics.replace("EmbedShare URLCopyEmbedCopy","")
        lyrics = ''.join([i for i in lyrics if not i.isdigit()])
        lyrics_split = lyrics.split("\n")

        lyrics = " ".join([i for i in lyrics_split if i != ""])
        

        lyrics_list_1.append(lyrics)
    except:
        lyrics_list_1.append("")

for song in songs_2:
    try:
        res = genius.search_song(song[0], song[1])
        lyrics = res.lyrics
        
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        lyrics = lyrics.replace("EmbedShare URLCopyEmbedCopy","")
        lyrics = ''.join([i for i in lyrics if not i.isdigit()])
        lyrics_split = lyrics.split("\n")

        lyrics = " ".join([i for i in lyrics_split if i != ""])
        
        lyrics_list_2.append(lyrics)
    except:
        lyrics_list_2.append("")

for i,lyrics in enumerate(lyrics_list_1):
    ids_lyrics_1[i].append(lyrics)

for i,lyrics in enumerate(lyrics_list_2):
    ids_lyrics_2[i].append(lyrics)

lyrics_1_file = "data/lyrics_1.csv"
lyrics_2_file = "data/lyrics_2.csv"

headers = ["id","lyrics"]

with open(lyrics_1_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(ids_lyrics_1)
    
with open(lyrics_2_file, 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(ids_lyrics_2)
    
    

