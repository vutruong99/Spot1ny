import pandas as pd
import matplotlib.pyplot as plt
from itertools import islice
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
import warnings
import csv

warnings.filterwarnings("ignore")

stats = []

def populate_dataframe(): 
    # Read data into dataframes

    # Songs df
    global songs_df_1, songs_df_2, user_info_df_1, user_info_df_2, user1, user2, audio_features_df_1, audio_features_df_2, billboard_100_df
    songs_df_1 = pd.read_csv("data/user_songs_1.csv", encoding= "utf-8-sig")
    songs_df_2 = pd.read_csv("data/user_songs_2.csv", encoding= "utf-8-sig")

    # Names df
    user_info_df_1 = pd.read_csv("data/user_info_1.csv", encoding= "utf-8-sig")
    user_info_df_2 = pd.read_csv("data/user_info_2.csv", encoding= "utf-8-sig")

    user1 = str(user_info_df_1["display_name"][0])
    user2 = str(user_info_df_2["display_name"][0]) 
    
    # Audio features df
    audio_features_df_1 = pd.read_csv("data/audio_features_1.csv", encoding= "utf-8-sig")
    audio_features_df_2 = pd.read_csv("data/audio_features_2.csv", encoding= "utf-8-sig")

    # Billboard's Hot 100 - Spotify version df
    billboard_100_df = pd.read_csv("data/billboard_100_spotify.csv")

def generateDictionary(dataframe, column):
    user_data = []
    if column not in dataframe:
        print("Column doesn't exist")
        return 0
    
    for row in dataframe[column]:
        if column == "genres":
            row_data = row.replace("[","").replace("]","").replace("'","").split(", ")
            for r in row_data:
                user_data.append(r)
        else:
            row_data = row
            if row_data:
                user_data.append(row_data)
  
    user_data = [i for i in user_data if i]

    user_dict = dict()

    for row in user_data:
        user_dict[row] = user_dict.get(row,0) + 1
    
    return user_dict

def plot(genres_dictionary, user_dataframe, feature):
    user_genres_dict = genres_dictionary
    username = user_dataframe["display_name"][0]
    
    def take(n, iterable):
        return dict(islice(iterable, n))

    sorted_user_genres =  {k: v for k, v in sorted(user_genres_dict.items(), 
                                                             reverse = True, key=lambda item: item[1])}
    top_10_user_genres = take(10, sorted_user_genres.items())

    p = sns.barplot(x = list(top_10_user_genres.values()), y = list(top_10_user_genres.keys()), orient = "h")
    p.set_xlabel("Count", fontsize = 15)
    p.set_title(username + "'s top " + feature, fontsize = 20)
    
    plt.savefig("visualizations/" + username + "'s top " + feature + ".png", bbox_inches='tight')
    plt.clf()

def featureAnalysis(first_user_dict, second_user_dict, feature):
    first_user_feature = first_user_dict
    second_user_feature = second_user_dict
    
    common_features = dict()
    for key in first_user_feature:
        if key in second_user_feature:
            common_features[key] = min(first_user_feature[key], second_user_feature[key])
    
    if common_features:
        sorted_common_features =  {k: v for k, v in sorted(common_features.items(), 
                                                             reverse = True, key=lambda item: item[1])}
        
        keys = []
        counts = []
        print("Most common " + feature + ":")
        for i,key in enumerate(sorted_common_features):
            if i == 5: break
            if feature == "songs":
                song = songs_df_1.loc[songs_df_1["id"]==key].values[0]
                print(song[1] + " by " + song[2] + " in " + song[3])
            else:
                print(key, sorted_common_features[key])
                keys.append(key)
                counts.append(sorted_common_features[key])
                p = sns.barplot(x = counts, y = keys, orient = "h")
                p.set_xlabel("Count", fontsize = 15)
                p.set_title("Common "  + feature, fontsize = 20)
                plt.savefig("visualizations/" + "Common "  + feature + ".png", bbox_inches='tight')
                plt.clf()
        print()
    else:
        print("No common " + feature)
        print()

