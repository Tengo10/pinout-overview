import pinout as gen

pins = [
    [{"type": "pin", "name": "PD7", "alt": False},
     {"type": "spacer", "name":"", "alt": False},
     {"type": "sys", "name": "NRST", "alt": False},
     {"type": "tim2", "name":"CH4", "alt": False},
     {"type": "uart", "name":"CK", "alt": True},
     {"type": "opa", "name":"OPP1", "alt": False},
    ],
    [{"type": "pin", "name": "PA1", "alt": False},
     {"type": "adc", "name":"A1", "alt": False},
     {"type": "sys", "name": "OSCI", "alt": False},
     {"type": "tim1", "name":"CH2", "alt": False},
     {"type": "spacer", "name":"", "alt": False},
     {"type": "opa", "name":"OPN0", "alt": False},
    ],
    [{"type": "pin", "name": "PA2", "alt": False},
     {"type": "adc", "name":"A0", "alt": False},
     {"type": "sys", "name": "OSCO", "alt": False},
     {"type": "tim1", "name":"CH2N", "alt": False},
     {"type": "spacer", "name":"", "alt": False},
     {"type": "opa", "name":"OPP0", "alt": False},
     {"type": "adc", "name":"ETR2", "alt": False},
    ],
    [{"type": "vss", "name": "VSS", "alt": False},
    ],
    [{"type": "pin", "name": "PD0", "alt": False},
     {"type": "spacer", "name":"", "alt": False},
     {"type": "spacer", "name": "", "alt": False},
     {"type": "tim1", "name":"CH1N", "alt": False},
     {"type": "uart", "name":"TX", "alt": True},
     {"type": "opa", "name":"OPN1", "alt": False},
     {"type": "i2c", "name":"SDA", "alt": True},
    ],
    [{"type": "vdd", "name": "VDD", "alt": False},
    ],
    [{"type": "pin", "name": "PC0", "alt": False},
     {"type": "tim2", "name":"CH3", "alt": False},
     {"type": "uart", "name": "TX", "alt": True},
     {"type": "spi", "name":"NSS", "alt": True},
     {"type": "tim1", "name":"CH3", "alt": True},
    ],
    [{"type": "pin", "name": "PC1", "alt": False},
     {"type": "i2c", "name":"SDA", "alt": False},
     {"type": "tim1", "name": "BKIN", "alt": True},
     {"type": "spi", "name":"NSS", "alt": False},
     {"type": "uart", "name":"RX", "alt": True},
     {"type": "tim2", "name":"CH4", "alt": True},
     {"type": "tim2", "name":"CH1", "alt": True},
     {"type": "tim2", "name":"ETR", "alt": True},
     ],
]

types = {
    "pin": {
        "borderColor": "black",
        "backgroundColor": "grey",
        "textColor": "white"
    },
    "i2c": {
        "borderColor": "#00B8CC",
        "backgroundColor": "#88EBF7",
        "textColor": "black"
    },
    "tim1": {
        "borderColor": "#00CCA0",
        "backgroundColor": "#99FFE9",
        "textColor": "black"
    },
    "tim2": {
        "borderColor": "#69CC00",
        "backgroundColor": "#DAFFB3",
        "textColor": "black"
    },
    "adc": {
        "borderColor": "#0060CD",
        "backgroundColor": "#A2CEFF",
        "textColor": "black"
    },
    "sys": {
        "borderColor": "#9600CC",
        "backgroundColor": "#E399FF",
        "textColor": "black"
    },
    "uart": {
        "borderColor": "#CC0092",
        "backgroundColor": "#FFA3E5",
        "textColor": "black"
    },
    "spi": {
        "borderColor": "#00CC5F",
        "backgroundColor": "#8CEEBA",
        "textColor": "black"
    },
    "opa": {
        "borderColor": "#CCAA00",
        "backgroundColor": "#FFE97C",
        "textColor": "black"
    },
    "vss": {
        "borderColor": "black",
        "backgroundColor": "black",
        "textColor": "white"
    },
    "vdd": {
        "borderColor": "red",
        "backgroundColor": "red",
        "textColor": "white"
    },
}

pinout = gen.Package("QFN-20", "QFN")
pinout.set_footprint(20, 40, 30, 20, 60)
pinout.set_label(80, 10, 30)
pinout.add_types(types)
pinout.add_pins(pins)

pinout.save()