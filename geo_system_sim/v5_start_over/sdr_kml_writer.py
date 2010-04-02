#!/usr/bin/env python

from lxml import etree
import numpy as np

class kml_icon_node():
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

class colored_pushpin():
    def __init__(self, id, color, scale = '1.0'):
        self.root = etree.Element('Style', id=id)

        icon_style_el = etree.SubElement(self.root, 'IconStyle')
        scale_el = etree.SubElement(icon_style_el, 'scale')
        icon_el = etree.SubElement(icon_style_el, 'Icon')
        href_el = etree.SubElement(icon_el, 'href')

        color_el = etree.SubElement(icon_style_el, 'color')
        color_mode_el = etree.SubElement(icon_style_el, 'colorMode')

        line_style_el = etree.SubElement(self.root, 'LineStyle')
        width_el = etree.SubElement(line_style_el, 'width')

        scale_el.text = scale
        href_el.text = 'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
        width_el.text = '2'

        color_el.text = color
        color_mode_el.text = 'normal'

    def get_id(self):
        return self.root.get("id")

    def get_scale(self):
        node = self.root.find("IconStyle/scale")
        return node.text

    def get_color(self):
        node = self.root.find('IconStyle/color')
        return node.text

    def set_id(self, value):
        self.root.set("id",value)

    def set_scale(self, value):
        node = self.root.find("IconStyle/scale")
        node.text = value

    def set_color(self, value):
        node = self.root.find('IconStyle/color')
        node.text = value

class line_color():
    def __init__(self, id, color, width):
        self.root = etree.Element('Style', id=id)
        
        linestyle_el = etree.SubElement(self.root, 'LineStyle')
        width_el = etree.SubElement(linestyle_el, 'width')
        color_el = etree.SubElement(linestyle_el, 'color')
        color_mode_el = etree.SubElement(linestyle_el, 'colorMode')
    
        width_el.text = width
        color_el.text = color
        color_mode_el.text = 'normal'

    def get_width(self):
        node = self.root.find('LineStyle/width')
        return node.text

    def get_color(self):
        node = self.root.find('LineStyle/color')
        return node.text

    def set_width(self, value):
        node = self.root.find('LineStyle/width')
        node.text = value

    def set_color(self, value):
        node = self.root.find('LineStyle/color')
        node.text = value
        

class polygon_color():
    def __init__(self, id, color):
        self.root = etree.Element('Style', id=id)
        
        polystyle_el = etree.SubElement(self.root,'PolyStyle')
        color_el = etree.SubElement(polystyle_el, 'color')
        color_mode_el = etree.SubElement(polystyle_el, 'colorMode')
        
        color_el.text = color
        color_mode_el.text = 'normal'

    def get_color(self):
        node = self.root.find('PolyStyle/color')
        return node.text

    def set_color(self, value):
        node = self.root.find('PolyStyle/color')
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
        return string

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
        node.text = values

class line():
    def __init__(self, name, description, style_id, points):
        self.root = etree.Element("Placemark")
        
        name_el = etree.SubElement(self.root, 'name')
        descrip_el = etree.SubElement(self.root, 'description')
        style_el = etree.SubElement(self.root, 'styleUrl')
        
        line_el = etree.SubElement(self.root, 'LineString')
        tess_el = etree.SubElement(line_el, 'tessellate')
        coord_el = etree.SubElement(line_el, 'coordinates')

        name_el.text = name
        descrip_el.text = description
        style_el.text = '#' + style_id
        
        coord_el.text = points

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
        node = self.root.find("LineString/coordinates")
        string = node.text
        return string

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
        node = self.root.find("LineString/coordinates")
        node.text = values

    def append_point(self, point):
        coords = self.get_coordinates()
        coords += point + '\n'
        self.set_coordinates(coords)

