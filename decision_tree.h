/* Auto-generated Decision Tree */
#ifndef DECISION_TREE_H
#define DECISION_TREE_H

typedef struct {
    int feature;         
    float threshold;    
    int left;            
    int right;           
    unsigned char value; 
} Node;

const Node decision_tree[] = {
    { 1, 113.5, 1, 12, 0 },
    { 2, 140.5, 2, 7, 0 },
    { 0, 195.5, 3, 6, 0 },
    { 1, 90.5, 4, 5, 0 },
    { -2, -2.0, -1, -1, 255 },
    { -2, -2.0, -1, -1, 255 },
    { -2, -2.0, -1, -1, 0 },
    { 1, 81.0, 8, 11, 0 },
    { 0, 124.5, 9, 10, 0 },
    { -2, -2.0, -1, -1, 255 },
    { -2, -2.0, -1, -1, 0 },
    { -2, -2.0, -1, -1, 0 },
    { -2, -2.0, -1, -1, 0 },
};

#define NUM_NODES (sizeof(decision_tree) / sizeof(decision_tree[0]))
#endif // DECISION_TREE_H
