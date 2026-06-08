def linear_interpolation(start, end, t):
    return start + (end - start) * t

def interpolate_color_linear(start_color, end_color, t):
    r = int(linear_interpolation(start_color[0], end_color[0], t))
    g = int(linear_interpolation(start_color[1], end_color[1], t))
    b = int(linear_interpolation(start_color[2], end_color[2], t))
    return (r, g, b)
