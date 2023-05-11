import pinout as gen

from ch32v003 import pins, types 

pin_mapping = [ "PD4", "PD5", "PD6", "PD7", "PA1",
                "PA2", "VSS", "PD0", "VDD", "PC0",
                "PC1", "PC2", "PC3", "PC4", "PC5",
                "PC6", "PC7", "PD1", "PD2", "PD3" ]

pinout = gen.Package("CH32V003F4P6", "SOP")
pinout.set_footprint(20, 40, 80, 20, 60)
pinout.set_label(110, 10, 30)
pinout.add_types(types)
pinout.set_label_af_height( 0, 0, 0 );
pinout.package_width = 300
pinout.pin_push_out_extra = 40
pinout.pin_no_offset = 54
pinout.add_pins(pins)
pinout.subtitle = "TSSOP20 4.4x6.5mm\n0.65mm Pitch"
pinout.footprint_text = "TSSP20"
pinout.add_mapping( pin_mapping )
pinout.is_diag = True

pinout.save()