import classes
import numpy as np
from scipy.signal import convolve2d
import scipy.ndimage.filters
import cv2 as cv

R = 200
G = 100
B = 100

def clamp(value, min_value=0, max_value=255):
    return np.maximum(min_value, np.minimum(max_value, value))

def rgb_to_yuv(r, g, b):
    
    vc = 1.402
    uc = 1.772
    yc1 = 0.34414
    yc2 = 0.71414


    D = yc1/uc
    E = yc2/vc

    y = clamp(((g+D*b+E*r)/(1+D+E)).astype(int))

    v = clamp(((r-y)/vc + 128).astype(int))
    u = clamp(((b-y)/uc + 128).astype(int))

    return y, u ,v

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



# class GREEN_FLOOR(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    


#         self.feed.append(blue)
#         return blue
    
#     def Floor_Fit(self, mat):
#         pass

# class GREEN_FLOOR_Fit_houghP(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)
#         geen_edges = np.zeros_like(image)
#         geen_lines = np.zeros_like(image)

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    
#         horizontal = np.array([[0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0],
#                       [-1,-1, 4,-1,-1],
#                       [0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0]])
#         vertical = np.array([[0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0],
#                       [0,0, 4,0,0],
#                       [0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0]])
#         geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)


#         lines = cv.HoughLinesP(geen_edges[:,:,1], 0.5 , np.pi * 0.2, 10, minLineLength=100, maxLineGap=10)
        
#         if lines is not None:
#             for i in range(0, len(lines)):
#                 l = lines[i][0]
#                 cv.line(geen_lines,(l[0], l[1]), (l[2], l[3]), (0,255,0))

#         self.feed.append(geen_lines)
#         return geen_lines
    
#     def Floor_Fit(self, mat):
#         pass

# class GREEN_FLOOR_Fit_ContourCV(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)
#         geen_edges = np.zeros_like(image)
#         geen_lines = np.zeros_like(image)

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    
#         horizontal = np.array([[0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0],
#                       [-1,-1, 4,-1,-1],
#                       [0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0]])
#         vertical = np.array([[0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0],
#                       [0,0, 4,0,0],
#                       [0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0]])
#         geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

#         contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         try:
#             largest_contour = max(contours, key=cv.contourArea)
#             cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
#         except:
#             pass

#         self.feed.append(geen_lines)
#         return geen_lines
    
# class GREEN_FLOOR_Fit_ContourCV_SimpleControl_multiview(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)
#         geen_edges = np.zeros_like(image)
#         geen_lines = np.zeros_like(image)
#         LEFT = False
#         RIGHT = False
#         SPIN = False

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    
#         horizontal = np.array([[0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0],
#                       [-1,-1, 4,-1,-1],
#                       [0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0]])
#         vertical = np.array([[0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0],
#                       [0,0, 4,0,0],
#                       [0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0]])
#         geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

#         contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         new_contours = []
#         for contour in contours:
#             if np.any(contour[:, 0, 1] == 239):
#                 new_contours.append(contour)
#         cv.drawContours(geen_lines, new_contours, -1, (0, 255, 0), thickness=cv.FILLED)


#         vert_check = np.sum(geen_lines[:,:,1], 0)
#         hort_check = geen_lines[-1,:,1]
#         geen_lines[-10,:,0] = np.where(hort_check,255, 0)
#         geen_lines[-50,:,0] = np.where(vert_check,255, 0)
#         geen_lines[:,:,2] = np.where(vert_check,0, 255)
#         if sum(hort_check)//255 < 30:
#             geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
#             SPIN = True

        
#         sh = np.shape(geen_lines)
#         middle = (sh[0]//2 -1, sh[1]//2 -1)
#         middle_cv = (middle[-1], middle[0])
#         _slice =  int(sh[1]*0.1/2)
#         if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
#             if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
#                 RIGHT = True
#             else:
#                 LEFT = True

#         if SPIN:
#             cv.putText(geen_lines, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif LEFT:
#             cv.putText(geen_lines, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif RIGHT:
#             cv.putText(geen_lines, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
#         self.feed.append(geen_lines)
#         return geen_lines
    
# class GREEN_FLOOR_Fit_ContourCV_SimpleControl_soloview(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)
#         geen_edges = np.zeros_like(image)
#         geen_lines = np.zeros_like(image)
#         LEFT = False
#         RIGHT = False
#         SPIN = False

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    
#         horizontal = np.array([[0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0],
#                       [-1,-1, 4,-1,-1],
#                       [0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0]])
#         vertical = np.array([[0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0],
#                       [0,0, 4,0,0],
#                       [0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0]])
#         geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

