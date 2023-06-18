import os
import sys
import drawsvg as dw
import yaml
from yamlinclude import YamlIncludeConstructor
from pinoutOverview import shapes
from pinoutOverview import footprint as fp
SIN_45 = 0.7071067811865475

class label_line:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.side = -1
        self.direction = 1

class Package:
    def __init__(self):
        self.data = {}

        self.canvas_height = 0
        self.canvas_width = 0

    def load_data(self, path):
        YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader , base_dir=os.path.dirname(path))
        with open(path, 'r', encoding='utf-8') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def __draw_QFN(self):

        pin_number      = int(self.data['footprint'].split('-')[1])
        pin_side        = int(pin_number/4)
        pin_spacing     = self.data['pin']['spacing_calc']
        pin_length      = self.data['pin']['length']
        pin_width       = self.data['pin']['width']
        corner_spacing  = pin_spacing*1.5
        package_width   = pin_spacing * (pin_side-1) + corner_spacing*2
        pad_width       = package_width - corner_spacing*2
        dot_width       = pin_width/3
        dot_position    = - package_width/2 + corner_spacing + dot_width/2
        is_diag         = self.data['package']['diagonal']
        rotate_opt      = f"rotate({45 if is_diag else 0}, {0}, {0})"
        
        package     = dw.Group(id="package", transform=rotate_opt)
        footprint   = dw.Group(id=self.data['name'])
        pins        = dw.Group(id="pins")
        pin_numbers = dw.Group(id="pin-numbers")

        border  = shapes.qfn_border(package_width, **self.data['package']['style'])
        pad     = shapes.qfn_pad(pad_width, **self.data['pin']['style'])
        pin     = shapes.qfn_pin(pin_width, pin_length, **self.data['pin']['style'])
        dot     = dw.Circle( dot_position, dot_position, dot_width,
                            **self.data['package']['marker_style'])
        fp_font_size = int(self.data['package']['text_style']['font_size'])
        pd_font_size = int(self.data['package']['sub_text_style']['font_size'])
        del self.data['package']['text_style']['font_size']
        del self.data['package']['sub_text_style']['font_size']

        fp_text = dw.Text(self.data['package_text']['text'], fp_font_size, 0, self.data['package']['text_offset'],
                          **self.data['package']['text_style'])
        pd_text = dw.Text(self.data['package_text']['sub_text'], pd_font_size, 0, self.data['package']['sub_text_offset'],
                          **self.data['package']['sub_text_style'])

        for p in range(pin_side):
            pins.append(dw.Use(pin, (-package_width+pin_length)/2,
                               -package_width/2+corner_spacing+p*pin_spacing))
        
        start_x = package_width/2 - pin_width/2 - 3
        start_y = - package_width/2 + corner_spacing

        if is_diag:
            start_x = (corner_spacing - pin_width*0.75) * SIN_45
            start_y = (corner_spacing - package_width*0.5 - pin_width) / SIN_45 - 3

        self.data['pin']['style']["text_anchor"] = "middle"

        for i in range(pin_side):
            number_x = pin_spacing * SIN_45 * i if is_diag else 0
            number_y = pin_spacing * SIN_45 * i if is_diag else pin_spacing * i+pin_width/10

            pin_numbers.append(dw.Text(str(1+i), 15, -start_x-number_x, start_y+number_y+1,
                                        **self.data['pin']['text_style'], text_anchor='middle'))
        for i in range(pin_side):
            number_x = pin_spacing * SIN_45 * i if is_diag else pin_spacing * i
            number_y = pin_spacing * SIN_45 * i if is_diag else pin_width/10

            pin_numbers.append(dw.Text(str(1+i+pin_side), 15, start_y+number_x, start_x+number_y+1,
                                        **self.data['pin']['text_style'], text_anchor='middle'))
        for i in range(pin_side):
            number_x = pin_spacing * SIN_45 * i if is_diag else 0
            number_y = pin_spacing * SIN_45 * i if is_diag else pin_spacing * i -pin_width/10

            pin_numbers.append(dw.Text(str(1+i+2*pin_side), 15, start_x+number_x, -start_y-number_y+1,
                                        **self.data['pin']['text_style'], text_anchor='middle'))
        for i in range(pin_side):
            number_x = pin_spacing * SIN_45 * i if is_diag else pin_spacing * i
            number_y = pin_spacing * SIN_45 * i if is_diag else -pin_width/10

            pin_numbers.append(dw.Text(str(1+i+3*pin_side), 15, -start_y-number_x, -start_x-number_y+1,
                                        **self.data['pin']['text_style'], text_anchor='middle'))
        
        package.append(border)
        package.append(pad)
        package.append(dot)
        for i in range(4):
            package.append(dw.Use(pins, 0, 0,transform=f"rotate({i*90}, {0}, {0})"))

        footprint.append(package)

        footprint.append(fp_text)
        footprint.append(pd_text)
        footprint.append(pin_numbers)

        return footprint

    def __draw_SOP(self):
        
        pin_number      = int(self.data['footprint'].split('-')[1])

        pin_length      = self.data['pin']['length']
        pin_width       = self.data['pin']['width']
        pin_spacing_og  = self.data['pin']['spacing']
        pin_spacing     = self.data['pin']['spacing_calc']
        pin_side        = int(pin_number/2)
        pin_no_offset   = self.data['pin']['number_offset']
        
        package_height  = (pin_number/2+1) * pin_spacing
        package_width   = self.data['package']['width']
        
        footprint   = dw.Group(id=self.data['name'])
        pins        = dw.Group(id="pins")
        pin_numbers = dw.Group(id="pin-numbers")
        border      = shapes.sop_border(package_width, package_height, **self.data['package']['style'])
        marker      = dw.Circle(-package_width/2+pin_spacing_og, -package_height/2+pin_spacing_og,
                                pin_width/2, **self.data['package']['marker_style'])

        fp_font_size = int(self.data['package']['text_style']['font_size'])
        pd_font_size = int(self.data['package']['sub_text_style']['font_size'])
        del self.data['package']['text_style']['font_size']
        del self.data['package']['sub_text_style']['font_size']

        fp_text = dw.Text(self.data['package_text']['text'], fp_font_size, 0, -15,
                          **self.data['package']['text_style'])
        pd_text = dw.Text(self.data['package_text']['sub_text'], pd_font_size, 0, 50,
                          **self.data['package']['sub_text_style'])
        pin         = shapes.sop_pin(pin_width, pin_length, **self.data['pin']['style'])
        
        
        for p in range(pin_side):
            y = - package_height/2 + pin_spacing * (p+1)
            x = - package_width/2 - pin_length/2
            pins.append(dw.Use(pin, x, y))
            pin_numbers.append(dw.Text(str(p+1), pin_width, x+pin_length/2+pin_no_offset, 
                                       y+pin_width/10, **self.data['pin']['text_style'], text_anchor='start'))

            x = package_width/2+pin_length/2
            pins.append(dw.Use(pin,  x, y))
            pin_numbers.append(dw.Text(str(pin_number-p), pin_width, x-pin_length/2-pin_no_offset,
                                       y+pin_width/10, **self.data['pin']['text_style'], text_anchor='end'))

        footprint.append(pins)
        footprint.append(border)
        footprint.append(marker)
        footprint.append(fp_text)
        footprint.append(pd_text)
        footprint.append(pin_numbers)

        return footprint
        
    def __calc_index_QFN(self):
        
        package_width   = self.data['package']['width']
        pin_spacing     = self.data['pin']['spacing_calc']
        corner_spacing  = pin_spacing*1.5
        pin_number      = int(self.data['footprint'].split('-')[1])
        pin_side1       = int(pin_number/4)
        pin_side2       = int(pin_number/8)
        label_start     = self.data['label']['offset']
        extra_side      = 0
        label_pos_index = []

        # Check for uneven number of pins
        if pin_number/4 % 2 != 0:
            extra_side = 1

        # Left side
        for i in range(pin_side1):
            line = label_line()
            y = -package_width/2 + corner_spacing + i*pin_spacing
            line.start_x = -package_width/2
            line.start_y = y
            line.end_x = -label_start-package_width/2
            line.end_y = y

            label_pos_index.append(line)
        
        # Bottom Left
        for i in range(pin_side2+extra_side):
            line = label_line()
            line.start_x = corner_spacing + i*pin_spacing-package_width/2
            line.start_y = package_width/2
            line.end_x = -label_start-package_width/2
            line.end_y = 2*corner_spacing + (i+3)*pin_spacing
            label_pos_index.append(line)
            
        # Bottom Right
        for i in range(pin_side2):
            line = label_line()
            i2 = pin_side1 + pin_side2 - i - 1 + extra_side
            i3 = pin_side2 + extra_side + i
            line.start_x = corner_spacing + i3*pin_spacing-package_width/2
            line.start_y = package_width/2
            line.end_x = package_width/2 + label_start
            line.end_y =2*corner_spacing + i2*pin_spacing-package_width/2
            line.side = 1
            label_pos_index.append(line)
        # Right side
        for i in range(pin_side1):
            line = label_line()
            i2 = pin_side1 - i - 1
            line.start_x = package_width/2
            line.start_y = corner_spacing + i2*pin_spacing-package_width/2
            line.end_x = package_width/2 + label_start
            line.end_y = corner_spacing + i2*pin_spacing-package_width/2
            line.side = 1
            label_pos_index.append(line)
        # Top Right
        for i in range(pin_side2):
            line = label_line()
            i2 = pin_side1 - i - 1
            line.start_x = corner_spacing + i2*pin_spacing-package_width/2
            line.start_y = -package_width/2
            line.end_x = label_start+package_width/2
            line.end_y = -corner_spacing - (i+extra_side)*pin_spacing-package_width/2
            line.side = 1
            label_pos_index.append(line)
        # Top Left
        for i in range(pin_side2+extra_side):
            line = label_line()
            i2 = pin_side1 - pin_side2 - i -1
            i3 = pin_side2 + extra_side - i -1
            line.start_x = corner_spacing + i2*pin_spacing-package_width/2
            line.start_y = -package_width/2
            line.end_x = -label_start-package_width/2
            line.end_y = -corner_spacing - i3*pin_spacing-package_width/2
            label_pos_index.append(line)
        return label_pos_index
    
    def __calc_index_QFN_diag(self):
        label_pos_index     = []
        package_width       = self.data['package']['width']
        pin_spacing         = self.data['pin']['spacing_calc']
        corner_spacing      = pin_spacing*1.5
        pin_number          = int(self.data['footprint'].split('-')[1])
        pin_side1           = int(pin_number/4)
        label_start         = self.data['label']['offset'] + (-corner_spacing*2.75) * SIN_45
        center_offset       = 0 if not 'center_offset' in self.data['label'] else self.data['label']['center_offset']

        # Left Top side
        start_x0 = (-corner_spacing) * SIN_45
        start_y0 = (corner_spacing - package_width) * SIN_45

        start_x1 = (corner_spacing - package_width) * SIN_45
        start_y1 = (corner_spacing) * SIN_45

        # Left Top side
        for i in range(pin_side1):
            line = label_line()
            step = pin_spacing*SIN_45*i
            line.start_x = start_x0 - step
            line.start_y = start_y0 + step
            line.end_x = start_x0 - step-label_start
            line.end_y = - (pin_side1-i) * pin_spacing - center_offset

            label_pos_index.append(line)

        # Left Bottom side
        for i in range(pin_side1):
            line = label_line()
            step = pin_spacing*SIN_45*i
            
            line.start_x = start_x1 + step
            line.start_y = start_y1 + step
            line.end_x = start_x1 + step-label_start
            line.end_y = start_y1 + (i) * pin_spacing + center_offset
            line.direction = -1

            label_pos_index.append(line)

        # Right Bottom side
        for i in range(pin_side1):
            line = label_line()
            step = pin_spacing*SIN_45*i
            line.start_x = - start_x0 + step
            line.start_y = - start_y0 - step
            line.end_x = - start_x0 + step + label_start
            line.end_y = + (pin_side1-i) * pin_spacing + center_offset
            line.side = 1

            label_pos_index.append(line)

        # Right Top side
        for i in range(pin_side1):
            line = label_line()
            step = pin_spacing*SIN_45*i
            
            line.start_x = - start_x1 - step
            line.start_y = - start_y1 - step
            line.end_x = - start_x1 - step + label_start
            line.end_y = - start_y1 - (i) * pin_spacing - center_offset
            line.side = 1
            line.direction = -1

            label_pos_index.append(line)

        return label_pos_index
    

    def __calc_index_SOP(self):
        
        pin_number          = int(self.data['footprint'].split('-')[1])
        pin_spacing         = self.data['pin']['spacing_calc']
        package_width       = self.data['package']['width']
        pin_length          = self.data['pin']['length']
        label_width         = self.data['label']['width']
        label_start         = self.data['label']['offset']
        corner_spacing      = self.data['pin']['spacing_calc']*1.5

        label_pos_index     = []

        for i in range(int(pin_number/2)):
            line = label_line()
            overall_ofs_y = -(pin_spacing) * ((pin_number/2)/2)
            offset_y = (i+0.5)*(pin_spacing) + overall_ofs_y
            line.start_x = -package_width/2-pin_length
            line.start_y = offset_y
            line.end_x = -label_start-pin_length-label_width
            line.end_y = offset_y
            label_pos_index.append(line)

        for i in range(int(pin_number/2)):
            line = label_line()
            i2 = pin_number/2 - i - 1
            overall_ofs_y = -(pin_spacing) * (pin_number/4)
            offset_y = corner_spacing + (i2-1)*(pin_spacing) + overall_ofs_y
            line = label_line()
            line.start_x = package_width/2+pin_length
            line.start_y = offset_y
            line.end_x = label_start+pin_length+label_width
            line.end_y = offset_y
            line.side = 1
            label_pos_index.append(line)
        return label_pos_index

    def _generate_footprint(self):
        footprint       = self.data['footprint'].split('-')[0]
        pin_number      = int(self.data['footprint'].split('-')[1])
        pin_spacing     = self.data['pin']['spacing_calc']
        
        corner_spacing  = pin_spacing*1.5
        
        dw_footprint = dw.Group(id=self.data['name'])
        
        if footprint == "QFN":
            self.data['package']['width']   = (pin_number/4-1) * pin_spacing + 2*corner_spacing
            self.data['package']['height']  = (pin_number/4-1) * pin_spacing + 2*corner_spacing
            dw_footprint = self.__draw_QFN()
        elif footprint == "SOP":
            dw_footprint = self.__draw_SOP()
        return dw_footprint
    
    def _generate_label(self, name, ftype, label_width, alt=False, direction=1):
        label_height    = self.data['label']['height']

        type_box = ftype["box_style"] if "box_style" in ftype else {}
        type_text = ftype["text_style"] if "text_style" in ftype else {}

        dw_label = dw.Group(id=f"Label-{name}-{'alt' if alt else 'std'}-{direction}")
        skew = -label_height/2*direction

        box_opts = self.data['label']['box_style' if not alt else 'alt_box_style']
        box_opts |= type_box

        box_opts["transform"] = f" skewX({skew})"

        text_opts = self.data['label']['text_style' if not alt else 'alt_text_style']
        text_opts |= type_text

        box = shapes.label_box(label_width, label_height, **box_opts)
        text = shapes.label_text(name, label_height, **text_opts)

        dw_label.append(box)
        dw_label.append(text)

        return dw_label

    def _generate_pin_label(self, pin, pin_functions, op, afpin=0):
        
        label_width = self.data['label']['width']
        label_dist = self.data['label']['spacing']
        label_offset = self.data['label']['offset']
        label_spacing = 0
        side = op.side
        direction = op.direction
        #side2 = 0
        dw_pin_label = dw.Group(id=f"PIN-{pin}-{afpin}-{'left' if side == -1 else 'right'}-{direction}")
        extent=0

        for function in pin_functions:
            ftype = self.data['types'][function["type"]]
            label_width = self.data['label']['width']
            if "width" in ftype:
                label_width = ftype["width"]
            if "skip" in ftype:
                if ftype["skip"]:
                    label_spacing += label_dist + label_width
                    continue
            label = self._generate_label(function["name"], ftype, label_width, function["alt"], direction)
            dw_pin_label.append(dw.Use(label, (label_spacing+label_width*0.5)*side, 0))
            label_spacing += label_dist + label_width
            extent=(label_spacing-label_width*0.5)*side
        
        return dw_pin_label, extent, -label_offset*side

    def _generate_pinout(self):
        
        footprint       = self.data['footprint'].split('-')[0]
        pin_number      = self.data['footprint'].split('-')[1]
        mapping         = self.data['mapping']
        is_diag         = self.data['package']['diagonal']

        self._calculate_size()
        dw_labels = dw.Group(id="labels")
        dw_lineholder = dw.Group(id="lines")
        dw_footprint = self._generate_footprint()
        
        
        label_pos_index = []

        if footprint == "QFN" and not is_diag:
            label_pos_index = self.__calc_index_QFN()

        elif footprint == "QFN" and is_diag:
            label_pos_index = self.__calc_index_QFN_diag()

        elif footprint == "SOP":
            label_pos_index = self.__calc_index_SOP()
        
        line = self.data["label"]["label_line_style"]
        for i, m in enumerate(mapping):
            if i > int(pin_number)-1:
                pass
            elif hasattr( m, "__len__" ) and not isinstance( m, str ):
                line_op = label_pos_index[i]
                line_op.end_y -= (self.data['label']['height'] + self.data['label']['vert_spacing']) * (len(m)*0.75 if len(m) % 2 == 0 else len(m)/1.5)
                for j, k in enumerate(m):
                    pin = self.data['pins'][k]
                    line_op.end_y += (self.data['label']['height'] + self.data['label']['vert_spacing'])
                    dw_pin, extent, extentmin = self._generate_pin_label(str(i), pin, label_pos_index[i], afpin=j)
                    dw_lineholder.append(shapes.label_line(line_op, extent, extentmin, **line))
                    dw_labels.append(dw.Use(dw_pin, line_op.end_x, line_op.end_y))

            else:
                pin = self.data['pins'][m]
                line_op = label_pos_index[i]
                dw_pin, extent, extentmin = self._generate_pin_label(m, pin, line_op)
                dw_lineholder.append(shapes.label_line(line_op, extent, 0, **line))
                dw_labels.append(dw.Use(dw_pin, line_op.end_x, line_op.end_y))


        self.canvas_width   = 2500 if 'canvas_width' not in self.data else self.data['canvas_width']
        self.canvas_height  = 1000 if 'canvas_height' not in self.data else self.data['canvas_height']
        
        package_x_offset = 0 if 'package_x_offset' not in self.data else self.data['package_x_offset']
        package_y_offset = 0 if 'package_y_offset' not in self.data else self.data['package_y_offset']

        


        self.dwPinout = dw.Drawing(self.canvas_width, self.canvas_height, origin='center', displayInline=True)
        print(self.canvas_width, "  ", self.canvas_height)
        self.dwPinout.embed_google_font("Roboto Mono")
        self.dwPinout.append(dw.Rectangle(-self.canvas_width/2, -self.canvas_height/2, self.canvas_width, self.canvas_height,
                                          stroke="black", stroke_width=2, fill="white"))
        self.dwPinout.append(dw.Use(dw_lineholder, package_x_offset, package_y_offset))
        self.dwPinout.append(dw.Use(dw_footprint, package_x_offset, package_y_offset))
        self.dwPinout.append(dw.Use(dw_labels, package_x_offset, package_y_offset))
        self.dwPinout.append(dw.Use(self._generate_legend(), -self.canvas_width/2, self.canvas_height/2-160))
        self.dwPinout.append(dw.Use(self._generate_title(), 0, -self.canvas_height/2+60))

        if 'custom_image' in self.data:
            print("Custom Image Found")
            programmer = fp.Programmer()
            board = programmer.draw()
            self.dwPinout.append(dw.Use(board, self.data['custom_image']['x_offset'], self.data['custom_image']['y_offset']))
            #for l in self.data['custom_image']['connections']:
            #    print(l[1])
            #    img_line_op = label_pos_index[l[1]]
            #    print(img_line_op)
            #    img_line = programmer.line(l[0], img_line_op.end_x, img_line_op.end_y, **line)
            #    self.dwPinout.append(img_line)

        if 'text_field' in self.data:
            for field in self.data['text_field']:
                self.dwPinout.append(dw.Text(field['text'], field['font_size'], field['x'], field['y'], **field['style']))


        if 'line' in self.data:
            for l in self.data['line']:
                c_line = dw.Path(**l['style'])
                for cmd in l['path']:
                    if cmd[0] == 'M':
                        c_line.M(cmd[1], cmd[2])
                    elif cmd[0] == 'L':
                        c_line.L(cmd[1], cmd[2])
                    elif cmd[0] == 'H':
                        c_line.H(cmd[1])
                    elif cmd[0] == 'V':
                        c_line.V(cmd[1])
                    elif cmd[0] == 'Q':
                        c_line.Q(cmd[1], cmd[2], cmd[3], cmd[4])
                    elif cmd[0] == 'C':
                        c_line.C(cmd[1], cmd[2], cmd[3], cmd[4], cmd[5], cmd[6])
                    elif cmd[0] == 'Z':
                        c_line.Z()
                self.dwPinout.append(c_line)

        if 'custom_label' in self.data:
            for l in self.data['custom_label']:
                ftype  = self.data['types'][l["type"]]
                if "width" in ftype:
                    label_width = ftype["width"]
                c_label = self._generate_label(l['text'], ftype, label_width)
                self.dwPinout.append(dw.Use(c_label, l['x'], l['y']))


    def _generate_legend(self):
        label_amount = len(self.data['types'])
        label_height = self.data['label']['height']
        label_width = self.data['label']['width']
        label_spacing = self.data['label']['spacing']

        column1 = self.canvas_width/7
        column2 = self.canvas_width/3.2
        column3 = self.canvas_width/2
        column4 = self.canvas_width/3*2

        legends = dw.Group(id="legends")

        for i, typ in enumerate(self.data['types']):
            ftype = self.data['types'][typ]
            if "width" in ftype:
                label_width = ftype["width"]
            if "skip" in ftype:
                if ftype["skip"]:
                    continue
            legend_group = dw.Group(id=f"legend_{typ}")
            
            label = self._generate_label(typ.upper(), ftype, label_width)
            legend_group.append(dw.Use(label, 0, 0))
            text = dw.Text(ftype['description'], label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
            legend_group.append(dw.Use(text, label_width/2 + 20, (label_height-10)/10))
            
            if i < label_amount/3-1:
                legends.append(dw.Use(legend_group, column1, (i)*(label_height+label_spacing)))
            elif i < label_amount/3*2-1:
                legends.append(dw.Use(legend_group, column2, (i - label_amount/3)*(label_height+label_spacing)))
            else:
                legends.append(dw.Use(legend_group, column3, (i - label_amount/3*2)*(label_height+label_spacing)))

        legend_normal = dw.Group(id="legend_normal")
        label_normal = self._generate_label("FUNC", {'box_style': {'fill': 'white', 'stroke': 'black'}}, self.data['label']['width'])
        legend_normal.append(dw.Use(label_normal, 0, 0))
        text_normal = dw.Text("Default Function", label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
        legend_normal.append(dw.Use(text_normal, label_width + 10, (label_height-10)/10))
        legends.append(dw.Use(legend_normal, column4, 0))

        legend_alt = dw.Group(id="legend_alt")
        label_alt = self._generate_label("FUNC", {'box_style': {'fill': 'white', 'stroke': 'black'}}, self.data['label']['width'], alt=True)
        
        legend_alt.append(dw.Use(label_alt, 0, 0))
        text_alt = dw.Text("Alternate Function", label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
        legend_alt.append(dw.Use(text_alt, label_width + 10, (label_height-10)/10))
        legends.append(dw.Use(legend_alt, column4, label_height+label_spacing))

        return legends
    
    def _generate_title(self):
        title = dw.Group(id="title")
        title.append(dw.Text(self.data['name'], 40, 0, 0,
                            text_anchor='middle', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono'))
        title.append(dw.Text(self.data['subtitle'], 20, 0, 50,
                            text_anchor='middle', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono'))
        return title

    def _calculate_size(self):
        mapping = self.data['mapping']
        max_lines = 2

        for i, m in enumerate(mapping):
                if hasattr( m, "__len__" ) and not isinstance( m, str ):
                    if len(m) > max_lines:
                        max_lines = len(m)
        
        self.data['pin']['spacing_calc'] = (max_lines-1) * (self.data['label']['height'] + self.data['label']['vert_spacing'])
        #max_labels = max(map(len, self.pins))
        #self.canvas_width = (self.package_width/2 + self.label_start + (self.label_width + self.label_spacing) * (max_labels+1))*2 + 2
        
        #if self.footprint == "QFN":
        #    self.canvas_height = self.package_width + (self.pin_number/2+1) * self.pin_spacing + 4*self.corner_spacing + 2
        #elif self.footprint == "SOP":
        #    self.canvas_height = (self.extra_vertical_spacing+self.pin_spacing) * (self.pin_number/2+1)*2 + 2
        
    def save(self, out):
        self._generate_pinout()
        if out == "":
            out = self.data['name'] + ".svg"
        if out[-4:] != ".svg":
            out += ".svg"
        
        self.dwPinout.save_svg(out)

if __name__ == "__main__":
    pinout = Package()
    pinout.load_data(sys.argv[1])
    name = ""
    if len(sys.argv) > 2:
        name = sys.argv[2]
    pinout.save(name)