def popularityAnalysis(first_dataframe, user_info_df_1, second_dataframe, user_info_df_2):
    print(user_info_df_1["display_name"][0] + "'s average songs' popularity is", first_dataframe["popularity"].mean())
    print(user_info_df_2["display_name"][0] + "'s average songs' popularity is", second_dataframe["popularity"].mean())
    print()
    max_first_pop = first_dataframe.sort_values(by=["popularity"]).iloc[-1]
    min_first_pop = first_dataframe.sort_values(by=["popularity"]).iloc[0]
    
    print(user_info_df_1["display_name"][0] + "'s most and least popular songs are")                                                
    print(max_first_pop["song"] + " by " + max_first_pop["artist"] + " with popularity " + str(max_first_pop["popularity"]))
    print(min_first_pop["song"] + " by " + min_first_pop["artist"] + " with popularity " + str(min_first_pop["popularity"]))
    print()

    max_second_pop = second_dataframe.sort_values(by=["popularity"]).iloc[-1]
    min_second_pop = second_dataframe.sort_values(by=["popularity"]).iloc[0]
    
    print(user_info_df_2["display_name"][0] + "'s most and least popular songs are")
    print(max_second_pop["song"] + " by " + max_second_pop["artist"] + " with popularity " + str(max_second_pop["popularity"]))
    print(min_second_pop["song"] + " by " + min_second_pop["artist"] + " with popularity " + str(min_second_pop["popularity"]))
    print()

    return [max_first_pop["song"], min_first_pop["song"], max_second_pop["song"], min_second_pop["song"]]
def similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, feature):
    if feature == "song":
        feature = "id"
    
    if feature == "genres":
        u1 = songs_df_1[feature].to_numpy()
        u2 = songs_df_2[feature].to_numpy()
        u1_set = set()
        u2_set = set()
        for item in u1:
            item = item.replace("[","").replace("]","").replace("'","").split(", ")
            for genre in item:
                u1_set.add(genre)
        for item in u2:
            item = item.replace("[","").replace("]","").replace("'","").split(", ")
            for genre in item:
                u2_set.add(genre)
                
        similarity = len(set(u1_set) & set(u2_set))/len(set(u1_set) | set(u2_set))*100
    
    else:
        u1 = songs_df_1[feature]
        u2 = songs_df_2[feature]
        u1.drop_duplicates(keep = "first", inplace = True)
        u2.drop_duplicates(keep = "first", inplace = True)
        similarity = len(pd.merge(u1, u2, how = "inner").index)/len(pd.merge(u1, u2, how = "outer").index)*100

    return similarity

def individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, feature):
    user1 = user_info_df_1["display_name"][0]
    user2 = user_info_df_2["display_name"][0]

    if feature == "song":
        feature = "id"
    
    if feature == "genres":
        u1 = songs_df_1[feature].to_numpy()
        u2 = songs_df_2[feature].to_numpy()
        u1_set = set()
        u2_set = set()
        for item in u1:
            item = item.replace("[","").replace("]","").replace("'","").split(", ")
            for genre in item:
                u1_set.add(genre)
        for item in u2:
            item = item.replace("[","").replace("]","").replace("'","").split(", ")
            for genre in item:
                u2_set.add(genre)
 
        per1 = (len(set(u1_set) & set(u2_set))/len(u2_set))*100
        per2 = (len(set(u1_set) & set(u2_set))/len(u1_set))*100

        print("Individual " + feature + " match")
        print(user1 + " matches " + str(per1) + " % with " + user2)
        print(user2 + " matches " + str(per2) + " % with " + user1)
    
    else:
        u1 = songs_df_1[feature]
        u2 = songs_df_2[feature]
        u1.drop_duplicates(keep = "first", inplace = True)
        u2.drop_duplicates(keep = "first", inplace = True)
        per1 = len(pd.merge(u1, u2, how = "inner").index)/len(u2) * 100
        per2 = len(pd.merge(u1, u2, how = "inner").index)/len(u1) * 100
        print("Individual " + feature + " match")
        print(user1 + " matches " + str(per1) + " % with " + user2)
        print(user2 + " matches " + str(per2) + " % with " + user1)
        print()

def kNearestNeighbours():
    X = audio_features_df_1.drop('id', axis = 1)
    X_np = X.to_numpy()

    X_2 = audio_features_df_2.drop("id", axis = 1)
    X_2_np = X_2.to_numpy()

    test_song_name = songs_df_2.iloc[0]["song"]
    
    knn = NearestNeighbors(n_neighbors=11)
    knn.fit(X_np)
    NearestNeighbors(algorithm='auto', n_neighbors=11, p=2,radius=1.0)
    res = knn.kneighbors([X_2_np[0]], return_distance=True)
    print("Vectors' distances and indexes")
    print(res)
    print()
    ids = []
    for r in res[1][0]:
        ids.append(audio_features_df_1.iloc[r]["id"])

    print("Recommendations for " + test_song_name + " are")
    for idz in ids:
        print(songs_df_1[songs_df_1['id'] == idz]["song"].to_string())

