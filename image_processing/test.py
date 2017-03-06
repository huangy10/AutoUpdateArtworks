# coding=utf-8
from __future__ import unicode_literals

from image_loader import Artwork
from processor import *

def test():
    test_image = os.path.join(base_dir, "步辇图_卷_作家_宋.jpg")
    artwork = Artwork(test_image)

    build_thumbnail(artwork)