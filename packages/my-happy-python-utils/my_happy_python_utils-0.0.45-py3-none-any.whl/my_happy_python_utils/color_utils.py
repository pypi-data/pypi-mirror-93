import random
import numpy as np
import colorsys

from . import version

__version__ = version.get_current()


def generate_different_colors(opt={}):
    num_colors = opt.get('num_colors', 5)

    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i / 360.
        lightness = (50 + np.random.rand() * 10) / 100.
        saturation = (90 + np.random.rand() * 10) / 100.
        _r, _g, _b = colorsys.hls_to_rgb(hue, lightness, saturation)
        r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
        r_hex = hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]

        colors.append('#' + r_hex + g_hex + b_hex)

    return colors
