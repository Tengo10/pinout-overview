import drawsvg as dw

class Package:
    def __init__(self, name, footprint):
        self.name = name
        self.footprint = footprint
        self.types = {}
        self.pins = []

        self.pin_number = 0
        self.pin_spacing = 0
        self.pin_length = 0
        self.pin_width = 0
        self.corner_spacing = 0

        self.label_width = 0
        self.label_spacing = 0
        self.label_start = 0
        self.label_height = 0

        self.package_width = 0
        self.package_height = 0
        self.legend_width = 0
        self.legend_height = 0

        self.canvas_height = 0
        self.canvas_width = 0

        self.types["spacer"] = {
            "borderColor": "white",
            "backgroundColor": "white",
            "textColor": "white",
            "description": "spacer"
        }

        # self.dwPinout = dw.Drawing(2000, 1000, origin='center', displayInline=False)

    def set_footprint(self, pin_number, pin_spacing, pin_length, pin_width, corner_spacing):
        self.pin_number = pin_number
        self.pin_spacing = pin_spacing
        self.pin_length = pin_length
        self.pin_width = pin_width
        self.corner_spacing = corner_spacing

    def set_label(self, label_width, label_spacing, label_start):
        self.label_width = label_width
        self.label_spacing = label_spacing
        self.label_start = label_start

    def add_types(self, types):
        self.types = self.types | types

    def add_pins(self, pins):
        self.pins = pins

    def _generate_footprint(self):
        dw_footprint = dw.Group(id=self.name)
        if self.footprint == "QFN":
            self.package_width = package_width = (self.pin_number/4-1) * self.pin_spacing + 2*self.corner_spacing
            self.package_height = self.package_width
            outer = dw.Rectangle(0, 0, package_width, package_width, 
                                 stroke="black", stroke_width=2, fill="grey")
            
            dw_footprint.append(outer)

            pad = dw.Path(stroke_width=2, stroke='black', fill='lightgrey')
            pad.M(self.corner_spacing+self.pin_width, self.corner_spacing-self.pin_width/2)
            pad.H(package_width-self.corner_spacing+self.pin_width/2)
            pad.V(package_width-self.corner_spacing+self.pin_width/2)
            pad.H(self.corner_spacing-self.pin_width/2)
            pad.V(self.corner_spacing+self.pin_width)
            pad.Z()

            dw_pins = dw.Group(id="Pins")
            pin = dw.Rectangle(0, 0,
                               self.pin_width, self.pin_length,
                               stroke="black", stroke_width=2, fill="lightgrey")
            
            for p in range(int(self.pin_number/4)):
                dw_pins.append(dw.Use(pin, self.pin_spacing*p, 0,))

            for i in range(4):
                dw_footprint.append(dw.Use(dw_pins, self.corner_spacing-self.pin_width/2, 0,
                                            transform=f"rotate({i*90}, {package_width/2}, {package_width/2})"))

            point = dw.Circle(self.corner_spacing-self.pin_width/4, self.corner_spacing-self.pin_width/4,
                              self.pin_width/4, stroke="black", stroke_width=2, fill="lightgrey")
            

            dw_footprint.append(point)
            
            dw_footprint.append(pad)
            


        elif self.footprint == "SOP":
            self.package_height = (self.pin_number/2+1) * self.pin_spacing
            self.package_width = 200
            print(self.package_height)
            #outside = dw.Rectangle(self.pin_length,0, self.package_width, self.package_height, 
            #                       stroke="black", stroke_width=2, fill="none")
            #inside = dw.Rectangle(self.pin_length+self.package_width*0.025, self.package_width*0.025, 
            #                      self.package_width-self.package_width*0.025*2, self.package_height-self.package_width*0.025*2, 
            #                      stroke="black", stroke_width=2, fill="none")
            
            border = dw.Path(stroke="black", stroke_width=2, fill="none")
            border.M(self.pin_length, 0)
            border.H(self.pin_length+self.package_width)
            border.V(self.package_height)
            border.H(self.pin_length)
            border.V(0)
            border.M(self.pin_length+self.package_width*0.025, self.package_width*0.025)
            border.H(self.pin_length+self.package_width*(1-0.025))
            border.V(self.package_height-self.package_width*0.025)
            border.H(self.pin_length+self.package_width*0.025)
            border.V(self.package_width*0.025)
            border.L(self.pin_length, 0)
            border.M(self.pin_length+self.package_width, 0)
            border.L(self.pin_length+self.package_width*(1-0.025), self.package_width*0.025)
            border.M(self.pin_length+self.package_width, self.package_height)
            border.L(self.pin_length+self.package_width*(1-0.025), self.package_height-self.package_width*0.025)
            border.M(self.pin_length, self.package_height)
            border.L(self.pin_length+self.package_width*0.025, self.package_height-self.package_width*0.025)
            border.Z()
            #border.M(self.pac)


            dw_pin = dw.Path(stroke="black", stroke_width=2, fill="none")
            dw_pin.M(0,0)
            dw_pin.H(self.pin_length)
            dw_pin.V(self.pin_width)
            dw_pin.H(0)
            dw_pin.V(0)
            dw_pin.M(self.pin_length/3, 0)
            dw_pin.V(self.pin_width)
            dw_pin.M(self.pin_length*2/3, 0)
            dw_pin.V(self.pin_width)
            dw_pin.Z()

            dw_pins = dw.Group(id="Pins")

            for p in range(int(self.pin_number/2)):
                dw_pins.append(dw.Use(dw_pin, 0, self.pin_spacing*(p+1)))
                dw_pins.append(dw.Use(dw_pin, self.pin_length+self.package_width, self.pin_spacing*(p+1)))

            #dw_footprint.append(outside)
            #dw_footprint.append(inside)
            dw_footprint.append(border)
            dw_footprint.append(dw_pins)

        footprint_text = dw.Text(f"{self.footprint}-{self.pin_number}", 30, 0, 0,
                                     text_anchor='middle', dominant_baseline='middle',
                                     fill="black", font_weight='bold', font_family='Roboto Mono')
        
        dw_footprint.append(dw.Use(footprint_text, self.package_width/2, self.package_height/2))
        return dw_footprint
    
    def __label_box(self, width, height, borderColour, borderWidth, backgroundColour, skew, radius):
        label_box = dw.Rectangle(0, 0, width, height, rx=radius, ry=radius, 
                                 stroke=borderColour, stroke_width=borderWidth, 
                                 fill=backgroundColour, transform=f"skewX({skew})")
        return label_box
    
    def _generate_label(self, name, border_color, background_color, text_color, alt=False):
        dw_label = dw.Group(id=f"Label{name}-{'alt' if alt else 'std'}")

        skew = -self.label_height/2

        border_color = self._check_color(border_color)
        background_color = self._check_color(background_color)
        text_color = self._check_color(text_color)

        box = self.__label_box(self.label_width, self.label_height, 
                               border_color, 2, background_color, skew, 2)

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


    
    def _generate_pin_label(self, pin, pin_functions, side=1):
        side2 = int((side-1) /(-2))
        label_spacing = self.label_spacing+self.label_width
        dw_pin_label = dw.Group(id=f"PIN-{pin}")
        for i, function in enumerate(pin_functions):
            border_color = self.types[function["type"]]["borderColor"]
            background_color = self.types[function["type"]]["backgroundColor"]
            text_color = self.types[function["type"]]["textColor"]
            label = self._generate_label(function["name"], border_color,
                                         background_color, text_color, function["alt"])
            dw_pin_label.append(dw.Use(label, (i+side2)*label_spacing*side + self.label_spacing*side2, 0))
        return dw_pin_label
    
    def _generate_label_line(self, start, stop):
        dw_label_line = dw.Path(stroke="black", stroke_width=2, fill="none")
        dw_label_line.M(start[0], start[1])
        dw_label_line.V(stop[1])
        dw_label_line.H(stop[0])
        return dw_label_line

    def _generate_pinout(self):
        dw_labels = dw.Group(id="Labels")
        dw_footprint = self._generate_footprint()
        self.label_height = self.pin_spacing-10
        label_pos_index = []
        if self.footprint == "QFN":
            # Left side
            for i in range(int(self.pin_number/4)):
                index = [-1, 
                         [0, self.corner_spacing + i*self.pin_spacing],
                         [-self.label_start, self.corner_spacing + i*self.pin_spacing]]
                label_pos_index.append(index)
            extraSide = 0
            if self.pin_number/4 % 2 != 0:
                extraSide = 1
            # Bottom Left
            for i in range(int(self.pin_number/8)+extraSide):
                i2 = i + int(self.pin_number/4)
                index = [-1, 
                         [self.corner_spacing + i*self.pin_spacing, self.package_width],
                         [-self.label_start,2*self.corner_spacing + i2*self.pin_spacing]]
                label_pos_index.append(index)
            # Bottom Right
            for i in range(int(self.pin_number/8)):
                i2 = int(self.pin_number/4) + int(self.pin_number/8) - i - 1 + extraSide
                i3 = int(self.pin_number/8) + extraSide + i
                index = [1,
                         [self.corner_spacing + i3*self.pin_spacing, self.package_width],
                         [self.package_width + self.label_start, 2*self.corner_spacing + i2*self.pin_spacing]]
                label_pos_index.append(index)
            # Right side
            for i in range(int(self.pin_number/4)):
                i2 = int(self.pin_number/4) - i - 1
                index = [1, 
                         [self.package_width, self.corner_spacing + i2*self.pin_spacing],
                         [self.package_width + self.label_start, self.corner_spacing + i2*self.pin_spacing]]
                label_pos_index.append(index)
            # Top Right
            for i in range(int(self.pin_number/8)):
                i2 = int(self.pin_number/4) - i - 1
                index = [1,
                         [self.corner_spacing + i2*self.pin_spacing, 0],
                         [self.package_width + self.label_start, -self.corner_spacing - (i+extraSide)*self.pin_spacing]]
                label_pos_index.append(index)
            # Top Left
            for i in range(int(self.pin_number/8)+extraSide):
                i2 = int(self.pin_number/4) - int(self.pin_number/8) - i -1
                i3 = int(self.pin_number/8) + extraSide - i -1
                index = [-1,
                         [self.corner_spacing + i2*self.pin_spacing, 0],
                         [-self.label_start, -self.corner_spacing - i3*self.pin_spacing]]
                label_pos_index.append(index)

        elif self.footprint == "SOP":
            for i in range(int(self.pin_number/2)):
                index = [-1, 
                         [0, (i+1)*self.pin_spacing+self.pin_width/2],
                         [-self.label_start, (i+1)*self.pin_spacing+self.pin_width/2]]
                label_pos_index.append(index)
            for i in range(int(self.pin_number/2)):
                i2 = self.pin_number/2 - i - 1
                index = [1, 
                         [self.package_width+2*self.pin_length, self.corner_spacing + i2*self.pin_spacing-self.pin_width/2],
                         [self.package_width + self.label_start+2*self.pin_length, self.corner_spacing + i2*self.pin_spacing-self.pin_width/2]]
                label_pos_index.append(index)
        
        for i, pin in enumerate(self.pins):
            dw_pin = self._generate_pin_label(str(i), pin, label_pos_index[i][0])
            dw_labels.append(dw.Use(dw_pin, label_pos_index[i][2][0], label_pos_index[i][2][1]))
            dw_labels.append(self._generate_label_line(label_pos_index[i][1], label_pos_index[i][2]))

        self._calculate_size()
        self.dwPinout = dw.Drawing(self.canvas_width, self.canvas_height, origin='center', displayInline=True)
        print(self.canvas_width, "  ", self.canvas_height)
        self.dwPinout.embed_google_font("Roboto Mono")
        self.dwPinout.append(dw.Rectangle(-self.canvas_width/2, -self.canvas_height/2, self.canvas_width, self.canvas_height,
                                          stroke="black", stroke_width=2, fill="white"))
        self.dwPinout.append(dw.Use(dw_footprint, -self.package_width/2, -self.package_height/2))
        self.dwPinout.append(dw.Use(dw_labels, -self.package_width/2, -self.package_height/2))
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
        text_alt = dw.Text("Alternativ Function", self.label_height, 0, 0,
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
        return title

    def _check_color(self, color):
        if isinstance(color, tuple) and len(color) == 3:
            return f"rgb({color[0]}, {color[1]}, {color[2]})"
        return color

    def _calculate_size(self):
        max_labels = max(map(len, self.pins))
        self.canvas_width = (self.package_width/2 + self.label_start + (self.label_width + self.label_spacing) * max_labels)*2 + 2
        if self.footprint == "QFN":
            self.canvas_height = self.package_width + (self.pin_number/2+1) * self.pin_spacing + 4*self.corner_spacing + 2
        elif self.footprint == "SOP":
            self.canvas_height = self.pin_spacing * (self.pin_number/2+1)*2 + 2
        
    def save(self):
        self._generate_pinout()
        self.dwPinout.save_svg(self.name + ".svg")
