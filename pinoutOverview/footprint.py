#from dataclasses import dataclass
import drawsvg as dw
from . import shapes

class label_line:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.side = -1
        self.direction = 1


class QFN():
    def __init__(self):

        self.pin_number = 0
        self.pin_width = 0
        self.pin_length = 0
        self.pin_spacing = 0
        self.corner_spacing = 0
        self.pin_side = 0
        self.pin_options = {}

        self.pad_width = 0
        self.dot_width = 0
        self.dot_position = 0
        self.dot_radius = 0

        self.package_width = 0
        self.package_options = {}
        self.is_diag = False

    def pin_opt(self, pin_number, pin_width, pin_length, pin_spacing, pin_options):
        self.pin_number     = pin_number
        self.pin_width      = pin_width
        self.pin_length     = pin_length
        self.pin_spacing    = pin_spacing
        self.pin_options    = pin_options
        self.pin_side       = int(pin_number/4)
        self.corner_spacing = self.pin_spacing * 1.5
        self.package_width  = self.pin_spacing * (self.pin_side - 1) + self.corner_spacing * 2
        self.pad_width      = self.package_width - self.corner_spacing*2
        self.dot_width      = self.pin_width / 3
        self.dot_position   = - self.package_width/2 + self.corner_spacing + self.dot_width/2

    def set_diag(self, diag):
        self.is_diag = diag

    
class Programmer():
    def __init__(self):
        self.pro = dw.Group(id='programmer')
        self.ics = dw.Group(id='prog-ics')
        self.pins = dw.Group(id='prog-pins')
        self.text = dw.Group(id='prog-text')
        self.ports = dw.Group(id='prog-ports')

        self.lines = dw.Group(id='prog-lines')

        self.out_index = [
            {"start_x": -320, "start_y": -40},
            {"start_x": -320, "start_y": -18},
            {"start_x": -320, "start_y": 4},
            {"start_x": -320, "start_y": 26},
            {"start_x": -320, "start_y": 48},
        ]
    def draw(self):
        pcb_style = {
            'fill': '#00CC00',
            'stroke': '#00AA00',
            'stroke-width': 1,
            'rx': 20,
            'ry': 20,
        }
        text_style = {
            'fill': 'white',
            'font-family': 'Roboto Mono',
            'font-size': 20,
            'text-anchor': 'left',
            'alignment-baseline': 'middle',

        }
        ic_style = {
            'fill': '#333333',
            'stroke': '#000000',
            'stroke-width': 1,
        }
        pin_style = {
            'fill': '#efc547',
            'stroke': '#af8a18',
            'stroke-width': 1,
        }
        port_style = {
            'fill': '#898989',
            'stroke': '#5b5b5b',
            'stroke-width': 1,
            'rx': 5,
            'ry': 5,
        }
        # Add Text
        text = [['GND', 'SWD', '3.3', '5V', 'GND']] #[['M0',  'CL',  '3.3', 'M1', 'M2'],
                
        row_x = -210
        row_y = -40
        row_x_spacing = 50
        row_y_spacing = 22
        for i,row in enumerate(text):
            for j, txt in enumerate(row):
                self.text.append(dw.Text(txt, 20, row_x + row_x_spacing*i, 
                                         row_y + row_y_spacing*j, **text_style))


        # Add ICs
        self.ics.append(dw.Rectangle(-35, -35, 70, 70, **ic_style, transform="rotate(45)"))

        # Add Pins
        pin_length = 100
        pin_width = 10
        pin_offset_x = row_x - 10 - pin_length
        pin_offset_y = row_y - pin_width -2
        pin_box_offset_x = row_x - 35 - row_y_spacing
        pin_box_offset_y = row_y - row_y_spacing +4
        for i in range(len(text[0])):
            self.pins.append(dw.Rectangle(pin_offset_x, pin_offset_y + i*row_y_spacing, 
                                          pin_length, pin_width, **pin_style))
            self.pins.append(dw.Rectangle(pin_box_offset_x, pin_box_offset_y + i*row_y_spacing,
                                          row_y_spacing, row_y_spacing, **ic_style, rx=2, ry=2))

        # Add Ports
        usb_x_offset = 200
        usb_y_offset = -40
        usb_width = 60
        usb_height = 80

        self.ports.append(dw.Rectangle(usb_x_offset, usb_y_offset, usb_width, usb_height,
                                       **port_style,))

        self.pro.append(shapes.label_box(500, 200, **pcb_style)) # PCB
        self.pro.append(self.ics)
        
        self.pro.append(self.ports)
        self.pro.append(self.text)
        self.pro.append(self.pins)

        return self.pro
    
    def line(self, index, end_x, end_y, **kwargs):



        #conn_line = dw.Group(id='conn-line')

        line_param = label_line()
        line_param.start_x = self.out_index[index]['start_x']
        line_param.start_y = self.out_index[index]['start_y']
        line_param.end_x = end_x
        line_param.end_y = end_y

        print(line_param)
        conn_line = shapes.label_line(line_param, 0, 0, **kwargs)

        return conn_line


