
# Pinout Generator

A very work in progress pinout diagram generator using Python and drawsvg

# Usage

## Config Files

Configuration can be split across multiple config files to allow for sharing of common properties
> "_style" fields are standard SVG properties like fill, font_family, etc.

#### Define types

``` yaml
types:
    pin:
        width: 80
        description: PIN NAME
        box_style:
            stroke: black
            fill: grey
        text_style:
            font_family: Roboto Mono
            fill: white
    ...
```

#### Define pin functions

``` yaml
pins:
    PIN1:
        - type: pin
            name: PD7
            alt: False
        - type: spacer
    ...
```

#### Map Pins to physical output on IC

``` yaml
mapping: [PIN1, PIN2, ...]
```

#### Styling

See the default files for further reference

``` yaml
pin: !include ../defaults/pin_qfn.yaml
label: !include ../defaults/label_qfn.yaml
package: !include ../defaults/package_qfn.yaml
```

#### Chip options

``` yaml
footprint: QFN-20 #Footprint-PinNumber
name: "IC NAME" 
subtitle: "SUBTITLE"
package_text:
  text: "ON PACKAGE TEXT"
  sub_text: "ON PACKAGE SUBTEXT"
canvas_width: 2000
canvas_height: 1000
```

## Generating the Images

To generate a single Image

``` shell
 py pinout.py [yaml file] [output file]
```

To generate a whole directory, first characters of yaml files should match directory name.
SVGs will be saved in the directory

``` shell
 py generate_dir.py [yaml dir]
```

# TODO

- [ ] Error checking
- [x] Documentation
- [ ] Improve SVG generation
- [ ] Add different styling options
- [ ] Added YAML functionality like Homeassistant and ESPHome has
- [ ] Improve modularity to allow for more complex footprints
- [ ] Clean up a lot of bad programming and improve readability 
- [x] Use config files and cli
