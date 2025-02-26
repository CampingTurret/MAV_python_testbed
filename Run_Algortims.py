from classes import Base_Algorthm
from reader import Get_Image_dict
import cv2 as cv
import algortims
import pathlib
import numpy as np

if __name__ == "__main__":
    Images = Get_Image_dict()
    f1 = "cyberzoo_poles_panels_mats" #cyberzoo_aggressive_flight
    f2 = "20190121-142935"#20190121-144646
    ex_images: dict = Images[f"Images\\{f1}"][f"Images\\{f1}\\{f2}"]
    for sub in Base_Algorthm.__subclasses__():
        cc = sub()
        for k,image in ex_images.items():
            if image == '.jpg':
                im = cv.imread(pathlib.Path(k).absolute())
                im = cv.transpose(im)
                im = cv.flip(im, 0)

                im = np.array(im)
                cc.execute(im)
        cc.gen_feed()