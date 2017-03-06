# coding=utf-8
from __future__ import unicode_literals
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps

base_dir = os.path.abspath(os.path.dirname(__file__))

template_file_path = os.path.join(base_dir, "templates", "thumbnail.png")

# layout data
template_size = (1243, 1702)
cover_radius = 1175
title_frame_offset = 92
title_offset = 108
author_offset = 233

font_path = os.path.join(base_dir, "font/default.TTF")
title_font = ImageFont.truetype(font_path, size=75)
author_font = ImageFont.truetype(font_path, size=60)
title_color = 0x704d2b
author_color = 0x8d6a42

def create_mask():
    # size = (cover_radius, cover_radius)
    # mask = Image.new("L", size, 0)
    # draw = ImageDraw.Draw(mask)
    # draw.ellipse((0, 0) + size, fill=255)
    mask = Image.open(os.path.join(base_dir, "templates", "mask.jpg"))
    return mask

mask = create_mask()


# calculate more directly useful locating parameters
cover_margin_left = 25
cover_margin_top = 4
title_margin_top = cover_radius + title_frame_offset + title_offset
author_margin_top = cover_radius + title_frame_offset + author_offset

def get_margin_left_with_width(width):
    return (template_size[0] - width) / 2


# This part is deprecated. Keep it as reference
# def convert_cover_from_square_to_round(im):
#     output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
#     output.putalpha(mask)
#     return output.convert("RGBA")


def insert_cover_to_template(cover_im, template_im):
    # convert the cover from square to round, as the function name says.
    cover_im = ImageOps.fit(cover_im, mask.size, centering=(0.5, 0.5))
    # put cover on the template
    cover_offset = (cover_margin_left, cover_margin_top)

    template_im.paste(cover_im, cover_offset, mask)

    return template_im


def add_text_to_template(title, author, dynasty, template_im):
    draw = ImageDraw.Draw(template_im)
    title_size = draw.textsize(title, title_font)
    title_width = title_size[0]

    title_margin_left = get_margin_left_with_width(title_width)
    draw.text((title_margin_left, title_margin_top), title, title_color, font=title_font)

    author_text = "%s · %s" % (author, dynasty)
    author_size = draw.textsize(author_text, author_font)
    author_width = author_size[0]

    author_margin_left = get_margin_left_with_width(author_width)
    draw.text((author_margin_left, author_margin_top), author_text, author_color, font=author_font)


def build_thumbnail(artwork):
    cover_path = artwork.get_cover_path()

    # read images into memory
    cover_im = Image.open(cover_path)
    template_im = Image.open(template_file_path)

    # insert the cover to the template
    template_im = insert_cover_to_template(cover_im, template_im)

    # add text
    add_text_to_template(artwork.artwork_name, artwork.author, artwork.dynasty, template_im)

    # save the output
    template_im.save(artwork.get_thumbnail_path())