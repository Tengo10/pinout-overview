import drawsvg as dw

def sop_border(width, height, **kwargs):
    """
    Draw SOP border, additional args passed to drawsvg
    """
    border = dw.Rectangle(-width/2, -height/2, width, height, **kwargs)
    return border

def sop_pin(width, length, **kwargs):
    """
    Draw SOP pin, additional args passed to drawsvg
    """
    pin = dw.Path(**kwargs)
    pin.M(-length/2,-width/2)
    pin.H(length/2)
    pin.V(width/2)
    pin.H(-length/2)
    pin.V(-width/2)
    pin.M(-length/6, -width/2)
    pin.V(width/2)
    pin.M(length/6, -width/2)
    pin.V(width/2)
    pin.Z()
    return pin

def qfn_border(width, **kwargs):
    """
    Draw SOP border, additional args passed to drawsvg
    """
    border = dw.Rectangle(-width/2, -width/2, width, width, **kwargs)
    return border

def qfn_pin(width, length, **kwargs):
    """
    Draw QFN pin, additional args passed to drawsvg
    """
    pin = dw.Rectangle(-length/2, -width/2, length, width, **kwargs)
    return pin

def qfn_pad(width, **kwargs):
    pad = dw.Path(**kwargs)
    pad.M(-width/2+width/5, -width/2)
    pad.H(width/2)
    pad.V(width/2)
    pad.H(-width/2)
    pad.V(-width/2+width/5)
    pad.Z()
    return pad

def label_box(width, height, **kwargs):
    """
    Draw label box, additional args passed to drawsvg
    """
    box = dw.Rectangle(-width/2, -height/2, width, height, **kwargs)
    return box

def label_text(name, height, **kwargs):
    """
    Draw label text, additional args passed to drawsvg
    """
    x_offset = 0
    if "font_style" in kwargs and kwargs["font_style"] == "italic":
        x_offset = height/10
        
    text = dw.Text(name, height-height/5, -x_offset, height/10, **kwargs)
    return text

def label_line(op, extentXmax, extentXmin, **kwargs):
    """
    Draw label line, additional args passed to drawsvg
    """
    dw_label_line = dw.Path(**kwargs)
    dw_label_line.M(op.start_x, op.start_y)
    dw_label_line.H(op.start_x-extentXmin)
    dw_label_line.V(op.end_y)
    dw_label_line.H(op.end_x+extentXmax)
    return dw_label_line
