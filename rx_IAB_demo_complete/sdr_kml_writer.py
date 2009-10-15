#!/usr/bin/env python

from lxml import etree

class kml_style_node():
    def __init__(self, id, icon_location, scale='0.8'):
        self.root = etree.Element('Style', id=id)

        icon_style_el = etree.SubElement(self.root, 'IconStyle')
        scale_el = etree.SubElement(icon_style_el, 'scale')
        icon_el = etree.SubElement(icon_style_el, 'Icon')
        href_el = etree.SubElement(icon_el, 'href')

        line_style_el = etree.SubElement(self.root, 'LineStyle')
        width_el = etree.SubElement(line_style_el, 'width')

        scale_el.text = scale
        href_el.text = icon_location
        width_el.text = '2'

    def get_id(self):
        return self.root.get("id")

    def get_scale(self):
        node = self.root.find("IconStyle/scale")
        return node.text

    def get_icon_location(self):
        node = self.root.find("IconStyle/href")
        return node.text

    def set_id(self, value):
        self.root.set("id",value)

    def set_scale(self, value):
        node = self.root.find("IconStyle/scale")
        node.text = value

    def set_icon_location(self, value):
        node = self.root.find("IconStyle/href")
        node.text = value

class extruded_placemark():
    def __init__(self, name, description, style_id, coordinates):
        self.root = etree.Element('Placemark')

        name_el = etree.SubElement(self.root, 'name')
        description_el = etree.SubElement(self.root, 'description')
        style_el = etree.SubElement(self.root, 'styleUrl')
        point_el = etree.SubElement(self.root, 'Point')
        extrude_el = etree.SubElement(point_el, 'extrude')
        alt_mode_el = etree.SubElement(point_el, 'altitudeMode')
        coordinates_el = etree.SubElement(point_el, 'coordinates')

        name_el.text = name
        description_el.text = description
        style_el.text = '#'+style_id
        coordinates_el.text=coordinates

        extrude_el.text = '1'
        alt_mode_el.text = 'relativeToGround'

    def get_name(self):
        node = self.root.find("name")
        return node.text

    def get_description(self):
        node = self.root.find("description")
        return node.text

    def get_style(self):
        node = self.root.find("styleUrl")
        return node.text.strip('#')

    def get_coordinates(self):
        node = self.root.find("Point/coordinates")
        string = node.text
        list = string.split(',')
        return list

    def set_name(self, value):
        node = self.root.find("name")
        node.text = value

    def set_dscription(self, value):
        node = self.root.find("description")
        node.text = value

    def set_style(self, value):
        node = self.root.find("styleUrl")
        node.text = '#'+value

    def set_coordinates(self, values):
        node = self.root.find("Point/coordinates")
        node.text = ",".join(values)

class kml_writer():
    def __init__(self):
        self.style_list = []

        kml_el = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.page = etree.ElementTree(kml_el)

        document_el = etree.SubElement(kml_el, 'Document')

        picture_folder = '/home/aryoung/Desktop/rx_IAB_demo/'
        command_lo = picture_folder + 'command-center1.png'
        helmet_lo = picture_folder + 'fire-helmet-1.png'
        truck_lo = picture_folder + 'fire-truck1.png'
        radio_lo = picture_folder + 'Hand-Held-Radio-1.png'
        plb_lo = picture_folder + 'plb-1.png'
        dog_lo = picture_folder + 'dog_icon.png'


        self.add_style('command-center', command_lo, '2.2')
        self.add_style('fire-helmet', helmet_lo, '2')
        self.add_style('fire-truck', truck_lo, '2')
        self.add_style('hand-radio', radio_lo, '2')
        self.add_style('plb', plb_lo, '2.8')
        self.add_style('k9-unit', dog_lo, '2')

        self.extra_lines="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

    def add_style(self, style_id, icon_location, scale='0.8'):
        node = self.page.find("Document")
        style_node = kml_style_node(style_id, icon_location, scale)
        node.append(style_node.root)
        self.style_list.append(style_id)

    def add_placemark(self, name, description, coordinates, style='hand-radio'):
        node = self.page.find("Document")
#         if not(len(coordinates) == 2):
#             raise Exception("kml_writer::add_placemark-coordinates wrong length")

        coordinates = coordinates.strip('[]')
        coordinates = coordinates +',' + "50"
#        print "in add_placemark, coords: ", coordinates
#         list = []
#         for item in coordinates:
#             list.append(str(item))
        placemark = extruded_placemark(name, description, style, coordinates)
        node.append(placemark.root)


    def get_placemark(self, name):
        root = self.page.find("Document")
        # everything below here is a huge hack
        # because we don't have lxml2 and cant use
        # ''root.iter()''
        for el in root:
            if el.tag == "Placemark":
                for el2 in el:
                    if el2.tag == "name":
                        if el2.text == name:
                            node = el2
                            break
        return node.getparent()

    def update_placemark(self, placemark, new_coord):
#         if not(len(new_coord) == 2):
#             raise Exception("kml_writer::update_placemark-coordinates wrong length")
        
        node = self.get_placemark(placemark)
        node = node.find("Point/coordinates")
#         string = str(new_coord[0])+','+str(new_coord[1])+','+'50'
        node.text = new_coord + ',' + '50'

    def write_to_file(self, filename):
        f = open(filename, 'w')
        f.write(self.extra_lines)
        f.write("\n")
        self.page.write(f, pretty_print=True)
        f.close()

if __name__=='__main__':
    doc = kml_writer()
    coordinates = [-81.41633,37.22911]
    doc.add_placemark("Floating Fire Helmet", "Holy Cow it's a floating fire helmet", coordinates,'fire-helmet')
    doc.write_to_file('test_kml_writer.kml')
    doc.update_placemark("Floating Fire Helmet", [-81.41633,37.22911])
    doc.write_to_file('test_kml_writer1.kml')
