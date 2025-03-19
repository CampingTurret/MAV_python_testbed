import xlwings as xw
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import json


wb = xw.Book("rgb_data.xlsx")
sheet = wb.sheets['Sheet1']


rgb_data = np.array(sheet.range("A2:C101").value)  
labels = np.array(sheet.range("D2:D101").value)

def clamp(value, min_value=0, max_value=255):
    return max(min_value, min(max_value, value))

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


wb.close()


targets = np.array([
    [80, 110, 90],
    [82, 112, 88],
    [78, 108, 92],
    [120, 130, 150],
    [122, 128, 148],
    [118, 132, 152],

])
labels= np.array([255, 255, 255, 0, 0, 0])


clf = DecisionTreeClassifier(max_depth=8) 
clf.fit(targets, labels)


tree = clf.tree_
tree_dict = {
    "feature": tree.feature.tolist(),         
    "threshold": tree.threshold.tolist(),
    "children_left": tree.children_left.tolist(),
    "children_right": tree.children_right.tolist(),
    "value": tree.value.tolist(),              
}

with open("tree.json", "w") as f:
    json.dump(tree_dict, f, indent=2)

print("Decision tree saved to tree.json")