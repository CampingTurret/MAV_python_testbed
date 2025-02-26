import os 
import pathlib


def Build_dict(Image_dir: pathlib.Path, dict:dict) -> dict:
    for f in os.listdir(Image_dir):
        p = Image_dir/f
        if (os.path.isfile(p)):
            if len(p.suffixes) > 0:
                suffix = p.suffixes[0]
            else:
                suffix = ''
            dict.update({str(p):suffix})
        else:
            _2nd_dict = {}
            dict.update({str(p):_2nd_dict})

            Build_dict(p, _2nd_dict)
    return dict