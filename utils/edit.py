from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt


def convert_bw(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pix = image.load()

    factor = 50
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = a + b + c
            if S > (((255 + factor) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))

    return ImageQt(image.convert('RGBA'))


def convert_gray(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pix = image.load()

    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))

    return ImageQt(image.convert('RGBA'))


def convert_negative(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pix = image.load()

    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))

    return ImageQt(image.convert('RGBA'))


def convert_sepia(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pix = image.load()

    depth = 30
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c)
            a = S + depth * 2
            b = S + depth
            c = S
            if a > 255:
                a = 255
            if b > 255:
                b = 255
            if c > 255:
                c = 255
            draw.point((i, j), (a, b, c))

    return ImageQt(image.convert('RGBA'))


def crop(image_path):
    image = Image.open(image_path)

    width, height = image.size
    if width >= 200:
        x1 = int(width / 2) - 100
        x2 = int(width / 2) + 100
    else:
        x1 = 0
        x2 = width

    if height >= 200:
        y1 = int(height / 2) - 100
        y2 = int(height / 2) + 100
    else:
        y1 = 0
        y2 = height

    image = image.crop((x1, y1, x2, y2))  # left, top, right, bottom
    return ImageQt(image.convert('RGBA'))


def scale(image_path, magnitude=1):
    image = Image.open(image_path)
    width, height = image.size
    image = image.resize((int(width * magnitude), int(height * magnitude)), Image.NEAREST)  # change size
    return ImageQt(image.convert('RGBA'))
