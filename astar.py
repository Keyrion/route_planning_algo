import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import heapq
import math

x_size = 50
y_size = 50

destx = 30
desty = 30

ax = plt.gca()
ax.set_xlim([0,x_size])
ax.set_ylim([0,y_size])

class node:
	def __init__(self, v, x, y, h):
		self.val = v
		self.x = x
		self.y = y
		self.h = h

	def __lt__(self, other):
		if self.val < other.val:
			return True
		elif self.val== other.val and self.h < other.h:
			return True
		return False

#--------------------map generation-------------------------
def generate_abmap(map_flag):
	global x_size,y_size
	mmap = [([0]*y_size) for i in range(0, x_size)]
	
	if map_flag == 0:
		for i in range(x_size//4 ,x_size*3//4):
			for j in range(y_size//4,y_size*3//4):
				if random.randint(0,10) > 7:
					mmap[i][j] = 1

		for i in range(0,11):
			mmap[x_size//2+i-1][y_size//2-i-1] = 1
			mmap[x_size//2-i-1][y_size//2+i-1] = 1
			mmap[x_size//2+i][y_size//2-i-1] = 1
			mmap[x_size//2-i][y_size//2+i-1] = 1
			mmap[40][49-i] = 1;mmap[40][42-i] = 1

	elif map_flag == 1:
		for i in range(10,50):
			mmap[13][i] = 1
			mmap[25][50-i] = 1
			mmap[37][i] = 1

	else:
		for i in range(0,20):
			mmap[20+i][10] = 1
			mmap[34][10+i] = 1
			mmap[34][15+i] = 1
			mmap[20+i][34] = 1
	return mmap

def generate_remap(map):
	global ax

	for i in range(0, x_size):
		for j in range(0, y_size):
			if map[i][j]:
				rec = Rectangle((i, j), width=1, height=1, color='gray')
				ax.add_patch(rec)
			else:
				rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor = 'w')
				ax.add_patch(rec)

	rec = Rectangle((0,0), width=1, height=1, edgecolor='gray', facecolor='b')
	ax.add_patch(rec)
	rec = Rectangle((destx, desty), width=1, height=1, edgecolor='gray', facecolor='r')
	ax.add_patch(rec)
#--------------------------------------------------------------

def get_dist(nowx, nowy, curx, cury, flag):
	if flag ==0:
		return int(10*(abs(nowx-curx)+abs(nowy-cury)))
	elif flag == 1:
		return int(10*math.sqrt((nowx-curx)**2+(nowy-cury)**2))
	else:
		dx = abs(nowx - curx)
		dy = abs(nowy - cury)
		return int(10*(dx+dy) + (10*math.sqrt(2) - 20)* min(dx,dy))

#---------------------------------------------------------------

map_flag = int(input("map:"));
H_flag = int(input("H function:"))

mmap = generate_abmap(map_flag)
generate_remap(mmap)

plt.ion()
plt.pause(2)

#-------------------init----------------
openlst = [([0]*y_size) for i in range(0, x_size)]
closelst = [([0]*y_size) for i in range(0, x_size)]
pre = [([node(0,0,0,0)]*y_size) for i in range(0, x_size)]
gval = [([100000000]*y_size) for i in range(0, x_size)]
hval = [([100000000]*y_size) for i in range(0, x_size)]
hp = []

opencnt = 1

openlst[0][0] = 1;
gval[0][0] = 0;
hval[0][0] = get_dist(0,0,destx,desty,H_flag)
heapq.heappush(hp, node(gval[0][0] +hval[0][0], 0, 0, hval[0][0]))                                                           
#----------------------------------------

while opencnt!=0:
	now = hp[0]
	heapq.heappop(hp)

	# which one is correct :o
	if closelst[destx][desty]:   # goal in the closed list
		break

	if destx == now.x and desty == now.y: # reach the goal
		break
 
	rec = Rectangle((now.x,now.y), width=1, height=1, edgecolor='gray', facecolor='b')
	ax.add_patch(rec)

	opencnt -=1;
	openlst[now.x][now.y] =0
	closelst[now.x][now.y] =1

	xxx = now.x-1;yyy = now.y-1
	for i in range (0,3):
		for j in range(0,3):
			curx = xxx+i; cury = yyy+j
			if (curx >= 0 and curx < x_size) and (cury >= 0 and cury < y_size) and (not closelst[curx][cury]) and (not mmap[curx][cury]):

				if openlst[curx][cury] == 1:
					dist = gval[now.x][now.y] + get_dist(now.x, now.y, curx, cury, 1)                    #weight
					
					if gval[curx][cury] > dist:                                                                    
						pre[curx][cury] = node(0, now.x, now.y, hval[curx][cury])
						gval[curx][cury] = dist

						for nn in range(0,len(hp)):
							if hp[nn].x == curx and hp[nn].y == cury:
								hp[nn].val = dist + get_dist(curx,cury,destx,desty, H_flag)                
								break

						heapq.heapify(hp)
				else:
					pre[curx][cury] = node(0, now.x, now.y, hval[curx][cury])

					gval[curx][cury] = gval[now.x][now.y] + get_dist(now.x, now.y, curx, cury, 1)         #weight
					hval[curx][cury] = get_dist(curx, cury, destx, desty, H_flag)

					openlst[curx][cury] =1;
					opencnt +=1

					heapq.heappush(hp, node(gval[curx][cury] + hval[curx][cury], curx, cury, hval[curx][cury]))                     

#------------------show path-----------------------------

xpos=pre[destx][desty].x; ypos=pre[destx][desty].y
while not(xpos == 0 and ypos == 0):
	rec = Rectangle((xpos,ypos), width=1, height=1, edgecolor='gray', facecolor='g')
	ax.add_patch(rec)
	# plt.pause(0.01)
	tmpx = pre[xpos][ypos].x
	tmpy = pre[xpos][ypos].y

	xpos=tmpx;ypos=tmpy

plt.ioff()
plt.show()