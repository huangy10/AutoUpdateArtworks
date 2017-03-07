from __future__ import unicode_literals
import os
import xml.etree.cElementTree as ET
from conf import GlobalConfig
from xml.dom import minidom
from PIL import Image

from image_op import get_daily_image_dir

# In this script, we wrap the io operations here
base_dir = os.path.abspath(os.path.dirname(__file__))
conf = GlobalConfig()


def _(val):
    return "%s" % val


class MotionListLayout(object):

    def __init__(self):
        self.horizontal_interval = 60
        self.vertical_interval = 169
        self.left_margin = 200
        self.top_margin = 50
        self.item_width = 630
        self.item_height = 861

    @property
    def row_height(self):
        return self.item_height + self.vertical_interval

    @property
    def col_width(self):
        return self.item_width + self.horizontal_interval

    def layout_rect_for_id(self, idx):
        # idx starts from 1, minus 1 to make it start from 0
        idx = int(idx - conf.skip_as_num) - 1
        row = idx / 5
        col = idx % 5

        left = self.left_margin + float(col) * self.col_width
        top = float(row) * self.row_height

        return dict(left=_(left), top=_(top),
                    width=_(self.item_width), height=_(self.item_height))

default_list_layout = MotionListLayout()


class MotionXMLManger(object):

    def __init__(self, template_file):
        self.tree = ET.ElementTree(file=template_file)
        self.root = self.tree.getroot()

    def get_home_node(self):
        return self.root[0]

    def get_list_node(self):
        return self.root[1]

    def get_detail_root(self):
        return self.root[2]

    def add_artwork(self, artwork):
        list_layer = self.build_node_for_list_from_artwork(artwork)
        self.get_list_node().append(list_layer)
        detail_layer = self.build_node_for_detail_from_artwork(artwork)
        self.get_detail_root().append(detail_layer)


    def build_node_for_list_from_artwork(self, artwork):
        layer = ET.Element("layer", {"id": _(artwork.id)})
        img = ET.Element("img", {
            "id": "%s_img" % _(artwork.id),
            "file": os.path.join(conf.daily_image_folder, os.path.basename(artwork.get_thumbnail_path())),
            "name": artwork.artwork_name,
            "isshow": "yes",
            "detail_id": "%s_img_detail" % artwork.id,
            "img_state": "1"
        })
        layout_rect = ET.Element("rect", default_list_layout.layout_rect_for_id(artwork.id))

        img.append(layout_rect)
        layer.append(img)
        return layer

    def build_node_for_detail_from_artwork(self, artwork):
        layer = ET.Element("layer", {"id": "%s" % artwork.id})
        img = ET.Element("img", {
            "id": "%s_img_detail" % artwork.id,
            "file": os.path.join(conf.daily_image_folder, artwork.image_name),
            "name": artwork.artwork_name,
            "isshow": "no"
        })
        # calculate layout
        print artwork.get_detail_path()
        with Image.open(artwork.get_detail_path()) as im:
            width, height = im.size
            if width > height:
                orientation = "y"
            else:
                orientation = "x"
            left = int(3840 - (2150 / float(height) * float(width))) / 2

        layout_rect = ET.Element("rect", {
            "left": _(left), "top": "0", "width": _(width), "height": _(height),
            "orientation": orientation
        })

        img.append(layout_rect)
        layer.append(img)
        return layer


    def save(self, program_root):
        save_path = get_motion_xml_path(program_root)
        # self.tree.write(save_path, encoding="utf-8", xml_declaration=True)
        raw_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(raw_string)
        new_xml = reparsed.toprettyxml(indent="  ", newl="\n", encoding="utf-8")
        with open(save_path, "w") as f:
            f.write(new_xml)


def get_motion_xml_path(program_root):
    return os.path.join(get_daily_image_dir(program_root), "motion.xml")


def create_motion_xml(artworks, program_root):
    template_path = os.path.join(base_dir, "templates", "motion.template.xml")
    mgmt = MotionXMLManger(template_path)
    idx = conf.skip_as_num + 1
    for artwork in artworks:
        artwork.id = idx
        mgmt.add_artwork(artwork)
        idx += 1

    mgmt.save(program_root)
    print "done"