#         contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         try:
#             largest_contour = max(contours, key=cv.contourArea)
#             cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
#         except:
#             pass


#         vert_check = np.sum(geen_lines[:,:,1], 0)
#         hort_check = geen_lines[-1,:,1]
#         geen_lines[-10,:,0] = np.where(hort_check,255, 0)
#         geen_lines[-50,:,0] = np.where(vert_check,255, 0)
#         geen_lines[:,:,2] = np.where(vert_check,0, 255)
#         if sum(hort_check)//255 < 30:
#             geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
#             SPIN = True
        
#         sh = np.shape(geen_lines)
#         middle = (sh[0]//2 -1, sh[1]//2 -1)
#         middle_cv = (middle[-1], middle[0])
#         _slice =  int(sh[1]*0.1/2)
#         if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
#             if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
#                 RIGHT = True
#             else:
#                 LEFT = True

#         if SPIN:
#             cv.putText(geen_lines, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif LEFT:
#             cv.putText(geen_lines, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif RIGHT:
#             cv.putText(geen_lines, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
#         self.feed.append(geen_lines)
#         return geen_lines
    
class PASS_Baseline(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)
        self.feed.append(image)
        return image
    
# class GREEN_FLOOR_Fit_ContourCV_SimpleControl_soloview_Hidden(classes.Base_Algorthm):
#     def __init__(self):
#         super().__init__()

#     def execute(self, image):
#         """Return image! and add to feed!"""
#         self.org_feed.append(image)

#         blue = np.zeros_like(image)
#         geen_edges = np.zeros_like(image)
#         geen_lines = np.zeros_like(image)
#         out = np.zeros_like(image)
#         LEFT = False
#         RIGHT = False
#         SPIN = False

#         cond = np.logical_and(np.logical_and(image[:,:, 1] > G, image[:,:, 2] < R),image[:,:, 0] < B)
#         blue[:,:,1] = np.where(cond, 255, 0)    
#         horizontal = np.array([[0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0],
#                       [-1,-1, 4,-1,-1],
#                       [0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0]])
#         vertical = np.array([[0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0],
#                       [0,0, 4,0,0],
#                       [0, 0, -1, 0, 0],
#                       [0, 0, -1, 0, 0]])
#         geen_edges[:,:,1] = convolve2d(blue[:,:,1], horizontal + vertical, mode='same', boundary='fill', fillvalue=0)

#         contours, _ = cv.findContours(geen_edges[:,:,1], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         try:
#             largest_contour = max(contours, key=cv.contourArea)
#             cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
#         except:
#             pass

#         vert_check = np.sum(geen_lines[:,:,1], 0)
#         hort_check = geen_lines[-1,:,1]
#         geen_lines[-10,:,0] = np.where(hort_check,255, 0)
#         geen_lines[-50,:,0] = np.where(vert_check,255, 0)
#         geen_lines[:,:,2] = np.where(vert_check,0, 255)
#         out[:,:,2]  = np.where(vert_check,0, 255)
#         if sum(hort_check)//255 < 30:
#             geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
#             out[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
#             SPIN = True
        
#         sh = np.shape(geen_lines)
#         middle = (sh[0]//2 -1, sh[1]//2 -1)
#         middle_cv = (middle[-1], middle[0])
#         _slice =  int(sh[1]*0.1/2)
#         if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
#             if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
#                 RIGHT = True
#             else:
#                 LEFT = True

#         if SPIN:
#             cv.putText(out, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif LEFT:
#             cv.putText(out, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
#         elif RIGHT:
#             cv.putText(out, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
#         self.feed.append(out)
#         return out
    

