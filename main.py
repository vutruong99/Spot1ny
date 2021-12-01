import sys
from spotify_api import *
from billboard_100_scraper import *
from data_analysis import data_analysis

# def static_scrape(filepath):
#     with open(filepath, "r", encoding = "utf-8-sig", newline = "") as csvfile:
#         csvreader = csv.reader(csvfile)
#         cols = 0
#         rows = -1
#         for i,row in enumerate(csvreader):
#             cols = len(row)
#             if i < 6:
#                 print(row)
#             rows = rows + 1
            
#         print("\nThe dataset has " + str(rows) + " rows and " + str(cols) + " columns")

##################################################################
if __name__ == "__main__":
    if len(sys.argv) == 1:
        billboard_scraper("normal")
        billboard_to_spotify_id()
        spotify_playlists_scraper("normal")
        spotify_audio_features_scraper()
        spotify_user_info_scraper()
        data_analysis()
    # elif sys.argv[1] == "--scrape":
    #     billboard_scraper("partial")
    #     spotify_playlists_scraper("partial")
    #     spotify_audio_features_scraper()

    elif sys.argv[1] == "--static":
        data_analysis()
else:
    print("Please run this program from the command line")

