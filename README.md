# Spot1ny

![alt text](https://i.kinja-img.com/gawker-media/image/upload/c_fit,f_auto,g_center,pg_1,q_60,w_1165/msfgxy64htxbaki9up4e.png)

Spot1ny is a part of my plan to build a system to match people based on their data. Spot1ny compares the Spotify playlists of two users to see if their music tastes match. Also, I am developing a recommender system based on genres, audio features and lyrics. 

Libraries used:
* Spotipy
* Pandas
* Matplotlib
* Seaborn
* scikit-learn
* BeautifulSoup
* LyricsGenius
* Plotly

## Working on:
* Data analysis and visualization
* Recommendation sysstem based on audio features, genres, lyrics
* How to crawl lyrics effectively and correctly (for not so popular songs without lyrics)

## Usage:
* Create an application on [Spotify Devloper Dashboard](https://developer.spotify.com/dashboard/login)
* Get Client ID, Client Secret and Redirect URI
* Replace those credentials in the blanks in the two Python files
* Run the crawlers to spawn csv files:
```bash
python scraper.py
```

```bash
python user_info_api.py
```

```bash
python lyrics_scraper.py
```

* Run the notebook in Jupyter Notebook or other kernels
