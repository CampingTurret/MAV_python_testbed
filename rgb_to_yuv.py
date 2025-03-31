import numpy as np


R = 170
G = 162
B= 115

def clamp(value, min_value=0, max_value=255):
    return np.maximum(min_value, np.minimum(max_value, value))

def rgb_to_yuv(r, g, b):
    
    vc = 1.402
    uc = 1.772
    yc1 = 0.34414
    yc2 = 0.71414


    D = yc1/uc
    E = yc2/vc

    y = clamp(int((g+D*b+E*r)/(1+D+E)))

    v = clamp(int((r-y)/vc + 128))
    u = clamp(int((b-y)/uc + 128))

    return y, u ,v

print(rgb_to_yuv(R,G,B))