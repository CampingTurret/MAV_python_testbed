from classes import Base_Algorthm
from reader import Get_Image_dict
import cv2 as cv
import algortims
import pathlib
import numpy as np
import time
import platform


if __name__ == "__main__":
    f = open('Config.txt')
    for line in f.readlines():
        p, v = line.replace('\n','').split(':')
        if p == 'f1':
            f1 = v
        if p == 'f2':
            f2 = v
    if platform.system() == 'Windows':
        seperator = '\\'
    if platform.system() == 'Linux':
        seperator = '/'
    f.close()
    Images = Get_Image_dict()
    #f1 = "cyberzoo_poles_panels_mats" #cyberzoo_aggressive_flight
    #f2 = "20190121-142935"#20190121-144646
    res = {}
    ex_images: dict = Images[f"Images{seperator}{f1}"][f"Images{seperator}{f1}{seperator}{f2}"]
    I_len = len(ex_images)
    for sub in Base_Algorthm.__subclasses__():
        dt = time.time()
        cc = sub()
        for k,image in ex_images.items():
            if image == '.jpg':
                im = cv.imread(pathlib.Path(k).absolute())
                im = cv.transpose(im)
                im = cv.flip(im, 0)
                im = np.array(im)
                cc.execute(im)
        cc.gen_feed()
        res.update({str(cc.__class__):{'t1': dt, 't2':time.time()}})
    _dbaset = res["<class 'algortims.PASS_Baseline'>"]['t2'] - res["<class 'algortims.PASS_Baseline'>"]['t1']
    for key in res.keys():
        _dt = res[key]['t2'] - res[key]['t1'] 
        if key == "<class 'algortims.PASS_Baseline'>":
            _dt = _dbaset
        print(f"{key}: {(I_len)/_dt}")