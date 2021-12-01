from bs4 import BeautifulSoup
import requests
import csv

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

    billboard_100 = "data/billboard_100.csv"

    with open(billboard_100, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(results)
    
