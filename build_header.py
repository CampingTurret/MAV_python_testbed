import json

# --- Helper function to traverse the tree ---
def traverse_tree(tree, node_idx, y, u, v):
    node = {
        "feature": tree["feature"][node_idx],
        "threshold": tree["threshold"][node_idx],
        "left": tree["children_left"][node_idx],
        "right": tree["children_right"][node_idx],
        "value": tree["value"][node_idx],
    }
    
    # If it's a leaf node, return the classification
    if node["feature"] == -2:  # Leaf node
        return 255 if node["value"][0][1] > node["value"][0][0] else 0

    # Get the feature value (Y, U, V)
    feature_value = [y, u, v][node["feature"]]
    
    # Traverse left or right child based on the threshold
    if feature_value <= node["threshold"]:
        return traverse_tree(tree, node["left"], y, u, v)
    else:
        return traverse_tree(tree, node["right"], y, u, v)

# --- Load the JSON file ---
with open("tree.json", "r") as f:
    tree = json.load(f)

# --- Generate the Lookup Table ---
lut_size = 256
lookup_table = [[[0 for _ in range(lut_size)] for _ in range(lut_size)] for _ in range(lut_size)]

for y in range(lut_size):
    for u in range(lut_size):
        for v in range(lut_size):
            lookup_table[y][u][v] = traverse_tree(tree, 0, y, u, v)

# --- Write the Table to a C Header File ---
with open("lookup_table.h", "w") as f:
    f.write("/* Auto-generated lookup table */\n")
    f.write("const unsigned char lookup_table[256][256][256] = {\n")
    for y in range(lut_size):
        f.write(f"  {{ /* Y = {y} */\n")
        for u in range(lut_size):
            f.write("    {")
            f.write(", ".join(str(lookup_table[y][u][v]) for v in range(lut_size)))
            f.write("}" + (",\n" if u < lut_size - 1 else "\n"))
        f.write("  }" + (",\n" if y < lut_size - 1 else "\n"))
    f.write("};\n")
