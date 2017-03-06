from __future__ import unicode_literals
import os
import xml.etree.cElementTree as ET
from conf import GlobalConfig

# In this script, we wrap the io operations here
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
conf = GlobalConfig()


class MotionXMLManger(object):

    def __int__(self, template_file):
        self.tree = ET.ElementTree(file=template_file)
        self.root = self.tree.getroot()

    def get_home_node(self):
        return self.root[0]

    def get_list_node(self):
        return self.root[1]

    def get_detail_root(self):
        return self.root[2]

    def add_image_with_name(self, image, idx):
        home = self.get_home_node()
        list = self.get_list_node()
        detail = self.get_detail_root()

    def build_node_for_home(self, image, idx):
        node = ET.Element("layer", {"id": "%s" % idx})


def create_motion_xml(images):
    pass
