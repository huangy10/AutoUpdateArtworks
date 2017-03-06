# coding=utf-8
# 1. Detect the insertion of external drive and find if image inputs exits
# 2. Build the motion.xml config file
# 3. Copy the images and configuration file into the corresponding directory
from __future__ import unicode_literals

import os
import sys
import logging
import shutil

from conf import GlobalConfig, ConfigEnvironment, show_message_box
from image_loader import load_images, need_recreate_motion_xml, get_abs_dir
from image_op import backup_images, prepare_daily_image_folder, get_daily_image_dir
from image_processing.processor import build_thumbnail


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
        # Check if the images are valid
        res = reduce(lambda a, b: a
                                  and b.is_valid, images, True)
        if not res:
            lgr.debug("Find invalid image name.")
            show_message_box(
                "发现不正确的图片名称，注意图片名称应当符合“名字_装裱_作者_朝代.jpg”（或png)的格式，且请注意"
                "附上封面，封面的名称应该为“名字_装裱_作者_朝代_cover.jpg”（或者png）的格式。"
            )
            return
        if not need_recreate_motion_xml(images):
            lgr.debug("No update is found.")
            return
        else:
            daily_image_dir = \
                prepare_image_directories(program_root)
            if daily_image_dir is None:
                lgr.debug("Fail to create destination folders")
                show_message_box("无法创建目标文件夹")
                return
            # copy images into this dir
            lgr.debug("Copying images into destination folder")
            for image in images:
                src_abs_path = image.image_path
                dst_abs_path = os.path.join(daily_image_dir, image.image_name)
                shutil.copy(src_abs_path, dst_abs_path)

                # copy cover if exits
                src_cover_abs_path = image.get_cover_path()
                if os.path.exists(src_cover_abs_path):
                    dst_cover_abs_path = os.path.join(
                        daily_image_dir, os.path.basename(image.get_cover_path())
                    )

                    shutil.copy(src_cover_abs_path, dst_cover_abs_path)

                image.move_to(daily_image_dir)

                # generate thumbnail
                build_thumbnail(image)

            lgr.debug("Done copying.")
            lgr.debug("Creating motion.xml file")


if __name__ == '__main__':
    run(sys.argv[1])
