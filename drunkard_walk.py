import numpy as np
from random import randint
W = 35 # field width
H = 30 # field height

f = np.ones((H, W))
p = 0.8 # walls percentage
pos = [H//2, W//2]
f[pos[0], pos[1]] = 0
while True:
    if f.sum()/f.size < p:
        break
    dx = randint(0, 2) - 1
    dy = randint(0, 2) - 1
    if dx != 0:
        pos[1] += dx
    else:
        pos[0] += dy
    
    if pos[0] < 1:
        pos[0] = 1
    elif pos[0] > H-2:
        pos[0] = H-2
    if pos[1] < 1:
        pos[1] = 1
    elif pos[1] > W-2:
        pos[1] = W-2
    f[pos[0], pos[1]] = 0

# print field
for line in f:
    for num in line:
        if num == 1:
            print("##", end="")
        else:
            print("  ", end="")
    print("")