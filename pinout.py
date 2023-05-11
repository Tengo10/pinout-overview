import drawsvg as dw
import math

SIN_45 = 0.7071067811865475
COS_45 = 0.7071067811865476

class Package:
    def __init__(self, name, footprint):
        self.name = name
        self.footprint = footprint
        self.types = {}
        self.pins = []
        self.mapping = []

        self.pin_number = 0
        self.pin_spacing = 0
        self.pin_length = 0
        self.pin_width = 0
        self.corner_spacing = 0
        self.is_diag = False

        self.label_width = 0
        self.label_spacing = 0
        self.label_start = 0
        self.label_height = 0
        self.label_af_height = 0 #SOP Only
        self.label_pin_nominal_extra_spacing = 0 #SOP Only
        self.extra_vertical_spacing = 0  #SOP Only
        self.subtitle = "" # QFN Only
        self.padtitle = "" # QFN Only
        self.footprint_text = ""
        self.package_width = 0 # not overridden for QFN! QFN's only use package_height
        self.pin_no_offset = 0 # only used on SO
        self.pin_push_out_extra = 0
        self.package_height = 0
        self.legend_width = 0
        self.legend_height = 0

        self.canvas_height = 0
        self.canvas_width = 0

        self.types["spacer"] = {
            "borderColor": "white",
            "backgroundColor": "white",
            "textColor": "white",
            "skip" : True,
            "description": "spacer"
        }

    def set_footprint(self, pin_number, pin_spacing, pin_length, pin_width, corner_spacing):
        self.pin_number = pin_number
        self.pin_spacing = pin_spacing
        self.pin_length = pin_length
        self.pin_width = pin_width
        self.corner_spacing = corner_spacing

    def set_label_af_height( self, height, extra_vertical_spacing, nominal_lines ):
        self.label_af_height = height
        self.extra_vertical_spacing = extra_vertical_spacing
        self.label_pin_nominal_extra_spacing = nominal_lines

    def set_label(self, label_width, label_spacing, label_start):
        self.label_width = label_width
        self.label_spacing = label_spacing
        self.label_start = label_start

    def add_types(self, types):
        self.types = self.types | types

    def add_pins(self, pins):
        self.pins = pins
        
    def add_mapping(self, mapping):
        self.mapping = mapping

    def __draw_QFN(self):

        package_width = self.package_width

        package = dw.Group(id="Package", transform=f"rotate({45 if self.is_diag else 0}, {package_width/2}, {package_width/2})")
        footprint = dw.Group(id=self.name)
        
        border = dw.Rectangle(0, 0, package_width, package_width, 
                                 stroke="black", stroke_width=2, fill="grey")
        

        pad = dw.Path(stroke_width=2, stroke='black', fill='lightgrey', stroke_dasharray="4" )
        pad.M(self.corner_spacing+self.pin_width, self.corner_spacing-self.pin_width/2)
        pad.H(package_width-self.corner_spacing+self.pin_width/2)
        pad.V(package_width-self.corner_spacing+self.pin_width/2)
        pad.H(self.corner_spacing-self.pin_width/2)
        pad.V(self.corner_spacing+self.pin_width)
        pad.Z()

        pins = dw.Group(id="Pins")
        pin = dw.Rectangle(0, 0,
                               self.pin_width, self.pin_length,
                               stroke="black", stroke_width=2, fill="lightgrey", stroke_dasharray="4")
        
        for p in range(int(self.pin_number/4)):
            pins.append(dw.Use(pin, self.pin_spacing*p, 0,))
        
        dot = dw.Circle(self.corner_spacing/2-self.pin_width/6, self.corner_spacing/2-self.pin_width/6,
                              self.pin_width/3, stroke="black", stroke_width=2, fill="lightgrey")
                
        pin_numbers = dw.Group(id="PinNumbers")
        if self.is_diag:
            top_start_y = - self.package_width * SIN_45 + self.corner_spacing * SIN_45 + self.pin_width*0.75 * SIN_45
            top_start_x = - self.corner_spacing * COS_45 + self.pin_width*0.75 * COS_45
            #top_start_x = 0
            middle_start_x = (self.corner_spacing + self.pin_spacing*4)*SIN_45-self.package_width*SIN_45*1.5 - self.pin_width*0.25 * SIN_45
            middle_start_y = self.corner_spacing * COS_45 - self.pin_width*0.75 * SIN_45

            middle_start_x2 = (self.corner_spacing + self.pin_spacing*4)*SIN_45-self.package_width*SIN_45*.75 + self.pin_width*1.75 * SIN_45
            middle_start_y2 = (self.corner_spacing + self.pin_spacing*4) * COS_45 - self.pin_width*0.75 * SIN_45
            #middle_start_y2 = (self.corner_spacing + self.pin_spacing*4) * COS_45 - self.pin_width*.25 * SIN_45

            middle_start_x3 = (self.corner_spacing)*SIN_45+self.package_width*SIN_45*.5 + self.pin_width*0.25 * SIN_45
            middle_start_y3 = -self.corner_spacing * COS_45+self.pin_width*.75 * SIN_45
            for i in range(int(self.pin_number/4)):
                number_xy = self.pin_spacing * COS_45 * i
                pin_numbers.append(dw.Text(str(1+i), 15, top_start_x-number_xy, top_start_y+number_xy,
                                            text_anchor='middle', dominant_baseline='middle',
                                            font_family='Roboto Mono', fill="black"))
            for i in range(int(self.pin_number/4)):
                number_xy = self.pin_spacing * COS_45 * i
                pin_numbers.append(dw.Text(str(1+i+int(self.pin_number/4)), 15, middle_start_x+number_xy, middle_start_y+number_xy,
                                            text_anchor='middle', dominant_baseline='middle',
                                            font_family='Roboto Mono', fill="black"))
            for i in range(int(self.pin_number/4)):
                number_xy = self.pin_spacing * COS_45 * i
                pin_numbers.append(dw.Text(str(1+i+2*int(self.pin_number/4)), 15, middle_start_x2+number_xy, middle_start_y2-number_xy,
                                            text_anchor='middle', dominant_baseline='middle',
                                            font_family='Roboto Mono', fill="black"))
            for i in range(int(self.pin_number/4)):
                number_xy = self.pin_spacing * COS_45 * i
                pin_numbers.append(dw.Text(str(1+i+3*int(self.pin_number/4)), 15, middle_start_x3-number_xy, middle_start_y3-number_xy,
                                            text_anchor='middle', dominant_baseline='middle',
                                            font_family='Roboto Mono', fill="black"))
                
        package.append(border)
        package.append(pad)
        package.append(dot)
        for i in range(4):
            package.append(dw.Use(pins, self.corner_spacing-self.pin_width/2, 0,
                                    transform=f"rotate({i*90}, {package_width/2}, {package_width/2})"))
        footprint.append(dw.Use(package, -self.package_width/2, -self.package_height/2 ))
        footprint_text = dw.Text(self.footprint_text, 30, 0, -15,
                                     text_anchor='middle', dominant_baseline='middle', alignment_baseline='center',
                                     fill="black", font_weight='bold', font_family='Roboto Mono')
        footprint.append(footprint_text)
        footprint.append(pin_numbers)
        footprint.append(dw.Text(self.padtitle, 10, 0, 50,
                            text_anchor='middle', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono'))

        return footprint

    def __draw_SOP(self):
        footprint = dw.Group(id=self.name)

        border_core_width = (self.package_width-self.pin_length)
        border_core_height = (self.package_height-self.pin_width*2)
        borderCore = dw.Path(stroke="black", stroke_width=2, fill="grey")
        borderCore.M(0, 0)
        borderCore.H(border_core_width)
        borderCore.V(border_core_height)
        borderCore.H(0)
        borderCore.V(0)
        borderCore.Z()

        borderCoreInner = dw.Path(stroke="black", stroke_width=2, fill="grey")
        borderCoreInner.M(14, 4)
        borderCoreInner.H(border_core_width-4)
        borderCoreInner.V(border_core_height-4)
        borderCoreInner.H(14)
        borderCoreInner.V(4)
        borderCoreInner.Z()

        border = dw.Use( borderCore, -border_core_width/2, -border_core_height/2)
        borderInner = dw.Use( borderCoreInner, -border_core_width/2, -border_core_height/2)
        
        pin = dw.Path(stroke="black", stroke_width=2, fill="none")
        pin.M(0,0)
        pin.H(self.pin_length)
        pin.V(self.pin_width)
        pin.H(0)
        pin.V(0)
        pin.M(self.pin_length/3, 0)
        pin.V(self.pin_width)
        pin.M(self.pin_length*2/3, 0)
        pin.V(self.pin_width)
        pin.Z()

        pins = dw.Group(id="Pins")

        pin_numbers = dw.Group(id="PinNumbers")
        
        for p in range(int(self.pin_number/2)):
            y = (self.pin_spacing+self.extra_vertical_spacing)*(p+1) - self.package_height/2
            x = -self.package_width/2
            pins.append(dw.Use(pin, x-self.pin_length/2, y - self.pin_width/2))
            pin_numbers.append(dw.Text(str(p+1), 15, x+self.pin_no_offset, y,
                                        text_anchor='middle', dominant_baseline='middle',
                                        font_family='Roboto Mono', fill="black"))

            x = self.package_width/2
            pins.append(dw.Use(pin,  x-self.pin_length/2, y - self.pin_width/2))
            pin_numbers.append(dw.Text(str(self.pin_number-p), 15, x-self.pin_no_offset, y,
                                        text_anchor='middle', dominant_baseline='middle',
                                        font_family='Roboto Mono', fill="black"))

        footprint.append(pins)
        footprint.append(border)
        #footprint.append(borderInner) # Makes it look weird I fthink.
        footprint.append( dw.Use( dw.Circle( 0, 0, 10, stroke="black", stroke_width=2, fill="lightgrey" ), -border_core_width/2+30, -border_core_height/2+30))


        footprint_text = dw.Text(self.footprint_text, 30, 0, 0,
                                     text_anchor='middle', dominant_baseline='middle', alignment_baseline='center',
                                     fill="black", font_weight='bold', font_family='Roboto Mono')
        footprint.append(footprint_text)
        footprint.append(pin_numbers)

        return footprint
        
    def __calc_index_QFN(self):
        label_pos_index = []
        # Left side
        for i in range(int(self.pin_number/4)):
            index = [-1,
                        [-self.package_width/2, self.corner_spacing + i*self.pin_spacing-self.package_height/2],
                        [-self.label_start-self.package_width/2, self.corner_spacing + i*self.pin_spacing-self.package_height/2]]
            label_pos_index.append(index)
        extraSide = 0
        if self.pin_number/4 % 2 != 0:
            extraSide = 1
        # Bottom Left
        for i in range(int(self.pin_number/8)+extraSide):
            index = [-1, 
                        [self.corner_spacing + i*self.pin_spacing-self.package_width/2, self.package_width/2],
                        [-self.label_start-self.package_width/2,2*self.corner_spacing + (i+1.5)*self.pin_spacing]]
            label_pos_index.append(index)
        # Bottom Right
        for i in range(int(self.pin_number/8)):
            i2 = int(self.pin_number/4) + int(self.pin_number/8) - i - 1 + extraSide
            i3 = int(self.pin_number/8) + extraSide + i
            index = [1,
                        [self.corner_spacing + i3*self.pin_spacing-self.package_width/2, self.package_width/2],
                        [self.package_width/2 + self.label_start, 2*self.corner_spacing + i2*self.pin_spacing-self.package_height/2]]
            label_pos_index.append(index)
        # Right side
        for i in range(int(self.pin_number/4)):
            i2 = int(self.pin_number/4) - i - 1
            index = [1, 
                        [self.package_width/2, self.corner_spacing + i2*self.pin_spacing-self.package_height/2],
                        [self.package_width/2 + self.label_start, self.corner_spacing + i2*self.pin_spacing-self.package_height/2]]
            label_pos_index.append(index)
        # Top Right
        for i in range(int(self.pin_number/8)):
            i2 = int(self.pin_number/4) - i - 1
            index = [1,
                        [self.corner_spacing + i2*self.pin_spacing-self.package_width/2, -self.package_height/2],
                        [self.package_width + self.label_start-self.package_width/2, -self.corner_spacing - (i+extraSide)*self.pin_spacing-self.package_height/2]]
            label_pos_index.append(index)
        # Top Left
        for i in range(int(self.pin_number/8)+extraSide):
            i2 = int(self.pin_number/4) - int(self.pin_number/8) - i -1
            i3 = int(self.pin_number/8) + extraSide - i -1
            index = [-1,
                        [self.corner_spacing + i2*self.pin_spacing-self.package_width/2, -self.package_height/2],
                        [-self.label_start-self.package_width/2, -self.corner_spacing - i3*self.pin_spacing-self.package_height/2]]
            label_pos_index.append(index)
        return label_pos_index
    
    def __calc_index_QFN_diag(self):
        label_pos_index = []
        # Left Top side
        top_start_y = - self.package_width * SIN_45 + self.corner_spacing * SIN_45# + self.pin_width/4 * SIN_45
        top_start_x = - self.corner_spacing * COS_45# - self.pin_width/4 * COS_45

        middle_start_x = (self.corner_spacing + self.pin_spacing*4)*SIN_45
        middle_start_y = self.corner_spacing * COS_45

        label_spacing = self.pin_spacing / SIN_45

        # Left Top side
        for i in range(int(self.pin_number/4)):
            step = (self.pin_spacing)*SIN_45*i
            index = [ -1,
                    [top_start_x - step, top_start_y + step],
                    [top_start_x - step - 100, top_start_y + step*1.4-label_spacing+self.pin_width/2],
                    1
                 ]
            label_pos_index.append(index)
        # Left Bottom side
        for i in range(int(self.pin_number/4)):
            step = (self.pin_spacing)*SIN_45*i
            index = [ -1,
                    [-middle_start_x + step, middle_start_y + step],
                    [-middle_start_x + step-100, middle_start_y + step*1.4],
                    -1
                 ]
            label_pos_index.append(index)

        # Right Top side
        for i in range(int(self.pin_number/4)):
            step = (self.pin_spacing)*SIN_45*i
            index = [ 1,
                    [-top_start_x + step, top_start_y + step],
                    [-top_start_x + step + 100, top_start_y + step*1.4-label_spacing+self.pin_width/2],
                    -1
                 ]
            label_pos_index.append(index)
        
        # Right Bottom side
        for i in range(int(self.pin_number/4)):
            step = (self.pin_spacing)*SIN_45*i
            index = [ 1,
                    [middle_start_x - step, middle_start_y + step],
                    [middle_start_x - step + 100, middle_start_y + step*1.4],
                    1
                 ]
            label_pos_index.append(index)
        return label_pos_index
    

    def _generate_footprint(self):
        dw_footprint = dw.Group(id=self.name)

        if self.footprint == "QFN":
            self.package_width  = (self.pin_number/4-1) * self.pin_spacing + 2*self.corner_spacing
            self.package_height = self.package_width        
            dw_footprint = self.__draw_QFN()
        elif self.footprint == "SOP":
            # package_width is set by part.
            self.package_height = (self.pin_number/2+1) * (self.pin_spacing + self.extra_vertical_spacing)
            dw_footprint = self.__draw_SOP()
        return dw_footprint

    def __label_box(self, width, height, borderColour, borderWidth, backgroundColour, skew, radius, alt):
        label_box = dw.Rectangle(0, 0, width, height, rx=radius, ry=radius, 
                                 stroke=borderColour, stroke_width=borderWidth, 
                                 fill=backgroundColour, transform=f"skewX({skew})",
                                 stroke_dasharray="3 4" if alt else "", opacity=1)
        return label_box
    
    def _generate_label(self, name, border_color, background_color, text_color, alt=False, direction=1):
        dw_label = dw.Group(id=f"Label{name}-{'alt' if alt else 'std'}-{direction}")
        if direction == 1:
            skew = -self.label_height/2
        else:
            skew = self.label_height/2

        border_color = self._check_color(border_color)
        background_color = self._check_color(background_color)
        text_color = self._check_color(text_color)

        box = self.__label_box(self.label_width, self.label_height, 
                               border_color, 2, background_color, skew, 2, alt)

        dw_label.append(dw.Use(box, -skew/4, -self.label_height/2))
        
        if not alt:
            text = dw.Text(name, self.label_height-10, self.label_width/2, (self.label_height-10)/10,
                             text_anchor='middle', dominant_baseline='middle',
                             fill=text_color, font_weight='bold', font_family='Roboto Mono')
        else:
            text = dw.Text(name, self.label_height-10, self.label_width/2, (self.label_height-10)/10,
                             text_anchor='middle', dominant_baseline='middle',
                             fill=text_color, font_style='italic', font_family='Roboto Mono')
            
        dw_label.append(text)

        return dw_label


    
    def _generate_pin_label(self, pin, pin_functions, side=1, direction=1, afpin=0):
        side2 = int((side-1) /(-2))
        label_spacing = self.label_spacing+self.label_width
        dw_pin_label = dw.Group(id=f"PIN-{pin}-{afpin}")
        extent=0
        for i, function in enumerate(pin_functions):
            ftype = self.types[function["type"]]
            if "skip" in ftype: continue
            border_color = ftype["borderColor"]
            background_color = ftype["backgroundColor"]
            text_color = ftype["textColor"]
            label = self._generate_label(function["name"], border_color,
                                         background_color, text_color, function["alt"], direction)
            dw_pin_label.append(dw.Use(label, (i+side2)*label_spacing*side + self.label_spacing*side2, 0))
            extent=(i+0.5)*label_spacing*side
        return dw_pin_label, extent, -self.label_width*.75*side
    
    def _generate_label_line(self, start, stop, extentXmax, extentXmin, yofs):
        dw_label_line = dw.Path(stroke="black", stroke_width=2, fill="none")
        dw_label_line.M(start[0]-extentXmin, start[1]+yofs)
        dw_label_line.V(stop[1])
        dw_label_line.V(stop[1]+yofs)
        dw_label_line.H(stop[0]+extentXmax)
        return dw_label_line

    def _generate_pinout(self):
        
        dw_labels = dw.Group(id="Labels")
        dw_lineholder = dw.Group(id="Lines")
        dw_footprint = self._generate_footprint()
        self._calculate_size()
        self.label_height = self.pin_spacing-10
        label_pos_index = []

        if self.footprint == "QFN" and not self.is_diag:
            label_pos_index = self.__calc_index_QFN()

        elif self.footprint == "QFN" and self.is_diag:
            label_pos_index = self.__calc_index_QFN_diag()

        elif self.footprint == "SOP":
            for i in range(int(self.pin_number/2)):
                offset_x = 0-self.pin_push_out_extra
                overall_ofs_y = -(self.pin_spacing + self.extra_vertical_spacing) * ((self.pin_number/2)/2)
                offset_y = (i+0.5)*(self.pin_spacing + self.extra_vertical_spacing) + overall_ofs_y
                index = [-1, 
                         [offset_x-self.pin_length, offset_y],
                         [offset_x-self.label_start-self.pin_length, offset_y],
                         1]
                label_pos_index.append(index)
            for i in range(int(self.pin_number/2)):
                i2 = self.pin_number/2 - i - 1
                offset_x = self.pin_push_out_extra
                overall_ofs_y = -(self.pin_spacing + self.extra_vertical_spacing) * ((self.pin_number/2)/2) + self.extra_vertical_spacing*1.5
                #                * (int(self.pin_number/2)/2+(1-self.label_pin_nominal_extra_spacing*.75))
                offset_y = self.corner_spacing + (i2-1)*(self.pin_spacing + self.extra_vertical_spacing) + overall_ofs_y
                index = [1, 
                         [offset_x+self.pin_length, offset_y],
                         [offset_x+self.label_start+self.pin_length, offset_y],
                         1]
                label_pos_index.append(index)
        
        for i, m in enumerate(self.mapping):
            if hasattr( m, "__len__" ) and not isinstance( m, str ):
                afpinno = 0
                v_offset = math.floor(self.label_pin_nominal_extra_spacing-len(m))/2*self.label_af_height;
                for k in m:
                    pin = next(filter(lambda x: x[0]['name'] == k, self.pins))
                    dw_pin, extent, extentmin = self._generate_pin_label(str(i), pin, label_pos_index[i][0], direction=label_pos_index[i][3], afpin=afpinno)
                    dw_lineholder.append(self._generate_label_line(label_pos_index[i][1], label_pos_index[i][2], extent, extentmin, afpinno*self.label_af_height + v_offset))
                    dw_labels.append(dw.Use(dw_pin, label_pos_index[i][2][0], label_pos_index[i][2][1]+afpinno*self.label_af_height + v_offset))
                    afpinno = afpinno+1
            else:
                pin = next(filter(lambda x: x[0]['name'] == m, self.pins))
                dw_pin, extent, extentmin = self._generate_pin_label(str(i), pin, label_pos_index[i][0], direction=label_pos_index[i][3])
                dw_lineholder.append(self._generate_label_line(label_pos_index[i][1], label_pos_index[i][2], extent, extentmin, 0))
                dw_labels.append(dw.Use(dw_pin, label_pos_index[i][2][0], label_pos_index[i][2][1]))

        
        self.dwPinout = dw.Drawing(self.canvas_width, self.canvas_height, origin='center', displayInline=True)
        print(self.canvas_width, "  ", self.canvas_height)
        self.dwPinout.embed_google_font("Roboto Mono")
        self.dwPinout.append(dw.Rectangle(-self.canvas_width/2, -self.canvas_height/2, self.canvas_width, self.canvas_height,
                                          stroke="black", stroke_width=2, fill="white"))
        self.dwPinout.append(dw_footprint)
        self.dwPinout.append(dw_lineholder)
        self.dwPinout.append(dw_labels)
        self.dwPinout.append(dw.Use(self._generate_legend(), -self.canvas_width/2, self.canvas_height/2-160))
        self.dwPinout.append(dw.Use(self._generate_title(), 0, -self.canvas_height/2+60))

    def _generate_legend(self):
        label_amount = len(self.types)
        print(label_amount)
        column1 = self.canvas_width/6
        column2 = self.canvas_width/3
        column3 = self.canvas_width/2
        column4 = self.canvas_width/3*2

        legends = dw.Group(id="legends")

        for i, type in enumerate(self.types):
            legend_group = dw.Group(id=f"legend_{self.types[type]}")
            label = self._generate_label(type.upper(), self.types[type]["borderColor"], 
                                            self.types[type]["backgroundColor"] , self.types[type]["textColor"])
            legend_group.append(dw.Use(label, 0, 0))
            text = dw.Text(self.types[type]["description"], self.label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
            legend_group.append(dw.Use(text, self.label_width + 10, (self.label_height-10)/10))
            
            if i == 0:
                print()
            elif i < label_amount/3+1:
                legends.append(dw.Use(legend_group, column1, (i-1)*(self.label_height+self.label_spacing)))
            elif i < label_amount/3*2+1:
                legends.append(dw.Use(legend_group, column2, (i - label_amount/3-1)*(self.label_height+self.label_spacing)))
            else:
                legends.append(dw.Use(legend_group, column3, (i - label_amount/3*2-1)*(self.label_height+self.label_spacing)))

        legend_normal = dw.Group(id="legend_normal")
        label_normal = self._generate_label("FUNC", "black", 
                                            "white", "black")
        legend_normal.append(dw.Use(label_normal, 0, 0))
        text_normal = dw.Text("Default Function", self.label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
        legend_normal.append(dw.Use(text_normal, self.label_width + 10, (self.label_height-10)/10))
        legends.append(dw.Use(legend_normal, column4, 0))

        legend_alt = dw.Group(id="legend_alt")
        label_alt = self._generate_label("FUNC", "black", 
                                            "white", "black", alt=True)
        legend_alt.append(dw.Use(label_alt, 0, 0))
        text_alt = dw.Text("Alternative Function", self.label_height, 0, 0,
                            text_anchor='start', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono')
        legend_alt.append(dw.Use(text_alt, self.label_width + 10, (self.label_height-10)/10))
        legends.append(dw.Use(legend_alt, column4, self.label_height+self.label_spacing))

        return legends
    
    def _generate_title(self):
        title = dw.Group(id="title")
        title.append(dw.Text(self.name, 40, 0, 0,
                            text_anchor='middle', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono'))
        title.append(dw.Text(self.subtitle, 20, 0, 50,
                            text_anchor='middle', dominant_baseline='middle',
                            fill="black", font_weight='bold', font_family='Roboto Mono'))
        return title

    def _check_color(self, color):
        if isinstance(color, tuple) and len(color) == 3:
            return f"rgb({color[0]}, {color[1]}, {color[2]})"
        return color

    def _calculate_size(self):
        max_labels = max(map(len, self.pins))
        self.canvas_width = (self.package_width/2 + self.label_start + (self.label_width + self.label_spacing) * (max_labels+1))*2 + 2
        if self.footprint == "QFN":
            self.canvas_height = self.package_width + (self.pin_number/2+1) * self.pin_spacing + 4*self.corner_spacing + 2
        elif self.footprint == "SOP":
            self.canvas_height = (self.extra_vertical_spacing+self.pin_spacing) * (self.pin_number/2+1)*2 + 2
        
    def save(self):
        self._generate_pinout()
        self.dwPinout.save_svg(self.name + ".svg")
