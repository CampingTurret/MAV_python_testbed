import classes
import numpy as np
from scipy.signal import convolve2d
import scipy.ndimage.filters
import cv2 as cv

R = 200
G = 100
B = 100

EDGE_on = False
if(EDGE_on):
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

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    


        self.feed.append(blue)
        return blue
    
    def Floor_Fit(self, mat):
        pass

class GREEN_FLOOR_Fit_houghP(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    
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
        geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)


        lines = cv.HoughLinesP(geen_edges[:,:,1], 0.5 , np.pi * 0.2, 10, minLineLength=100, maxLineGap=10)
        
        if lines is not None:
            for i in range(0, len(lines)):
                l = lines[i][0]
                cv.line(geen_lines,(l[0], l[1]), (l[2], l[3]), (0,255,0))

        self.feed.append(geen_lines)
        return geen_lines
    
    def Floor_Fit(self, mat):
        pass

class GREEN_FLOOR_Fit_ContourCV(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    
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
        geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

        contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        try:
            largest_contour = max(contours, key=cv.contourArea)
            cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
        except:
            pass

        self.feed.append(geen_lines)
        return geen_lines
    
class GREEN_FLOOR_Fit_ContourCV_SimpleControl_multiview(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)
        LEFT = False
        RIGHT = False
        SPIN = False

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    
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
        geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

        contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        new_contours = []
        for contour in contours:
            if np.any(contour[:, 0, 1] == 239):
                new_contours.append(contour)
        cv.drawContours(geen_lines, new_contours, -1, (0, 255, 0), thickness=cv.FILLED)


        vert_check = np.sum(geen_lines[:,:,1], 0)
        hort_check = geen_lines[-1,:,1]
        geen_lines[-10,:,0] = np.where(hort_check,255, 0)
        geen_lines[-50,:,0] = np.where(vert_check,255, 0)
        geen_lines[:,:,2] = np.where(vert_check,0, 255)
        if sum(hort_check)//255 < 30:
            geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
            SPIN = True

        
        sh = np.shape(geen_lines)
        middle = (sh[0]//2 -1, sh[1]//2 -1)
        middle_cv = (middle[-1], middle[0])
        _slice =  int(sh[1]*0.1/2)
        if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
            if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
                RIGHT = True
            else:
                LEFT = True

        if SPIN:
            cv.putText(geen_lines, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif LEFT:
            cv.putText(geen_lines, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif RIGHT:
            cv.putText(geen_lines, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
        self.feed.append(geen_lines)
        return geen_lines
    
class GREEN_FLOOR_Fit_ContourCV_SimpleControl_soloview(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)
        LEFT = False
        RIGHT = False
        SPIN = False

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    
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
        geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

        contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        try:
            largest_contour = max(contours, key=cv.contourArea)
            cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
        except:
            pass


        vert_check = np.sum(geen_lines[:,:,1], 0)
        hort_check = geen_lines[-1,:,1]
        geen_lines[-10,:,0] = np.where(hort_check,255, 0)
        geen_lines[-50,:,0] = np.where(vert_check,255, 0)
        geen_lines[:,:,2] = np.where(vert_check,0, 255)
        if sum(hort_check)//255 < 30:
            geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
            SPIN = True
        
        sh = np.shape(geen_lines)
        middle = (sh[0]//2 -1, sh[1]//2 -1)
        middle_cv = (middle[-1], middle[0])
        _slice =  int(sh[1]*0.1/2)
        if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
            if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
                RIGHT = True
            else:
                LEFT = True

        if SPIN:
            cv.putText(geen_lines, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif LEFT:
            cv.putText(geen_lines, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif RIGHT:
            cv.putText(geen_lines, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
        self.feed.append(geen_lines)
        return geen_lines
    
class PASS_Baseline(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)
        self.feed.append(image)
        return image
    
class GREEN_FLOOR_Fit_ContourCV_SimpleControl_soloview_Hidden(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)
        out = np.zeros_like(image)
        LEFT = False
        RIGHT = False
        SPIN = False

        cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
        blue[:,:,1] = np.where(cond, 255, 0)    
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
        geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

        contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        try:
            largest_contour = max(contours, key=cv.contourArea)
            cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
        except:
            pass

        vert_check = np.sum(geen_lines[:,:,1], 0)
        hort_check = geen_lines[-1,:,1]
        geen_lines[-10,:,0] = np.where(hort_check,255, 0)
        geen_lines[-50,:,0] = np.where(vert_check,255, 0)
        geen_lines[:,:,2] = np.where(vert_check,0, 255)
        out[:,:,2]  = np.where(vert_check,0, 255)
        if sum(hort_check)//255 < 30:
            geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
            out[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
            SPIN = True
        
        sh = np.shape(geen_lines)
        middle = (sh[0]//2 -1, sh[1]//2 -1)
        middle_cv = (middle[-1], middle[0])
        _slice =  int(sh[1]*0.1/2)
        if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
            if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
                RIGHT = True
            else:
                LEFT = True

        if SPIN:
            cv.putText(out, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif LEFT:
            cv.putText(out, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif RIGHT:
            cv.putText(out, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
        self.feed.append(out)
        return out