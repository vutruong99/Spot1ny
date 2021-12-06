from PIL import Image, ImageFont, ImageDraw, ImageOps
import csv

result_file = "data/results.csv"
common_file = "data/commons.csv"

stats = []
common_songs = []
common_artists = []
common_albums = []
common_genres = []


def setup():
    global com_per_songs, com_per_artists, com_per_genres, com_per_albums
    
    with open(result_file, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            stats.append(row)

    with open(common_file, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader, None)
        for i, row in enumerate(reader):
            common_songs.append(row[0])
            common_artists.append(row[1])
            common_albums.append(row[2])
            common_genres.append(row[3])

            if i == 0:
                com_per_songs = row[4]
                com_per_artists = row[5]
                com_per_albums = row[6]
                com_per_genres= row[7]

        global frame_width, user1, n_songs_1, n_artists_1, n_albums_1, n_genres_1, total_pop_1, total_dur_1
        global avg_pop_1, avg_dur_1, user2, n_songs_2, n_artists_2, n_albums_2, n_genres_2, total_pop_2
        global total_dur_2, avg_pop_2, avg_dur_2
        global u1a, u2a

        u1a = Image.open('images/user1_avatar.jpg')
        u2a = Image.open('images/user2_avatar.jpg')

        frame_width = 1500
        user1 = stats[0][0]
        n_songs_1 = stats[0][1]
        n_artists_1 = stats[0][2]
        n_albums_1 = stats[0][3]
        n_genres_1 = stats[0][4]
        total_pop_1 = stats[0][5]
        total_dur_1 = stats[0][6]
        avg_pop_1 = stats[0][7]
        avg_dur_1 = stats[0][8]

        user2 = stats[1][0]
        n_songs_2 = stats[1][1]
        n_artists_2 = stats[1][2]
        n_albums_2 = stats[1][3]
        n_genres_2 = stats[1][4]
        total_pop_2 = stats[1][5]
        total_dur_2 = stats[1][6]
        avg_pop_2 = stats[1][7]
        avg_dur_2 = stats[1][8]

        basic_stats()
        ind_stats(0)
        ind_stats(1)
        common_stats()

        

bg_color_list = ["4800FF", "FF6436","513750","01644F","1E1A19","F971A1","9FC3D3","CB7E52","B49AC9","FF281B"]
text_color_list = ["BA9CD4","FFCDD2","F49B21","99C4D7","60F448","BCF5CE","FFFEFD","523555","FFCDCB","250E08"]
stats_color_list = ["7EF3E1", "E81F31","ED2033","000000","F535AB","162F62","5D4563","FBFDFF","523755","FFC44E"]

bg_color = "#23262C"
text_color = "#b2daab"
stats_color = "#699CA4"

# title_color = "#3AA185"

stats_font = 64
text_font = 56
title_font = 80
huge_font = 150

def add_text_stats_page(image, text, align, height, size, colour, type, frame_width):
    font = ImageFont.truetype("fonts/SVN-GothamBold.ttf", size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font = font)

    if w > 550 and type == "line":
        while w > 550 :
            text = text[:-1]
            w, h = draw.textsize(text, font = font)
        text = text + "..."

    if w > 550 and type == "genre":
        text = text[:text.find(" ")] + "\n" + text[text.find(" ")+1:]
        w, h = draw.textsize(text, font = font)
        while w > 550 :
            size = size-1
            font = ImageFont.truetype("fonts/SVN-GothamBold.ttf", size)
            w, h = draw.textsize(text, font = font)
    
    left_width = frame_width - frame_width//2
    right_width = frame_width + frame_width//2

    if align == "left":
        draw.text(((300 - w), height), text, font = font, fill = colour)
    elif align == "center":
        draw.text(((frame_width - w)/2, height), text, font = font, fill = colour)
    elif align == "right":
        draw.text(((900), height), text, font = font, fill = colour)
    elif align == "right-center":
        draw.text(((right_width-w)/2, height), text, font = font, fill = colour)
    elif align == "left-center":
        draw.text(((left_width-w)/2, height), text, font = font, fill = colour)
    elif align == "left-l":
        draw.text((100, height), text, font = font, fill = colour)
    elif align == "left-r":
        draw.text((850, height), text, font = font, fill = colour)
    elif align == "right-l":
        draw.text((left_width - w, height), text, font = font, fill = colour)
    elif align == "right-r":
        draw.text((frame_width - w, height), text, font = font, fill = colour)

def add_percentage(image, left_text, text , height, size, colour, side, frame_width):
    font = ImageFont.truetype("fonts/SVN-GothamBold.ttf", size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(left_text, font = font)
    ws,hs = draw.textsize(" ", font = font)

    if side == "left":
        draw.text((w + 100 + ws, height), text, font = font, fill = colour)
    else:
        draw.text(((frame_width)//2 + w + 100 + ws, height), text, font = font, fill = colour)

def draw_top_line(image, text, size, side, frame_width):
    font = ImageFont.truetype("fonts/SVN-GothamBold.ttf", size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font = font)
    if side == "left":
        draw.line((0,105 , (frame_width-w)//2 - 20,105), fill=text_color, width=15)
    else:
        draw.line(((frame_width-w)//2 + w + 20 ,105 , frame_width ,105), fill=text_color, width=15)

def basic_stats():
    global u1a, u2a
    im = Image.new("RGB", (1200, 1200), bg_color)

    size = (300, 300)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.rectangle((0, 0) + size, fill=255)

    draw_top_line(im, "Spot1ny", text_font, "left", 1200)
    draw_top_line(im, "Spot1ny", text_font, "right", 1200)

    u1a_cropped = ImageOps.fit(u1a, mask.size, centering=(0.5, 0.5))
    u1a_cropped.putalpha(mask)

    u2a_cropped = ImageOps.fit(u2a, mask.size, centering=(0.5, 0.5))
    u2a_cropped.putalpha(mask)

    im.paste(u1a_cropped, ((600-300)//2,200), u2a_cropped)
    im.paste(u2a_cropped, ((1800-300)//2,200), u1a_cropped)

    add_text_stats_page(im, "Spot1ny", "center", 80 , text_font, text_color, "nor", 1200)

    add_text_stats_page(im, user1, "left-center", 520 , text_font, stats_color, "nor", 1200)
    add_text_stats_page(im, user2, "right-center", 520 , text_font, stats_color, "nor", 1200)

    add_text_stats_page(im, "songs", "center", 635 , stats_font, text_color, "nor", 1200)
    add_text_stats_page(im, "artists", "center", 697 , stats_font, text_color, "nor", 1200)
    add_text_stats_page(im, "albums", "center", 759 , stats_font, text_color, "nor", 1200)
    add_text_stats_page(im, "genres", "center", 821 , stats_font, text_color, "nor", 1200)
    add_text_stats_page(im, "avg pop", "center", 883 , stats_font, text_color, "nor", 1200)
    add_text_stats_page(im, "avg time", "center", 945 , stats_font, text_color, "nor", 1200)

    add_text_stats_page(im, n_songs_1, "left", 635 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_artists_1, "left", 697 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_albums_1, "left", 759 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_genres_1, "left", 821 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, avg_pop_1, "left", 883 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, avg_dur_1 + "'", "left", 945 , stats_font, stats_color, "nor", 1200)

    add_text_stats_page(im, n_songs_2, "right", 635 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_artists_2, "right", 697 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_albums_2, "right", 759 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, n_genres_2, "right", 821 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, avg_pop_2, "right", 883 , stats_font, stats_color, "nor", 1200)
    add_text_stats_page(im, avg_dur_2 + "'", "right", 945 , stats_font, stats_color, "nor", 1200)

    add_text_stats_page(im, "github.com/vutruong99", "center", 1080 , text_font, text_color, "nor", 1200)

    im.save("images/basic_statistics.png")

def csv_to_list(item):
    res = []
    item = item.replace("[","").replace("]","").replace("'","").split(", ")
    for genre in item:
        res.append(genre)
       
    return res

def ind_stats(user):
    global u1a, u2a
    username = stats[user][0]
    top_artists = csv_to_list(stats[user][9])
    top_albums = csv_to_list(stats[user][10])
    top_genres = csv_to_list(stats[user][11])
    top_pop = stats[user][12]

    im = Image.new("RGB", (frame_width, 1815), bg_color)

    size = (512, 512)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.rectangle((0, 0) + size, fill=255)

    draw_top_line(im, "Spot1ny", text_font, "left", 1500)
    draw_top_line(im, "Spot1ny", text_font, "right", 1500)
    
    if user == 0:
        ua = u1a
    else:
        ua = u2a

    ua_cropped = ImageOps.fit(ua, mask.size, centering=(0.5, 0.5))
    ua_cropped.putalpha(mask)

    im.paste(ua_cropped, ((frame_width - 500)//2,200), ua_cropped)

    add_text_stats_page(im, "Spot1ny", "center", 80 , text_font, text_color, "nor", 1500)

    add_text_stats_page(im, username, "center", 750 , title_font, stats_color, "nor", 1500)
    
    add_text_stats_page(im, "top artists", "left-l", 860 , text_font, text_color, "nor", 1500)
    y_pos_1 = 960

    for artist in top_artists:
        add_text_stats_page(im, artist, "left-l", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    add_text_stats_page(im, "top albums", "left-r", 860 , text_font, text_color, "nor", 1500)

    y_pos_1 = 960
    for album in top_albums:
        add_text_stats_page(im, album, "left-r", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    add_text_stats_page(im, "top genre", "left-l", 1360 , text_font, text_color, "nor", 1500)

    y_pos_1 = 1460
    add_text_stats_page(im, top_genres[0].upper(), "left-l", y_pos_1 , title_font, stats_color, "genre", 1500)


    add_text_stats_page(im, "most popular track", "left-r", 1360 , text_font, text_color, "nor", 1500)

    y_pos_1 = 1460
    add_text_stats_page(im, top_pop, "left-r", y_pos_1 , title_font, stats_color, "genre", 1500)

    
    add_text_stats_page(im, "github.com/vutruong99", "center", 1680 , text_font, text_color, "nor", 1500)

    im.save("images/" + username + "_statistics.png")

def common_stats():
    global u1a, u2a
    im = Image.new("RGB", (frame_width, 1900), bg_color)

    size = (400, 400)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.rectangle((0, 0) + size, fill=255)

    draw_top_line(im, "Spot1ny", text_font, "left", 1500)
    draw_top_line(im, "Spot1ny", text_font, "right", 1500)
    
    u1a_cropped = ImageOps.fit(u1a, mask.size, centering=(0.5, 0.5))
    u1a_cropped.putalpha(mask)

    u2a_cropped = ImageOps.fit(u2a, mask.size, centering=(0.5, 0.5))
    u2a_cropped.putalpha(mask)

    im.paste(u1a_cropped, ((750-400)//2,200), u2a_cropped)
    im.paste(u2a_cropped, ((2250-400)//2,200), u1a_cropped)

    add_text_stats_page(im, "Spot1ny", "center", 80 , text_font, text_color, "nor", 1500)

    add_text_stats_page(im, user1, "left-center", 650 , title_font, stats_color, "nor", 1500)

    add_text_stats_page(im, user2, "right-center", 650 , title_font, stats_color, "nor", 1500)
    
    add_text_stats_page(im, "shared songs", "left-l", 760 , text_font, text_color, "nor", 1500)
    add_percentage(im, "shared songs", com_per_songs + "%" , 760, text_font, stats_color, "left", 1500)
    
    y_pos_1 = 860

    for song in common_songs:
        add_text_stats_page(im, song, "left-l", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    add_text_stats_page(im, "shared artists", "left-r", 760 , text_font, text_color, "nor", 1500)
    add_percentage(im, "shared artists", com_per_artists + "%" , 760, text_font, stats_color, "right", 1500)
    
    y_pos_1 = 860
    for artist in common_artists:
        add_text_stats_page(im, artist, "left-r", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    add_text_stats_page(im, "shared albums", "left-l", 1260 , text_font, text_color, "nor", 1500)
    add_percentage(im, "shared albums", com_per_albums + "%" , 1260, text_font, stats_color, "left", 1500)

    y_pos_1 = 1360
    for album in common_albums:
        add_text_stats_page(im, album, "left-l", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    add_text_stats_page(im, "shared genres", "left-r", 1260 , text_font, text_color, "nor", 1500)
    add_percentage(im, "shared genres", com_per_genres + "%" , 1260, text_font, stats_color, "right", 1500)

    y_pos_1 = 1360
    for genre in common_genres:
        add_text_stats_page(im, genre, "left-r", y_pos_1 , stats_font, stats_color, "line", 1500)
        y_pos_1 += 67

    
    add_text_stats_page(im, "github.com/vutruong99", "center", 1780 , text_font, text_color, "nor", 1500)

    im.save("images/common_statistics.png")

