from random import randint, seed
from time import time
from json import dumps
from PIL import Image, ImageDraw

class Node:
    def __init__(self, leaf) -> None:
        self.leaf = leaf
        self.lchild = None
        self.rchild = None
    
    def get_leaves(self):
        if self.lchild == None and self.rchild == None:
            return [self.leaf]
        else:
            res = []
            if self.lchild != None:
                res.extend(self.lchild.get_leaves())
            if self.rchild != None:
                res.extend(self.rchild.get_leaves())
            return res
    
    def get_level(self, level, queue=None):
        if queue == None:
            queue = []
        if level == 1:
            queue.append(self)
        else:
            if self.lchild != None:
                self.lchild.get_level(level - 1, queue)
            if self.rchild != None:
                self.rchild.get_level(level - 1, queue)
        return queue
    
    def paint(self, draw):
        self.leaf.paint(draw)
        if self.lchild != None:
            self.lchild.paint(draw)
        if self.rchild != None:
            self.rchild.paint(draw)

class Container:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = [x+w/2, y+h/2]
    
    def paint(self, draw):
        global SQUARE
        draw.rectangle(
            [self.x, self.y, self.x+self.w, self.y+self.h], 
            (0, 0, 0), 
            (0, 255, 0),
            2
        )


def sdict(d):
    return dumps(d, indent=2, ensure_ascii=False)


def random_split(cont):
    if randint(0, 99) % 2 == 0:
        # vertical
        r1 = Container(
            cont.x, 
            cont.y, 
            randint(cont.w//3, cont.w//3*2), 
            cont.h)
        r2 = Container(
            cont.x+r1.w, 
            cont.y, 
            cont.w-r1.w, 
            cont.h)
        if r1.w / cont.w < 0.4 or r1.w / cont.w > 0.6:
            return(random_split(cont))
    else:
        # horizontal
        r1 = Container(
            cont.x, 
            cont.y, 
            cont.w, 
            randint(cont.h//3, cont.h//3*2))
        r2 = Container(
            cont.x, 
            cont.y+r1.h, 
            cont.w, 
            cont.h-r1.h)
        if r1.h / cont.h < 0.4 or r1.h / cont.h > 0.6:
            return(random_split(cont))
    
    return [r1, r2]


def split_container(cont, i):
    root = Node(cont)
    if root.leaf.w < 50 or root.leaf.h < 50:
        return root
    if i != 0:
        sr = random_split(cont)
        root.lchild = split_container(sr[0], i-1)
        root.rchild = split_container(sr[1], i-1)
    return root

canvas = Image.new("RGB", (500, 500))
MAP_SIZE = 50
SQUARE = canvas.width / MAP_SIZE
N_ITER = 4

if __name__ == "__main__":
    seed(time())
    canvas = Image.new("RGB", (500, 500))
    draw = ImageDraw.Draw(canvas)

    main_cont = Container(0, 0, canvas.width, canvas.height)
    cont_tree = split_container(main_cont, N_ITER)
    
    cont_tree.paint(draw)
    canvas.show()

