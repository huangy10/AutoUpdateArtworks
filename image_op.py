from __future__ import unicode_literals
import os
import shutil
import logging
from conf import GlobalConfig

lgr = logging.getLogger("palace")
conf = GlobalConfig()


def get_image_root(program_dir):
    return os.path.join(program_dir, "images")


def get_daily_image_dir(program_dir):
    image_root = get_image_root(program_dir)
    return os.path.join(image_root, conf.daily_image_folder)


def get_backup_dir(program_dir):
    image_root = get_image_root(program_dir)
    return os.path.join(image_root, "%s_backup" % conf.daily_image_folder)


def backup_images(program_dir):
    daily_images_dir = get_daily_image_dir(program_dir)

    if not os.path.exists(daily_images_dir):
        lgr.debug("No previous images found")
        return False

    backup_dir = get_backup_dir(program_dir)
    if os.path.exists(backup_dir):
        lgr.debug("Removing old backups")
        shutil.rmtree(backup_dir)

    lgr.debug("Creating backups")
    shutil.move(daily_images_dir, backup_dir)

    return True


def prepare_daily_image_folder(program_dir):
    daily_image_dir = get_daily_image_dir(program_dir)

    if os.path.exists(daily_image_dir):
        lgr.error("Cannot create daily image dir, that directory"
                  "already exists")
        return False

    os.makedirs(daily_image_dir)
    return True


def restore_backup(program_dir):
    pass
