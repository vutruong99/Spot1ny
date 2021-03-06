# Spot1ny

Spot1ny (Spot one en why) is a part of my plan to build a system to match people based on their data. Spot1ny compares the Spotify playlists of two users to see if their music tastes match. Also, I am developing a recommender system based on genres, audio features and lyrics. 

![alt text](https://github.com/vutruong99/Spot1ny/blob/master/images/1.png)
![alt text](https://github.com/vutruong99/Spot1ny/blob/master/images/2.png)
![alt text](https://github.com/vutruong99/Spot1ny/blob/master/images/3.png)
![alt text](https://github.com/vutruong99/Spot1ny/blob/master/images/4.png)

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


## Working on
* Data analysis and visualization
* Recommendation sysstem based on audio features, genres, lyrics
* How to crawl lyrics effectively and correctly (for not so popular songs without lyrics)
* Summary of data using Pillow (Similar to Spotify Wrapped) - Color Palettes From Spotify Wrapped 2018

## Installation and usage
* Create an application on [Spotify Devloper Dashboard](https://developer.spotify.com/dashboard/login)
* Get Client ID, Client Secret and Redirect URI
* Replace those credentials in the blanks spotify_api.py
* Run the requirements.txt file with:
```bash
pip install -r requirements.txt
```
* Run the main Python file to spawn csv files and analyze the data:
```bash
python main.py
```
* Or run the notebook in Jupyter Notebook or other kernels to see step by step analysis
