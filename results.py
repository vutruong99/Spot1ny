from os import stat
from PIL import Image, ImageFont, ImageDraw, ImageOps
import csv

result_file = "data/results.csv"

stats = []
with open(result_file, encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        stats.append(row)

print(stats)
        
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

bg_color_list = ["#4800FF", "#FF6436","#513750","#01644F","#1E1A19","#F971A1","9FC3D3","CB7E52","B49AC9","FF281B"]
text_color_list = ["#BA9CD4","#FFCDD2","#F49B21","#99C4D7","#60F448","#BCF5CE","FFFEFD","523555","FFCDCB","250E08"]
stats_color_list = ["#7EF3E1", "#E81F31","#ED2033","#000000","#F535AB","#162F62","5D4563","FBFDFF","523755","FFC44E"]

bg_color = "#FF281B"
text_color = "#250E08"
stats_color = "#FFC44E"

title_color = "#3AA185"

stats_font = 64
text_font = 56

def add_text_stats_page(image, text, align, height, size, colour):
    font = ImageFont.truetype("fonts/GothamBold.ttf", size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font = font)
    if align == "left":
        draw.text(((300 - w), height), text, font = font, fill = colour)
    elif align == "center":
        draw.text(((1200 - w)/2, height), text, font = font, fill = colour)
    elif align == "right":
        draw.text(((900), height), text, font = font, fill = colour)
    elif align == "right-center":
        draw.text(((1800-w)/2, height), text, font = font, fill = colour)
    elif align == "left-center":
        draw.text(((600-w)/2, height), text, font = font, fill = colour)
        
# def generate_gradient(
#         colour1: str, colour2: str, width: int, height: int) -> Image:
#     """Generate a vertical gradient."""
#     base = Image.new('RGB', (width, height), colour1)
#     top = Image.new('RGB', (width, height), colour2)
#     mask = Image.new('L', (width, height))
#     mask_data = []
#     for y in range(height):
#         mask_data.extend([int(255 * (y / height))] * width)
#     mask.putdata(mask_data)
#     base.paste(top, (0, 0), mask)
#     return base


# def create_mask(img):
#     mask_im = Image.new("L", img.size, 0)
#     draw = ImageDraw.Draw(mask_im)
#     draw.ellipse((0,0) + img.size, fill=255)
#     mask_im.save('images/mask_circle.jpg', quality=95)

#     return mask_im


u1a = Image.open('images/user1_avatar.jpg')
u2a = Image.open('images/user2_avatar.jpg')

im = Image.new("RGB", (1200, 1200), bg_color)

size = (300, 300)
mask = Image.new('L', size, 0)
draw = ImageDraw.Draw(mask) 
draw.rectangle((0, 0) + size, fill=255)

u1a_cropped = ImageOps.fit(u1a, mask.size, centering=(0.5, 0.5))
u1a_cropped.putalpha(mask)

u2a_cropped = ImageOps.fit(u2a, mask.size, centering=(0.5, 0.5))
u2a_cropped.putalpha(mask)

im.paste(u1a_cropped, ((600-300)//2,200), u2a_cropped)
im.paste(u2a_cropped, ((1800-300)//2,200), u1a_cropped)

add_text_stats_page(im, "Spot1ny", "center", 80 , text_font, text_color)

add_text_stats_page(im, "Thomas", "left-center", 520 , text_font, text_color)
add_text_stats_page(im, "SunCat", "right-center", 520 , text_font, text_color)

add_text_stats_page(im, "songs", "center", 635 , stats_font, stats_color)
add_text_stats_page(im, "artists", "center", 697 , stats_font, stats_color)
add_text_stats_page(im, "albums", "center", 759 , stats_font, stats_color)
add_text_stats_page(im, "genres", "center", 821 , stats_font, stats_color)
add_text_stats_page(im, "avg pop", "center", 883 , stats_font, stats_color)
add_text_stats_page(im, "avg time", "center", 945 , stats_font, stats_color)

add_text_stats_page(im, n_songs_1, "left", 635 , stats_font, stats_color)
add_text_stats_page(im, n_artists_1, "left", 697 , stats_font, stats_color)
add_text_stats_page(im, n_albums_1, "left", 759 , stats_font, stats_color)
add_text_stats_page(im, n_genres_1, "left", 821 , stats_font, stats_color)
add_text_stats_page(im, avg_pop_1, "left", 883 , stats_font, stats_color)
add_text_stats_page(im, avg_dur_1 + "'", "left", 945 , stats_font, stats_color)

add_text_stats_page(im, n_songs_2, "right", 635 , stats_font, stats_color)
add_text_stats_page(im, n_artists_2, "right", 697 , stats_font, stats_color)
add_text_stats_page(im, n_albums_2, "right", 759 , stats_font, stats_color)
add_text_stats_page(im, n_genres_2, "right", 821 , stats_font, stats_color)
add_text_stats_page(im, avg_pop_2, "right", 883 , stats_font, stats_color)
add_text_stats_page(im, avg_dur_2 + "'", "right", 945 , stats_font, stats_color)

add_text_stats_page(im, "github.com/vutruong99", "center", 1080 , text_font, text_color)

#####################################################################
# add_text_stats_page(im, "Commonality", "center", 1300 , 56, "#FF66D8")

# add_text_stats_page(im, "Songs", "center", 1400 , 56, "#F8F7F9")
# add_text_stats_page(im, "Artists", "center", 1500 , 56, "#F8F7F9")
# add_text_stats_page(im, "Albums", "center", 1600 , 56, "#F8F7F9")
# add_text_stats_page(im, "Genres", "center", 1700 , 56, "#F8F7F9")
# add_text_stats_page(im, "Popularity", "center", 1800 , 56, "#F8F7F9")
# add_text_stats_page(im, "Duration", "center", 1900 , 56, "#F8F7F9")

# add_text_stats_page(im, "142", "left", 1400 , 56, "#92DCE5")
# add_text_stats_page(im, "44", "left", 1500 , 56, "#92DCE5")
# add_text_stats_page(im, "80", "left", 1600 , 56, "#92DCE5")
# add_text_stats_page(im, "313", "left", 1700 , 56, "#92DCE5")
# add_text_stats_page(im, "56", "left", 1800 , 56, "#92DCE5")
# add_text_stats_page(im, "4'", "left", 1900 , 56, "#92DCE5")

# add_text_stats_page(im, "543", "right", 1400 , 56, "#92DCE5")
# add_text_stats_page(im, "138", "right", 1500 , 56, "#92DCE5")
# add_text_stats_page(im, "99", "right", 1600 , 56, "#92DCE5")
# add_text_stats_page(im, "544", "right", 1700 , 56, "#92DCE5")
# add_text_stats_page(im, "80", "right", 1800 , 56, "#92DCE5")
# add_text_stats_page(im, "3.8'", "right", 1900 , 56, "#92DCE5")

# back_im = im.copy()

# back_im.paste(u1a, (0, 0), create_mask(u1a))
# back_im.save('images/result_1.png', quality=95)

im.save("images/result.png")
# background = generate_gradient("#42275a", "#734b6d", 400, 600)
