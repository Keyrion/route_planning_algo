import numpy as np
import matplotlib.pyplot as plt
import time
import random
import math
import cv2

class node:
	def __init__(self, x, y, idx, pre):
		self.x =x
		self.y =y
		self.idx =idx
		self.pre =pre

def get_dist(x1,y1, x2,y2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def swap(a,b):
	return b,a

def get_sample(destx, desty, height, width):
	x = np.random.rand()

	if x > 0.65:
		return [destx, desty]
	else:
		return [np.random.randint(height), np.random.randint(width)]

def next_point(points, randx, randy, step):
	flag = False

	minn = get_dist(points[0].x, points[0].y, randx, randy)
	pre = points[0]

	for nd in points:
		dist = get_dist(nd.x,nd.y, randx, randy)
		if dist < minn:
			minn = dist;
			pre = nd

	if minn > step:
		randx = int(pre.x + (randx - pre.x) * step / minn)
		randy = int(pre.y + (randy - pre.y) * step / minn)

	if minn == 0:
		flag = True
	return [pre, randx, randy, flag]

def no_collision(sx, sy, ex, ey, img):
	# print(str(sx)+" "+str(sy)+" : "+str(ex)+" "+str(ey))

	flag = 1
	if abs(sx-ex) < abs(sy-ey):
		sx,sy = swap(sx, sy)
		ex,ey = swap(ex, ey)
		flag = 0

	gradient = (ey-sy) / (ex-sx)
	intercept = sy - gradient*sx

	step = 1
	if ex -sx < 0:
		step = -1

	xx = sx
	while abs(xx-sx) < abs(ex-sx):
		cor_y = gradient*xx +intercept
		yy = int(cor_y)

		xxx = xx; yyy = yy
		# print(str(xxx)+" "+str(yyy)+" : "+str(step)+" "+str(1000))
		# print(img[xxx][yyy])
		if not flag:
			xxx, yyy = swap(xxx, yyy)

		if img[xxx][yyy][0] == 0 and img[xxx][yyy][1] == 0 and img[xxx][yyy][2]  ==0:
			return False
		if yy != cor_y:
			if (yyy+1 < 1000 and img[xxx][yyy+1][0] == 0) and img[xxx][yyy][1] == 0 and img[xxx][yyy][2]  ==0:
				return False
		xx += step

	return True

clk = time.time()
plt.ion()

maze = cv2.imread("RRT.jpg")

[height, width, channel] = maze.shape

destx = 700; desty = 1000

point_cnt = 0
found = False
points = [node(0,0,0,None)]
step = 10

out = maze

while not found and time.time() - clk <= 30:
	[randx, randy] = get_sample(destx, desty, height, width)
	[prenode, nxtx, nxty, sampled] = next_point(points, randx, randy, step)

	# print(str(randx)+" --- "+str(randy))
	if not sampled:
		if no_collision(prenode.x, prenode.y, nxtx, nxty, maze):
			point_cnt +=1
			points.append(node(nxtx,nxty,point_cnt,prenode))

			cv2.line(out,(prenode.y, prenode.x), (nxty, nxtx), (0,0,255), 1)
			cv2.circle(out,(nxty,nxtx),2, (0,255,0),1)
			if nxtx >= destx-1 and nxtx <= destx+1 and nxty >= desty-2 and nxty <= desty+2:
				found = True;			

print("find in "+str(time.time() - clk)+" s")

cur = points[point_cnt]
while not(cur.x == 0 and cur.y == 0):
	pre = cur.pre
	cv2.line(out,(pre.y, pre.x), (cur.y, cur.x), (255,0,0), 2)
	cur = pre

plt.imshow(out)
plt.pause(1)
plt.ioff()
x = input()