def billboard_comparision():
  
    u1 = songs_df_1["id"]
    u2 = songs_df_2["id"]

    u1.drop_duplicates(keep = "first", inplace = True)
    u2.drop_duplicates(keep = "first", inplace = True)

    print(user1 + " has " + str(len(pd.merge(u1,billboard_100_df["id"]))) + " song(s) that are in Billboard Hot 100")
    print(user2 + " has " + str(len(pd.merge(u2,billboard_100_df["id"]))) + " song(s) that are in Billboard Hot 100")
    print()

def data_analysis():
    populate_dataframe()
    statistics_2 = []
    statistics_1 = []

    # Drop duplicate records
    songs_df_1.drop_duplicates(subset = ["id"], keep = "first", inplace = True)
    songs_df_2.drop_duplicates(subset = ["id"], keep = "first", inplace = True)

    # Number of unique songs
    n_unique_songs_1 = len(songs_df_1["id"])
    print(user1 + " has " + str(n_unique_songs_1) + " songs")
    print(user1 + "'s first 10 songs")
    print(songs_df_1.head(10))
    print()

    n_unique_songs_2 = len(songs_df_2["id"])
    print(user2 + " has " + str(n_unique_songs_2) + " songs")
    print(user2 + "'s first 10 songs")
    print(songs_df_2.head(10))
    print()
    
    # Number of unique artists
    n_unique_artists_1 = len(songs_df_1["artist"].unique())
    print(user1 + " listens to " + str(n_unique_artists_1) + " artists and they are: ")
    print()
    print(songs_df_1["artist"].unique())
    print()

    n_unique_artists_2 = len(songs_df_2["artist"].unique())
    print(user2 + " listens to " + str(n_unique_artists_2) + " artists and they are: ")
    print()
    print(songs_df_2["artist"].unique())
    print()

    # Number of unique albums
    n_unique_albums_1 = len(songs_df_1["album"].unique())
    print(user1 + " listens to " + str(n_unique_albums_1) + " albums and they are: ")
    print()
    print(songs_df_1["album"].unique())
    print()

    n_unique_albums_2 = len(songs_df_2["album"].unique())
    print(user2 + " listens to " + str(n_unique_albums_2) + " albums and they are: ")
    print()
    print(songs_df_2["album"].unique())
    print()

    # Songs' durations
    # Miliseconds to minutes
    songs_df_1["duration"] = (songs_df_1["duration"] * 0.001 / 60).round(2)
    songs_df_2["duration"] = (songs_df_2["duration"] * 0.001 / 60).round(2)

    total_songs_durations_1 = songs_df_1["duration"].sum()
    total_songs_durations_2 = songs_df_2["duration"].sum()

    avg_songs_durations_1 = songs_df_1["duration"].mean().round(2)
    avg_songs_durations_2 = songs_df_2["duration"].mean().round(2)

    print(user1 + "'s average songs' duration is " + str(avg_songs_durations_1) + " minutes")
    print(user2 + "'s average songs' duration is " + str(avg_songs_durations_2) + " minutes")
    print()

    sns.set(rc = {'figure.figsize':(15,8)})
    users_durations = [user1 + "'s average songs duration", user2 + "'s averages song duration"]
    durations_mean = [songs_df_1["duration"].mean(), songs_df_2["duration"].mean()]
    p = sns.barplot(x= users_durations, y= durations_mean)
    p.set_ylabel("Minutes", fontsize = 15)
    p.set_title("Average songs' durations", fontsize = 20)
    plt.savefig('visualizations/avg_songs_durations.png', dpi=300, bbox_inches='tight')
    plt.clf()
    # plt.show()

    # Songs' popularity

    total_songs_popularity_1 = songs_df_1["popularity"].sum()
    total_songs_popularity_2 = songs_df_2["popularity"].sum()

    avg_songs_popularity_1 = songs_df_1["popularity"].mean().round(2)
    avg_songs_popularity_2 = songs_df_2["popularity"].mean().round(2)

    print(user1 + "'s average songs' popularity is " + str(avg_songs_popularity_1))
    print(user2 + "'s average songs' popularity is " + str(avg_songs_popularity_2))
    print()

    users_popularity = [user1 + "'s average songs popularity", user2 + "'s averages song popularity"]
    popularity = [songs_df_1["popularity"].mean(), songs_df_2["popularity"].mean()]
    p = sns.barplot(x= users_popularity, y= popularity)
    p.set_ylabel("Popularity rank", fontsize = 15)
    p.set_title("Average songs' popularity", fontsize = 20)
    plt.savefig('visualizations/avg_songs_popularity.png', dpi=300, bbox_inches='tight')
    plt.clf()
    # plt.show()

    popularityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2)

    # Unique genres
    u1 = songs_df_1["genres"].to_numpy()
    u2 = songs_df_2["genres"].to_numpy()
    u1_set = set()
    u2_set = set()
    for item in u1:
        item = item.replace("[","").replace("]","").replace("'","").split(", ")
        for genre in item:
            if genre != "":
                u1_set.add(genre)

    n_unique_genres_1 = len(u1_set)
    print(user1 + " listens to " + str(n_unique_genres_1) + " different genres and they are: ")
    print(u1_set)
    print()

    for item in u2:
        item = item.replace("[","").replace("]","").replace("'","").split(", ")
        for genre in item:
            if genre != "":
                u2_set.add(genre)
    
    n_unique_genres_2 = len(u2_set)
    print(user2 + " listens to " + str(n_unique_genres_2) + " different genres and they are: ")
    print(u2_set)
    print()
    
    billboard_comparision()

    # Genres dicts
    first_user_genres_dict = generateDictionary(songs_df_1, "genres")
    second_user_genres_dict = generateDictionary(songs_df_2, "genres")

    # Artists dicts
    first_user_artists_dict = generateDictionary(songs_df_1, "artist")
    second_user_artists_dict = generateDictionary(songs_df_2, "artist")

    # Songs dicts
    first_user_songs_dict = generateDictionary(songs_df_1, "id")
    second_user_songs_dict = generateDictionary(songs_df_2, "id")

    # Albums dicts
    first_user_albums_dict = generateDictionary(songs_df_1, "album")
    second_user_albums_dict = generateDictionary(songs_df_2, "album")

    plot(first_user_genres_dict, user_info_df_1, "genres")
    plot(second_user_genres_dict, user_info_df_2, "genres")

    plot(first_user_artists_dict, user_info_df_1, "artists")
    plot(second_user_artists_dict, user_info_df_2, "artists")

    plot(first_user_albums_dict, user_info_df_1, "album")
    plot(second_user_albums_dict, user_info_df_2, "album")

    featureAnalysis(first_user_songs_dict, second_user_songs_dict, "songs")
    featureAnalysis(first_user_genres_dict, second_user_genres_dict, "genres")
    featureAnalysis(first_user_artists_dict, second_user_artists_dict, "artists")
    featureAnalysis(first_user_albums_dict, second_user_albums_dict, "albums")

    print("Songs similarity",similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "song"),"%")
    print("Aritsts similarity", similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "artist"), "%")
    print("Albums similarity", similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "album"), "%")
    print("Popularity similarity", similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "popularity"), '%')
    print("Genres similiarity", similarityAnalysis(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "genres"), "%")
    print()

    individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "song")
    individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "artist")
    individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "album")
    individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "popularity")
    individual_similarity(songs_df_1, user_info_df_1, songs_df_2, user_info_df_2, "genres")
    print()

    kNearestNeighbours()

    statistics_1.append([user1, n_unique_songs_1, n_unique_artists_1, n_unique_albums_1, n_unique_genres_1, 
    total_songs_popularity_1, total_songs_durations_1, avg_songs_popularity_1, avg_songs_durations_1])

    statistics_2.append([user2, n_unique_songs_2, n_unique_artists_2, n_unique_albums_2, n_unique_genres_2, 
    total_songs_popularity_2, total_songs_durations_2, avg_songs_popularity_2, avg_songs_durations_2])
         
    headers = ["username","songs","artists","albums","genres","total_pop","total_dur","avg_dur","avg_pop"]
        # "avg_dur", "top_songs", "top_artists", "top_albums", "top_genres","most_pop_song", 
        # "least_pop_song", "longest_song","shortest_song"]

    result_file = "data/results.csv"

    with open(result_file, 'w', encoding="utf-8", newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(statistics_1)
        csvwriter.writerows(statistics_2)
        
