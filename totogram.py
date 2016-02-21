import copy
import random
import math

'''
    REPORT
    ======
    Our algorithm always returns the best possible value possible when the root node is the mid element.
    we always assume that we can get the best value when the mid element is the root.

    We observed that our algorithm is much efficient then random search,local search and other such methods

    We guess the best score for depth k is int(math.ceil((3*2**(k-2) - 1) / float(k -1)))
    Its based on the assumption that root node = n/2 where n is the total number of elements

    Using this best score as base, we construct a tree conforming to this score.
   
    RESULTS
    =======
    We got the following results

    for k = 3:
    the best score is 3
    the tree is below:
    5 2 6 8 1 3 4 7 9 10
    total time used: 0.000286102294922
    ============================
    for k = 4:
    the best score is 4
    the tree is below:
    11 7 12 15 3 4 10 16 18 19 1 2 5 6 8 9 13 14 17 20 21 22
    total time used: 0.000742197036743
    ============================
    for k = 5:
    the best score is 6
    the tree is below:
    23 17 24 29 11 12 22 30 34 35 5 6 7 10 16 19 27 32 37 39 40 41 1 2 3 4 8 9 13 14 15 18 20 21 25 26 28 31 33 36 38 42 43 44 45 46
    total time used: 0.00163006782532
    ============================
    for k = 6:
    the best score is 10
    the tree is below:
    47 37 48 57 27 28 46 58 66 67 17 18 19 22 36 39 55 64 73 75 76 77 7 8 9 10 13 16 23 26 31 34 40 43 51 54 60 63 69 72 79 82 84 85 86 87 1 2 3 4 5 6 11 12 14 15 20 21 24 25 29 30 32 33 35 38 41 42 44 45 49 50 52 53 56 59 61 62 65 68 70 71 74 78 80 81 83 88 89 90 91 92 93 94
    total time used: 0.00366902351379
    ============================
    for k = 7:
    the best score is 16
    the tree is below:
    95 79 96 111 63 64 94 112 125 126 47 48 49 50 78 80 113 128 139 140 141 142 31 32 33 34 35 36 43 54 62 70 77 87 103 110 120 130 137 148 153 154 155 156 157 158 15 16 17 18 19 20 21 22 25 28 37 40 44 51 55 58 61 67 71 74 81 84 88 91 99 102 106 109 116 119 123 129 133 136 144 147 151 160 163 166 167 168 169 170 171 172 173 174 1 2 3 4 5 6 7 8 9 10 11 12 13 14 23 24 26 27 29 30 38 39 41 42 45 46 52 53 56 57 59 60 65 66 68 69 72 73 75 76 82 83 85 86 89 90 92 93 97 98 100 101 104 105 107 108 114 115 117 118 121 122 124 127 131 132 134 135 138 143 145 146 149 150 152 159 161 162 164 165 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190
    total time used: 0.00920820236206
    ============================
    


    ALGORITHM    
    =========

    First we store the entire set of elements for the possible depth in an array
        [1,2,3,....n]

    now we remove the mid element n/2 from the array.

    Now the the total number of elements = (n-1) is perfectly divisible by 3.

    We divide this array into 3 arrays left_array,mid_array,right_array of equal length (n-1)/2

    now we calculate cost = int(math.ceil((3*2**(k-2) - 1) / float(k -1)))

    now we select left,mid and right childs of the root based on the assumption 

    leftroot = root-cost       [it should be in left_array else perform swap]
    rightroot = root+cost      [it should be in right_array else perform swap]
    midroot = mid element of mid array

    If the children are not present in the respective arrays, we swap nodes from mid_array 
    such that these children are inserted into their respective arrays.

                                            root
                                          //  |  \\
                                       //     |     \\ 
                                    //        |       \\
                                  //          |         \\
                            LEFT TREE     MID TREE      RIGHT TREE

   LEFT TREE
    We perform LL preorder depth first traversal to create left tree 
    during preorder to add 
                        left_node :-
                            element = current_node-cost
                            if  element < left_array[0]:
                            then element =left_array.pop(0)

                        right_node :-
                            element= left_node+1
                            if element not in left_array
                            then element = left_array.pop(0)

                                    LEFT TREE[left_array]
                                        |
                                        |
                                    leftroot(root-cost)
                                    /                 \
                                   /                   \
                                  /                     \
                            left_node                   right_node
                        (leftroot-cost)                 (left_node+1)
                              / \                          /        \
                             /   \                        /          \
                            /     \                      /            \
                left_node-cost   left_node-cost+1  right_node-cost  right_node-cost+1
                     or             or                   or             or
                left_array(0)    left_array(0)      left_array(0)      left_array(0) 

    RIGHT TREE
    We perform RR preorder depth first traversal to create right tree
    during preorder to add 
                     right_node :-
                        element = current_node+cost
                        if  element > right_array[]:
                        then element =right_array.pop()

                     right_node :-
                        element= right_node-1
                        if element not in right_array
                        then element = right_array.pop()
    
                                    RIGHT TREE[right_array]
                                        |
                                        |
                                    rightroot(root+cost)
                                    /                 \
                                   /                   \
                                  /                     \
                            left_node                   right_node
                        (right_node-1)                 (right_node+cost)
                              / \                          /        \
                             /   \                        /          \
                            /     \                      /            \
                left_node+cost-1  left_node+cost  right_node+cost-1  right_node+cost
                     or              or                 or               or
                right_array(-1)   right_array(-1)  right_array(-1)    right_array(-1) 

    MID TREE
    
    Now we divide the mid array into two equal parts and create two sub trees
    1.) we perform LL preorder depth first traversal(same as LEFT TREE ) on the left subtree of the mid tree
    2.) we perform RR preorder depth first traversal on the right subtree(same as RIGHT TREE) of the mid tree
    
    3.)Now we combine these two subtrees to create the mid tree with midchild as the node_root


    Now we combine all the three trees under root node to form the Totogram 

                                    MID TREE mid_array = {start,....midchild,....end}
                                        |
                                        |
                                     midchild
                                     /      \
        LEFT TREE{start,...,midchild-1}    RIGHT TREE{midchild+1,...,end}      

'''

