# Spot1ny

![alt text](https://i.kinja-img.com/gawker-media/image/upload/c_fit,f_auto,g_center,pg_1,q_60,w_1165/msfgxy64htxbaki9up4e.png)

Spot1ny is a small project that compares the Spotify playlists of two users to see if their music tastes match. 

Libraries used:
* Spotipy
* Pandas
* Matplotlib
* Seaborn
* scikit-learn

## Working on:
* Data analysis and visualization
* Recommendation sysstem based on audio features and genres 

## Usage:
* Create an application on [Spotify Devloper Dashboard](https://developer.spotify.com/dashboard/login)
* Get Client ID, Client Secret and Redirect URI
* Replace those credentials in the blanks in the two Python files
* Run two crawlers to spawn two csv files:
```bash
python main.py
```

```bash
python userInfo.py
```
* Run the notebook in Jupyter Notebook or other kernels
