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
            [self.x*SQUARE, self.y*SQUARE, self.x*SQUARE+self.w*SQUARE, self.y*SQUARE+self.h*SQUARE], 
            outline=(0, 255, 0),
            width=2
        )


class Room:
    def __init__(self, cont) -> None:
        self.x = cont.x + randint(1, cont.w//3)
        self.y = cont.y + randint(1, cont.h//3)

        self.w = cont.w - (self.x - cont.x)
        self.h = cont.h - (self.y - cont.y)
        self.w -= randint(1, self.w//3)
        self.h -= randint(1, self.h//3)
    
    def paint(self, draw):
        global SQUARE
        fill_color = (100, 100, 100)
        draw.rectangle(
            [self.x*SQUARE, self.y*SQUARE, self.x*SQUARE+self.w*SQUARE, self.y*SQUARE+self.h*SQUARE],
            fill_color)


def sdict(d):
    return dumps(d, indent=2, ensure_ascii=False)


def random_split(cont):
    if cont.w > cont.h:
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
    
    return [r1, r2]


def split_container(cont, i):
    root = Node(cont)
    if i != 0:
        sr = random_split(cont)
        root.lchild = split_container(sr[0], i-1)
        root.rchild = split_container(sr[1], i-1)
    return root

def draw_paths(tree, draw):
    pass

canvas = Image.new("RGB", (500, 500))
MAP_SIZE = 40
SQUARE = canvas.width / MAP_SIZE
N_ITER = 9

if __name__ == "__main__":
    seed(time())
    canvas = Image.new("RGB", (500, 500))
    draw = ImageDraw.Draw(canvas)
    for i in range(MAP_SIZE):
        draw.line([i*SQUARE, 0, i*SQUARE,500], (50,50,50), 1)
        draw.line([0, i*SQUARE, 500, i*SQUARE], (50,50,50), 1)

    # split map
    main_cont = Container(0, 0, MAP_SIZE, MAP_SIZE)
    cont_tree = split_container(main_cont, N_ITER)
    cont_tree.paint(draw)

    # leaves = cont_tree.get_leaves()
    # for leaf in leaves:
    #     Room(leaf).paint(draw)

    canvas.show()