class Node(object):    #class used to define properties of nodes in Totogram
    def __init__(self, number):
   
        self.number = number
        self.left = self.mid = self.right = None
        self.depth = 1

    def switch(self, node):
        self.number, node.number = node.number, self.number

    def get_children(self):
        return filter(None, [self.left, self.mid, self.right])

    def has_children(self):
        return self.left != None or self.mid != None \
                                or self.right != None

    def bfs(self):
        yield [self]
        child_node = self.get_children()
        while len(child_node) != 0:
            yield child_node
            child_node = reduce(lambda x,y:x+y, 
                                [ch.get_children() for ch in child_node])
    def all_nodes(self):
        return reduce(lambda x, y: x+y, self.bfs())

    def zip_children(self):
        return [(self, _) for _ in self.get_children()]

    def score_node(self, node):
        return abs(self.number - node.number)

    def tree_score(self):
        max_value = (-1, None)
        for nodes in self.bfs():
            for node in nodes:
                zip_children = node.zip_children()
                if len(zip_children) == 0:
                    continue
                temp = max(zip_children, 
                        key=lambda x: x[0].score_node(x[1]))
                temp_value = temp[0].score_node(temp[1])
                if temp_value > max_value[0]:
                    max_value = (temp_value, temp)
        return max_value

    def __str__(self):
        # return "Node:%s"%str(self.number)
        return str(self.number)

    def display(self):
        for nodes in self.bfs():
            print ",".join(map(str, nodes))

    def copy(self):
        return copy.deepcopy(self)

