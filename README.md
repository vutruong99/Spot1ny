# Spot1ny

![alt text](https://github.com/vutruong99/Spot1ny/blob/master/images/result.png?raw=true)

Spot1ny (Spot one en why) is a part of my plan to build a system to match people based on their data. Spot1ny compares the Spotify playlists of two users to see if their music tastes match. Also, I am developing a recommender system based on genres, audio features and lyrics. 

Libraries used:
* Spotipy
* Pandas
* Matplotlib
* Seaborn
* scikit-learn
* BeautifulSoup
* LyricsGenius
* Plotly
* Pillow


## Working on:
* Data analysis and visualization
* Recommendation sysstem based on audio features, genres, lyrics
* How to crawl lyrics effectively and correctly (for not so popular songs without lyrics)
* Summary of data using Pillow (Similar to Spotify Wrapped)

## Usage:
* Create an application on [Spotify Devloper Dashboard](https://developer.spotify.com/dashboard/login)
* Get Client ID, Client Secret and Redirect URI
* Replace those credentials in the blanks in the two Python files
* Run the crawlers to spawn csv files and analyze the data:

```bash
python main.py
```

* Or run the notebook in Jupyter Notebook or other kernels to see step by step analysis
