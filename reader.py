import cv2
import os
import pathlib
import read_func

def Get_Image_dict() -> dict:
    Image_dir_local = pathlib.Path('./Images')
    Image_dict = {}
    read_func.Build_dict(Image_dir_local, Image_dict)
    return Image_dict