def construct_in_strategy(k):
    n = 3*2**(k-1) - 2
    # print "total:%s"%n
    array = range(1, n+1)
    cost = int(math.ceil((3*2**(k-2) - 1) / float(k -1)))
    root = Node(array.pop((n-1)/2))

    number = find_close(array, root.number-cost)
    left_node = Node(number)
    array.remove(number)
    left_node.depth = root.depth + 1
    root.left = left_node

    number = find_close(array, root.number, left=False)
    mid_node = Node(number)
    array.remove(number)
    mid_node.depth = root.depth + 1
    root.mid = mid_node

    number = find_close(array, root.number+cost, left=False)
    right_node = Node(number)
    array.remove(number)
    right_node.depth = root.depth + 1
    root.right = right_node
    temp_right_key_array, temp_left_key_array= [], []

    left_array = array[:len(array)/3]
    mid_array = array[len(array)/3:2*len(array)/3]
    right_array= array[2*len(array)/3:]
    temp_left_key_array.append(left_node.number)
    temp_right_key_array.append(right_node.number)
    len_array,poi = (n-1)/3, (n/2)-(cost*2)+1
    lf,rf = -1,0
       
    while len(temp_left_key_array):
        temp_left_key=temp_left_key_array.pop(0)-cost
        temp_right_key=temp_right_key_array.pop(0)+cost-2
        for i in range (0,2):
            if((temp_left_key) not in left_array) and ((temp_left_key) in mid_array):
                y = left_array.pop(lf)
                mid_array.insert(0,y)
                mid_array.remove(temp_left_key)
                left_array.append(temp_left_key)
                lf-=1
                temp_left_key_array.append(temp_left_key+i)
                temp_left_key+=1

            if((temp_right_key) not in right_array) and ((temp_right_key) in mid_array):
                y = right_array.pop(rf)
                mid_array.remove(temp_right_key)
                mid_array.append(y)
                right_array.insert(0,temp_right_key)
                rf+=1
                if i == 0:temp_right_key_array.append(temp_right_key-1)
                else:temp_right_key_array.append(temp_right_key)
                temp_right_key+=1

    construct_left_binary_tree(left_node, left_array, cost, k)
    construct_mid_binary_tree(mid_node, mid_array, cost, k)
    construct_right_binary_tree(right_node, right_array, cost, k)
    return root


def construct_left_binary_tree(node_root, array, cost, depth):
    root = node_root
    if root.depth >= depth:
        return

    number = find_close(array, (root.number-cost))
    root.left = Node(number)
    root.left.depth = root.depth + 1
    array.remove(number)
    construct_left_binary_tree(root.left, array, cost, depth)

    number = find_close(array, number+1, left=False)
    root.right = Node(number)
    root.right.depth = root.depth + 1
    array.remove(number)
    construct_left_binary_tree(root.right, array, cost, depth)

    return root

def construct_mid_binary_tree(node_root, array, cost, depth):
    root = node_root
    if root.depth >= depth:
        return

    number = find_close(array, root.number+cost, left=False)
    root.right = Node(number)
    root.right.depth = root.depth + 1
    array.remove(number)
    construct_right_binary_tree(root.right, array, cost, depth)

    number = find_close(array, (number-1))
    root.left = Node(number)
    root.left.depth = root.depth + 1
    array.remove(number)

    construct_left_binary_tree(root.left, array, cost, depth)
    
    return root

def construct_right_binary_tree(node_root, array, cost, depth):
    root = node_root
    if root.depth >= depth:
        return

    number = find_close(array, (root.number+cost), left=False)
    root.right = Node(number)
    root.right.depth = root.depth + 1
    array.remove(number)
    construct_right_binary_tree(root.right, array, cost, depth)

    number = find_close(array, number-1)
    root.left = Node(number)
    root.left.depth = root.depth + 1
    array.remove(number)
    construct_right_binary_tree(root.left, array, cost, depth)
    
    return root

def find_close(array, number, left=True):
    zip_array = [(abs(n-number), (n-number) if left else (number-n) ,n) for n in array]
    return min(zip_array)[2] 


if __name__ == "__main__":
    import sys
    k = int(sys.argv[1])
    tree = construct_in_strategy(k)
    print "%s"%tree.tree_score()[0]
    output = []
    for nodes in tree.bfs():
        output.append(map(str, nodes))
    print " ".join(reduce(lambda x, y: x+y, output))