class GREEN_FLOOR_Fit_ContourCV_SimpleControl_yuv(classes.Base_Algorthm):
    def __init__(self):
        super().__init__()

    def execute(self, image):
        """Return image! and add to feed!"""
        self.org_feed.append(image)

        blue = np.zeros_like(image)
        geen_edges = np.zeros_like(image)
        geen_lines = np.zeros_like(image)
        new_image = np.zeros_like(image)
        LEFT = False
        RIGHT = False
        SPIN = False
        new_image[:,:, 0], new_image[:,:, 1], new_image[:,:, 2] = rgb_to_yuv(image[:,:, 2], image[:,:, 1], image[:,:, 0])
        cond = np.logical_and(np.logical_and(new_image[:,:, 0] < 196, new_image[:,:, 1] < 114),new_image[:,:, 2] < 140)
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
        
        #maybe drop upper quarter/half of image at the beginning?
        if contours:
            #check whether if needed here later
            largest_contour = max(contours, key=cv.contourArea)
            contour_x = largest_contour[:, 0, 0]
            contour_y = largest_contour[:, 0, 1]

            last_row_y = np.max(contour_y)  #note this is last line of contour, not bottom most row of image!
            last_row_x = contour_x[contour_y == last_row_y]  

            
            min_x_last_row = np.min(last_row_x)
            max_x_last_row = np.max(last_row_x)

            if ((max_x_last_row - min_x_last_row)<30): #just replicating flood_fill code with coordinates for now.
                SPIN = True
            
            
            #if red in center # does it need to be checked? why not spin regardless? (does it skip calculations?)
            last_row = geen_lines[-1]  # Last row. 

            middle = last_row.shape[0] // 2 #replace by constant if image size fixed (test with that) 
            middle_cv = (middle, middle)
            sh = np.shape(geen_lines)
            _slice =  int(sh[1]*0.1/2)
            #_slice = 20  # Define the size of the slice around the center (e.g., 20 pixels)

            red_in_center = np.sum(last_row[middle-_slice:middle+_slice, 2]) > 0 #todo : stop summing if single red pixel found in a while loop
            if red_in_center:
                
                # why is this in last row? if contour row is not last row of image, will green be present in last row? i dont think so.
                # green check for turns, probably should be based on min and max_x_last_row (last row in flood_fill is based on that right?) 
                if ((middle - min_x_last_row) < (max_x_last_row - middle)): 
                    # 1. is either min or max sufficient? 
                    # 2. is  computation cost of comparision and subtraction equal? (equation can be rewritten)
                    RIGHT= True #right or left here?
                else:
                    LEFT = True
                ######################################################################
                # Extract the last row from the image
                #last_row = geen_lines[-1, :, 1] 

                # last_row_x = np.where(last_row > 0)[0]  # Indices of non-zero pixels in the last row

                # # Find min and max x-coordinates of green pixels in the last row
                # if len(last_row_x) > 0:  # Check if there are any green pixels in the last row
                #     min_x_last_row = np.min(last_row_x)
                #     max_x_last_row = np.max(last_row_x)
                # else:
                #     min_x_last_row = max_x_last_row = None  
                ######################################################################

        #####################################################
        #Original floor detect code for reference
        # try:
        #     largest_contour = max(contours, key=cv.contourArea)
        #     cv.drawContours(geen_lines, [largest_contour], -1, (0, 255, 0), thickness=cv.FILLED)
        # except:
        #     pass


        # vert_check = np.sum(geen_lines[:,:,1], 0)
        # hort_check = geen_lines[-1,:,1]
        # geen_lines[-10,:,0] = np.where(hort_check,255, 0)
        # geen_lines[-50,:,0] = np.where(vert_check,255, 0)
        # geen_lines[:,:,2] = np.where(vert_check,0, 255)
        # if sum(hort_check)//255 < 30:
        #     geen_lines[:,:,0] = np.where(geen_lines[-1,:,2],0, 255)
        #     SPIN = True
        
        # sh = np.shape(geen_lines)
        # middle = (sh[0]//2 -1, sh[1]//2 -1)
        # middle_cv = (middle[-1], middle[0])
        # _slice =  int(sh[1]*0.1/2)
        # if sum(geen_lines[-1,(middle[1]-_slice):(middle[1]+_slice),2])//255 > 0:
        #     if sum(geen_lines[-1,(middle[1]-_slice):,1]) > sum(geen_lines[-1,:(middle[1]+_slice),1]):
        #         RIGHT = True
        #     else:
        #         LEFT = True
        #######################################################
        if SPIN:
            cv.putText(geen_lines, "SPIN", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif LEFT:
            cv.putText(geen_lines, "Left", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3) 
        elif RIGHT:
            cv.putText(geen_lines, "Right", middle_cv, cv.FONT_HERSHEY_PLAIN, 5, (255,255,255), thickness=3)    
        self.feed.append(geen_lines)
        return geen_lines