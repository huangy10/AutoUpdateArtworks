from __future__ import unicode_literals

import os
from conf import GlobalConfig
import logging

# check the U-Disk and find target images


conf = GlobalConfig()
lgr = logging.getLogger(__name__)


class Artwork(object):

    def __int__(self, image_path):
        self.image_path = image_path
        image_name = os.path.basename(image_path)
        self.image_name = image_name
        artwork_full_name, ext = os.path.splitext(image_name)
        self.artwork_full_name = artwork_full_name
        self.ext = ext
        try:
            artwork_name, author, dynasty = artwork_full_name.split("_")
            self.is_valid = True
        except ValueError:
            self.is_valid = False
            artwork_name, author, dynasty = None, None, None
        self.artwork_name = artwork_name
        self.author = author
        self.dynasty = dynasty

        #
        self.dst_folder = None
        self.thumbnail_name = "%s_thumbnail.%s" % (artwork_full_name, ext)


def get_image_folder():
    return "{disk}:\\{folder}\\".format(
        disk=conf.u_disk_name, folder=conf.image_folder_name
    )


def load_images():
    """
    Load image list
    :return: list of image names(with file extension)
    """
    image_folder = get_image_folder()
    if not os.path.exists(image_folder):
        lgr.debug("Image folder not found.")
        return None

    images = filter(
        lambda im: im.split(".")[-1] in conf.image_formats,
        os.listdir(image_folder)
    )
    if len(images) > 0:
        lgr.debug("%s images are detected" % images.count())
    return images


def get_abs_dir(image_name):
    src_image_dir = get_image_folder()
    return os.path.join(src_image_dir, image_name)


def need_recreate_motion_xml(images):
    if not conf.history_valid:
        return True
    image_history = conf.get_history()

    if len(image_history) != len(images):
        return True

    for image in images:
        if image not in image_history:
            return True

    return False