class polygon():
    def __init__(self, name, description, style_id, outer_ring, inner_ring):
        self.root = etree.Element('Placemark')

        name_el = etree.SubElement(self.root, 'name')
        descrip_el = etree.SubElement(self.root, 'description')
        style_el = etree.SubElement(self.root, 'styleUrl')
        poly_el = etree.SubElement(self.root, 'Polygon')
        extrude_el = etree.SubElement(poly_el, 'extrude')
        alt_mode_el = etree.SubElement(poly_el, 'altitudeMode')
        
        out_bound_el = etree.SubElement(poly_el, 'outerBoundaryIs')
        out_lin_ring_el = etree.SubElement(out_bound_el, 'LinearRing')
        out_lin_ring_coords_el = etree.SubElement(out_lin_ring_el, 'coordinates')
        
        in_bound_el = etree.SubElement(poly_el, 'innerBoundaryIs')
        in_lin_ring_el = etree.SubElement(in_bound_el, 'LinearRing')
        in_lin_ring_coords_el = etree.SubElement(in_lin_ring_el, 'coordinates')

        name_el.text = name
        descrip_el.text = description
        style_el.text = '#'+style_id
        out_lin_ring_coords_el.text = outer_ring
        in_lin_ring_coords_el.text = inner_ring

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

    def get_outer_coordinates(self):
        node = self.root.find("Polygon/outerBoundaryIs/LinearRing/coordinates")
        string = node.text
        return string

    def get_inner_coordinates(self):
        node = self.root.find("Polygon/innerBoundaryIs/LinearRing/coordinates")
        string = node.text
        return string

    def set_name(self, value):
        node = self.root.find("name")
        node.text = value

    def set_dscription(self, value):
        node = self.root.find("description")
        node.text = value

    def set_style(self, value):
        node = self.root.find("styleUrl")
        node.text = '#'+value

    def set_outer_coordinates(self, values):
        node = self.root.find("Polygon/outerBoundaryIs/LinearRing/coordinates")
        node.text = values

    def set_inner_coordinates(self, values):
        node = self.root.find("Polygon/innerBoundaryIs/LinearRing/coordinates")
        node.text = values
        

class kml_writer():
    def __init__(self):
        self.placemarks = {}
        self.boxes = {}
        self.lines = {}
        
        kml_el = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.page = etree.ElementTree(kml_el)

        document_el = etree.SubElement(kml_el, 'Document')
    
        self.extra_lines="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

    def add_icon(self, style_id, icon_location, scale='0.8'):
        node = self.page.find("Document")
        style_node = kml_icon_node(style_id, icon_location, scale)
        node.append(style_node.root)

    def add_colored_pushpin(self, style_id, color, scale ='1.0'):
        node = self.page.find('Document')
        style_node = colored_pushpin(style_id, color, scale)
        node.append(style_node.root)

    def add_line_color(self, style_id, color, width = '1.0'):
        node = self.page.find('Document')
        style_node = line_color(style_id, color, width)
        node.append(style_node.root)

    def add_polygon_color(self, style_id, color):
        node = self.page.find('Document')
        style_node = polygon_color(style_id, color)
        node.append(style_node.root)
        

    def add_placemark(self, name, description, coordinates, style='hand-radio'):
        node = self.page.find("Document")

        coordinates = str(coordinates).strip('[]')
        coordinates = coordinates +',' + "50"

        placemark = extruded_placemark(name, description, style, coordinates)
        node.append(placemark.root)

        self.placemarks[name] = placemark

    def add_line(self, name, description, style, points):
        node = self.page.find('Document')

        point_string = '\n'
        for point in points:
            point_string += '\t' + str(point).strip('[]') + ',30\n'

        line_node = line(name, description, style, point_string)
        node.append(line_node.root)

        self.lines[name] = line_node

    def add_box(self, name, description, style, corner1, corner2):
        out_coords = []
        
        out_coords.append(corner1)
        out_coords.append([corner2[0], corner1[1]])
        out_coords.append(corner2)
        out_coords.append([corner1[0], corner2[1]])
        out_coords.append(corner1)

        center = []
        center.append((corner1[0] + corner2[0])/2)
        center.append((corner1[1] + corner2[1])/2)
        

        outer_string = '\n'
        for point in out_coords:
            outer_string += '\t' + str(point).strip('[]') + ',30\n'

        inner_string = str(center).strip('[]') + ',30'

        node = self.page.find('Document')
        
        polygon_node = polygon(name, description, style, outer_string, inner_string)
        node.append(polygon_node.root)

        self.boxes[name] = polygon_node


    def update_placemark_loc(self, placemark_name, new_coord):
        string = str(new_coords).strip('[]') + ',50'
        self.placemarks[placemark_name].set_coordinates(string)

    def add_point_to_line(self, name, point):
        string = '\t'+ str(point).strip('[]') + ',30'
        self.lines[name].append_point(string)

    def update_box_loc(self, name,  corner1, corner2):
        out_coords = []
        
        out_coords.append(corner1)
        out_coords.append([corner2[0], corner1[1]])
        out_coords.append(corner2)
        out_coords.append([corner1[0], corner2[1]])
        out_coords.append(corner1)

        center = []
        center.append((corner1[0] + corner2[0])/2)
        center.append((corner1[1] + corner2[1])/2)
        

        outer_string = ''
        for point in out_coords:
            outer_string += str(point).strip('[]') + ',30\n'

        inner_string = str(center).strip('[]') + ',30'
        
        self.boxes[name].set_outer_coordinates(outer_string)
        self.boxes[name].set_inner_coordinates(inner_string)

    def get_style(self, style_id):
        root = self.page.find("Document")
        for el in root:
            if el.tag == 'Style':
                if el.get('id') == style_id:
                    node = el
                    break

        return node

    def update_pushpin_color(self, style_id, color):
        node = self.get_style(style_id)
        node = node.find('IconStyle/color')
        node.text = color

    def update_line_color(self, style_id, color):
        node = self.get_style(style_id)
        node = node.find('LineStyle/color')
        node.text = color

    def update_line_width(self, style_id, width):
        node = self.get_style(style_id)
        node = node.find('LineStyle/width')
        node.text = str(width)

    def update_polygon_color(self, style_id, color):
        node = self.get_style(style_id)
        node = node.find('PolyStyle/color')
        node.text = color

    def write_to_file(self, filename):
        f = open(filename, 'w')
        f.write(self.extra_lines)
        f.write("\n")
        self.page.write(f, pretty_print=True)
        f.close()

