from abc import ABC, abstractmethod
import cv2 as cv
import numpy as np
class Base_Algorthm(ABC):
    feed: list
    
    def __init__(self):
        self.feed = []
        self.org_feed = []
        self.writer = cv.VideoWriter()        
        super().__init__()
    
    @abstractmethod
    def execute(self, image):
        """Return image! and add to feed! Also add original to org_feed"""
        pass

    def gen_feed(self):
        name = str(self.__class__).split('.')[-1].replace("'>", '')
        cc = cv.VideoWriter_fourcc(*'mp4v')
        print(self.writer.open(f"{name}.MP4", cc, 4, (520, 480), True))
        for c, i in enumerate(self.feed):
            if not i.shape  == (240, 520, 3):
                print("Improper dimentions, matrix should be 240x520x3 for color horizontal video")
            
            comb = np.concatenate([i, self.org_feed[c]], axis=0)
            #if not self.writer.isOpened():
            #    print("closed")
            self.writer.write(comb)
            #print(self.writer.isOpened())
        self.writer.release()
        pass
