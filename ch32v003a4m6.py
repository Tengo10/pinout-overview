import pinout as gen

from ch32v003 import pins, types 

pin_mapping = [ "PC1", "PC2", "PC3", "PC4", "PC6",
                "PC7", "PD1", "PD4", "PD5", "PD6",
                "PD7", "PA1", "PA2", "VSS", "VDD",
                "PD0" ]

pinout = gen.Package("CH32V003A4M6", "SOP")
pinout.set_footprint(16, 40, 80, 20, 60)
pinout.set_label(110, 10, 30)
pinout.add_types(types)
pinout.set_label_af_height( 0, 0, 0 );
pinout.package_width = 250
pinout.pin_push_out_extra = 14
pinout.pin_no_offset = 53
pinout.add_pins(pins)
pinout.add_mapping( pin_mapping )
pinout.subtitle = "SOP16 3.9x10mm\n1.27mm Pitch"
pinout.footprint_text = "SOP-16"
pinout.is_diag = True

pinout.save()