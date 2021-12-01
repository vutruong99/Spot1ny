from PIL import Image, ImageFont, ImageDraw, ImageOps
from spotify_api import retrieve_avatars


def add_text(image, text, align, height, size, colour):
    font = ImageFont.truetype("fonts/CircularStd-Bold.otf", size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font = font)
    if align == "left":
        W = 600
    elif align == "center":
        W = 1200
    elif align == "right":
        W = 1800     
    draw.text(((W - w)/2, height), text, font = font, fill = colour)

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

im = Image.new("RGB", (1200, 2400), "#2B2D42")


size = (256, 256)
mask = Image.new('L', size, 0)
draw = ImageDraw.Draw(mask) 
draw.ellipse((0, 0) + size, fill=255)

u1a_cropped = ImageOps.fit(u1a, mask.size, centering=(0.5, 0.5))
u1a_cropped.putalpha(mask)

u2a_cropped = ImageOps.fit(u2a, mask.size, centering=(0.5, 0.5))
u2a_cropped.putalpha(mask)

im.paste(u1a_cropped, ((600-256)//2,200), u2a_cropped)
im.paste(u2a_cropped, ((1800-256)//2,200), u1a_cropped)

add_text(im, "Spot1ny", "center", 100 , 80, "#F7EC59")

add_text(im, "Statistics", "center", 500 , 56, "#FF66D8")

add_text(im, "Songs", "center", 600 , 56, "#F8F7F9")
add_text(im, "Artists", "center", 700 , 56, "#F8F7F9")
add_text(im, "Albums", "center", 800 , 56, "#F8F7F9")
add_text(im, "Genres", "center", 900 , 56, "#F8F7F9")
add_text(im, "Popularity", "center", 1000 , 56, "#F8F7F9")
add_text(im, "Duration", "center", 1100 , 56, "#F8F7F9")

add_text(im, "142", "left", 600 , 56, "#92DCE5")
add_text(im, "44", "left", 700 , 56, "#92DCE5")
add_text(im, "80", "left", 800 , 56, "#92DCE5")
add_text(im, "313", "left", 900 , 56, "#92DCE5")
add_text(im, "56", "left", 1000 , 56, "#92DCE5")
add_text(im, "4'", "left", 1100 , 56, "#92DCE5")

add_text(im, "543", "right", 600 , 56, "#92DCE5")
add_text(im, "138", "right", 700 , 56, "#92DCE5")
add_text(im, "99", "right", 800 , 56, "#92DCE5")
add_text(im, "544", "right", 900 , 56, "#92DCE5")
add_text(im, "80", "right", 1000 , 56, "#92DCE5")
add_text(im, "3.8'", "right", 1100 , 56, "#92DCE5")

#####################################################################
add_text(im, "Commonality", "center", 1300 , 56, "#FF66D8")

add_text(im, "Songs", "center", 1400 , 56, "#F8F7F9")
add_text(im, "Artists", "center", 1500 , 56, "#F8F7F9")
add_text(im, "Albums", "center", 1600 , 56, "#F8F7F9")
add_text(im, "Genres", "center", 1700 , 56, "#F8F7F9")
add_text(im, "Popularity", "center", 1800 , 56, "#F8F7F9")
add_text(im, "Duration", "center", 1900 , 56, "#F8F7F9")

add_text(im, "142", "left", 1400 , 56, "#92DCE5")
add_text(im, "44", "left", 1500 , 56, "#92DCE5")
add_text(im, "80", "left", 1600 , 56, "#92DCE5")
add_text(im, "313", "left", 1700 , 56, "#92DCE5")
add_text(im, "56", "left", 1800 , 56, "#92DCE5")
add_text(im, "4'", "left", 1900 , 56, "#92DCE5")

add_text(im, "543", "right", 1400 , 56, "#92DCE5")
add_text(im, "138", "right", 1500 , 56, "#92DCE5")
add_text(im, "99", "right", 1600 , 56, "#92DCE5")
add_text(im, "544", "right", 1700 , 56, "#92DCE5")
add_text(im, "80", "right", 1800 , 56, "#92DCE5")
add_text(im, "3.8'", "right", 1900 , 56, "#92DCE5")

# add_text(im, "github.com/vutruong99", "center", 1250 , 80, "#F7EC59")
# back_im = im.copy()

# back_im.paste(u1a, (0, 0), create_mask(u1a))
# back_im.save('images/result_1.png', quality=95)


im.save("images/result.png")
# background = generate_gradient("#42275a", "#734b6d", 400, 600)
