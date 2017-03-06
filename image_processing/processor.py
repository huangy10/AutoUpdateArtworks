from __future__ import unicode_literals

from PIL import Image, ImageFont, ImageDraw


font_title = ImageFont.truetype("font/default.TTF", size=32)
font_author = ImageFont.truetype("font/default.TTF", size=16)


def build_thumbnail(image_path):
    with Image.open(image_path) as im:
        thumbnail = Image.new('RGBA', (800, 600))

