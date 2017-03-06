# 1. Detect the insertion of external drive and find if image inputs exits
# 2. Build the motion.xml config file
# 3. Copy the images and configuration file into the corresponding directory
from __future__ import unicode_literals

from conf import GlobalConfig, ConfigEnvironment
from image_loader import load_images, need_recreate_motion_xml, get_abs_dir
from image_op import backup_images, prepare_daily_image_folder, get_daily_image_dir

import os
import sys
import logging
import shutil


lgr = logging.getLogger(__name__)
conf = GlobalConfig()


def prepare_image_directories(program_root):
    if backup_images(program_root):
        lgr.debug("Backup success")
    success = prepare_daily_image_folder(program_root)
    if success:
        return get_daily_image_dir(program_root)
    else:
        return None


def run(program_root):
    with ConfigEnvironment(conf):
        images = load_images()
        if images is None or len(images) == 0:
            return
        if not need_recreate_motion_xml(images):
            lgr.debug("No update is found.")
            return
        else:
            daily_image_dir = \
                prepare_daily_image_folder(program_root)
            # copy images into this dir
            lgr.debug("Copying images into destination folder")
            for image in images:
                src_abs_path = get_abs_dir(image)
                dst_abs_path = os.path.join(daily_image_dir, image)
                shutil.copy(src_abs_path, dst_abs_path)

            lgr.debug("Done copying.")
            lgr.debug("Creating motion.xml file")


if __name__ == '__main__':
    run(sys.argv[1])
