import pinout as gen

from ch32v003 import pins, types 

pin_mapping = [ "PD7", "PA1", "PA2", "VSS", "PD0",
                "VDD", "PC0", "PC1", "PC2", "PC3",
                "PC4", "PC5", "PC6", "PC7", "PD1",
                "PD2", "PD3", "PD4", "PD5", "PD6" ]
                  
pinout = gen.Package("ch32v003f4u6", "QFN")
pinout.set_footprint(20, 40, 30, 20, 60)
pinout.set_label(110, 10, 30)
pinout.add_types(types)
pinout.add_pins(pins)
pinout.add_mapping(pin_mapping)
pinout.is_diag = True
pinout.subtitle = "3x3mm, 0.4mm BSC"
pinout.padtitle = "Connect thermal pad\npad to ground"
pinout.footprint_text = "QFN20\nTOP VIEW"
pinout.save()