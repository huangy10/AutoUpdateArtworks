# coding=utf-8
from __future__ import unicode_literals
import os
import sys
import yaml
import logging.config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(BASE_DIR, "conf", "log_conf.yaml")) as f:
    log_config = yaml.load(f)
    logging.config.dictConfig(log_config)

lgr = logging.getLogger(__name__)


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Test(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.a = 1


class GlobalConfig(object):

    __metaclass__ = Singleton

    def __init__(self):
        with open(os.path.join(BASE_DIR, "conf", "global_conf.yaml")) as f:
            try:
                raw_config = yaml.load(f)
                data = raw_config["global"]
                self._skip_aw_num = data["skip_aw_num"]
                self._image_folder_name = data["image_folder_name"]
                self._image_formats = data["image_formats"]
                self._u_disk_name = data["U_disk_name"]
                self._daily_image_folder = data["daily_image_folder"]

                status = raw_config["status"]
                self._busy = status["busy"]
                self._history_valid = status["history_valid"]

                history = raw_config["history"]
                self._history = history

                self._raw_config = raw_config
            except KeyError:
                lgr.error("Error with global_conf.yaml. Invalid configuration.")

    @property
    def skip_as_num(self):
        return self._skip_aw_num

    @property
    def daily_image_folder(self):
        return self._daily_image_folder

    @property
    def image_folder_name(self):
        return self._image_folder_name

    @property
    def image_formats(self):
        return self._image_formats

    @property
    def u_disk_name(self):
        return self._u_disk_name

    @property
    def history_valid(self):
        return self._history_valid

    @history_valid.setter
    def history_valid(self, val):
        self._raw_config["status"]["history_valid"] = val
        self._history_valid = val

        self._update()

    @property
    def busy(self):
        return self._busy

    @busy.setter
    def busy(self, val):
        self._raw_config["status"]["busy"] = val
        self._busy = val

        self._update()

    def _update(self):
        with open(os.path.join(BASE_DIR, "conf", "global_conf.yaml"), "w") as f:
            f.write(yaml.dump(self._raw_config, default_flow_style=False, allow_unicode=True))

    def get_history(self):
        return self._history

    def update_history(self, new_history):
        self._raw_config["history"] = new_history
        self._update()

        self._history = new_history


class ConfigEnvironment(object):

    def __init__(self, conf):
        self.conf = conf

    def __enter__(self):
        if self.conf.busy:
            self.conf.history_valid = False
        else:
            self.conf.busy = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            print "exit with error"
            return
        print "normal"
        self.conf.busy = False
        self.conf.history_valid = True


def show_message_box(message):
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "书画鉴赏", 1)
