import xlwings as xw
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


wb = xw.Book("rgb_data.xlsx")
sheet = wb.sheets['Sheet1']

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



data = sheet.range("A2:D101").value  


RGB = [] 
YUV = [] 
y = []

for row in data:
    if row and all(cell is not None for cell in row[:3]) and row[3] is not None:  # Ensure all RGB and label values are non-empty
        r, g, b = row[:3]
        RGB.append((int(r), int(g), int(b))) 
        YUV.append(rgb_to_yuv(int(r), int(g), int(b)))
        y.append(int(row[3]))  


targets = np.array(YUV)
labels = np.array(y)

wb.close()

fig_rgb = plt.figure()
ax_rgb = fig_rgb.add_subplot(111, projection='3d')
ax_rgb.set_title("RGB Values")
ax_rgb.set_xlabel("Red")
ax_rgb.set_ylabel("Green")
ax_rgb.set_zlabel("Blue")

for i, (r, g, b) in enumerate(RGB):
    color = 'green' if labels[i] == 255 else 'black'
    ax_rgb.scatter(r, g, b, color=color, s=20)

fig_yuv = plt.figure()
ax_yuv = fig_yuv.add_subplot(111, projection='3d')
ax_yuv.set_title("YUV Values")
ax_yuv.set_xlabel("Y")
ax_yuv.set_ylabel("U")
ax_yuv.set_zlabel("V")


for i, (y, u, v) in enumerate(YUV):
    color = 'green' if labels[i] == 255 else 'black'
    ax_yuv.scatter(y, u, v, color=color, s=20)


plt.show()


clf = DecisionTreeClassifier(max_depth=3) 
clf.fit(targets, labels)

print(clf.score(targets,labels))

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