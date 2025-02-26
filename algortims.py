import classes
import numpy as np
from scipy.signal import convolve2d
import scipy.ndimage.filters

class EDGE(classes.Base_Algorthm):

    def __init__(self):
        super().__init__()
        

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)
        edges = np.zeros_like(image)
        blurred = np.zeros_like(image)
        gray =  np.zeros_like(image)
        k = np.array([[1, 4, 7, 4, 1],
                      [4, 16, 26, 16, 4],
                      [7, 26, 41, 26, 7],
                      [4, 16, 26, 16, 4],
                      [1, 4, 7, 4, 1]])
        horizontal = np.array([[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [-1,-1, 4,-1,-1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]])
        vertical = np.array([[0, 0, -1, 0, 0],
                      [0, 0, -1, 0, 0],
                      [0,0, 4,0,0],
                      [0, 0, -1, 0, 0],
                      [0, 0, -1, 0, 0]])
        

        for dim in range(np.shape(image)[2]):
            blurred[:,:, dim] = convolve2d(image[:,:, dim], k, mode='same', boundary='fill', fillvalue=0) // 273


        gray = (convolve2d(np.sum(blurred, axis=2), horizontal + vertical, mode='same', boundary='fill', fillvalue=0) // 3) / 255
        gray = np.where(gray > 0.05, 1, 0)
        for dim in range(np.shape(image)[2]):
            edges[:,:, dim] = gray*255# *blurred[:,:, dim]
        self.feed.append(edges)
        return edges
    
    def run_edge(image):
        pass



class GREEN_FLOOR(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)

        for dim in range(np.shape(image)[2]):
            if dim == 1:
                blue[:,:,dim] = np.where((np.where(image[:,:, dim] > 70, 1, 0) - np.where(image[:,:, 2] > 100, 1, 0)) > 0, 255, 0)

        self.feed.append(blue)
        return blue