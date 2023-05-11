import pinout as gen

from ch32v003 import pins, types 

pin_mapping = [ ["PD6","PA1"], "VSS", "PA2", "VDD",
                "PC1", "PC2", "PC4", ["PD1","PD5","PD4"] ]
                  
pinout = gen.Package("ch32v003j4m6", "SOP")
pinout.set_footprint(8, 40, 100, 30, 60)
pinout.set_label(110, 10, 30)
pinout.add_types(types)
pinout.add_pins(pins)
pinout.set_label_af_height( 40, 50, 1 );
pinout.package_width = 400
pinout.pin_no_offset = 35
pinout.subtitle = "SOP8 3.9x5.0mm\n1.27mm Pitch"
pinout.footprint_text = "SOP-8"
pinout.pin_push_out_extra = 105
pinout.add_mapping(pin_mapping)
pinout.is_diag = True

pinout.save()