if __name__=='__main__':

    doc = kml_writer()
    # coordinates = [-81.41633,37.22911]
    # doc.add_placemark("Floating Fire Helmet", "Holy Cow it's a floating fire helmet", coordinates,'fire-helmet')
    # doc.write_to_file('test_kml_writer.kml')
    # doc.update_placemark("Floating Fire Helmet", [-81.41633,37.22911])
    # doc.write_to_file('test_kml_writer1.kml')


    #color aabbggrr

    x_lat = np.float64(38.81201111111111)
    x_lon = np.float64(-77.03778888888888)


    y_lat = np.float64(38.80172777777778)
    y_lon = np.float64(-77.06365833333334)

    line_data = [[-77.0638751200912,38.80163063822256],
                 [-77.06438427058546,38.80154193628145],
                 [-77.06500681851284,38.80136496318837],
                 [-77.06664823429649,38.80105449600172],
                 [-77.06749732744755,38.80096529343693],
                 [-77.06806315284953,38.80092063282158],
                 [-77.06924934883216,38.80092022117781],
                 [-77.07026434818849,38.80131677480325],
                 [-77.07065761769348,38.80184565413999],
                 [-77.07071217109308,38.8026385582689],
                 [-77.0707075022372,38.8033000825568],
                 [-77.07075265379531,38.80431482107588],
                 [-77.07073689884108,38.80519756743023],
                 [-77.0707188131228,38.80621116429549],
                 [-77.07059537223508,38.80682733577608],
                 [-77.07052545189553,38.80761862056147]]


    doc.add_colored_pushpin('green_pushpin', 'ff00ff00')
    doc.add_colored_pushpin('red_pushpin', 'ff0000ff')

    doc.add_placemark('corner1','corner 1 of box', [x_lon,x_lat], 'green_pushpin')
    doc.add_placemark('corner2','corner 2 of box', [y_lon,y_lat], 'red_pushpin')

    doc.add_line_color('line_color', 'ff7f007f')
    doc.add_line('line','hey it is a line', 'line_color', line_data)
    doc.add_point_to_line('line', [-77.07046411558089,38.80788222224388])

    doc.update_line_width('line_color', 5)

    doc.add_polygon_color('box1', '7fff0000')
    doc.add_box('box', 'here is a box','box1', [x_lon,x_lat],[y_lon,y_lat])
    doc.write_to_file('box.kml')

    
