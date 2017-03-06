# coding=utf-8
from __future__ import unicode_literals

from image_loader import Artwork
from xml_io import *

def test():
    test_image = os.path.join(base_dir, "测试图片_卷_作者_朝代.jpg")
    artwork = Artwork(test_image)

    create_motion_xml([artwork])

if __name__ == '__main__':
    test()