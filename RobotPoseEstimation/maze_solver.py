# Authors: Manuel Gozzi, Luisa Chiu
# Maze solver using OpenCV

# This code took heavy inspiration from the following sources:
# https://youtu.be/-keGVhYmY2c

# use the escape key to close the window
# ctrl + c or ctrl + z to stop the program via terminal

import cv2 
import numpy as np
import threading
import time
import math
import argparse

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

argparser = argparse.ArgumentParser()
argparser.add_argument('imagePath', help='path to image file')
args = argparser.parse_args()
imagePath = args.imagePath
grey_img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
_, th = cv2.threshold(grey_img,0,255,cv2.THRESH_OTSU)
cv2.imwrite('./images/BW_img.jpg', th)

p = 0 # Number of points for start and end selection
start = Point(0, 0)
end = Point(0, 0)
lineWidth = 5
paddingAmt = 7
erosionAmt = 7


# signifies up, right, down, left
dirs = [Point(0,1), Point(1,0), Point(0,-1), Point(-1,0)]

maze = cv2.imread(imagePath)
mazeWidth = maze.shape[1]
mazeHeight = maze.shape[0]

ret, maze = cv2.threshold(maze, 127, 255, cv2.THRESH_BINARY)
mazeD = cv2.erode(maze, np.ones((erosionAmt, erosionAmt), np.uint8), iterations=1)

notVisited = 0
visited = 1
found = False
explorationDelayNs = 0.0001

def pointInBounds(point):
    return point.x >= 0 \
        and point.x < mazeWidth \
        and point.y >= 0 \
        and point.y < mazeHeight

def isNotVisited(v, point):
    return v[point.y][point.x] == notVisited

# 1 means visited, 0 means not-visited
def BFS(start, end):
    global maze, mazeD, mazeWidth, mazeHeight, found

    bfsQueue = []
    v = [[0 for i in range(mazeWidth)] for j in range(mazeHeight)]
    # maintain parent info so that we can backtrack to find the complete path
    parent = [[Point(0, 0) for i in range(mazeWidth)] for j in range(mazeHeight)]
    bfsQueue.append(start)
    v[start.y][start.x] = visited

    while len(bfsQueue) > 0:
        p = bfsQueue.pop(0)
        lastTime = int(time.time() * 1000000)
        for dir in dirs:
            np = p + dir
            if pointInBounds(np) and isNotVisited(v, np) \
                and (mazeD[np.y][np.x][0] != 0 \
                or mazeD[np.y][np.x][1] != 0 \
                or mazeD[np.y][np.x][2] != 0):
                    v[np.y][np.x] = v[p.y][p.x] + 1 # we can use this for adding color if we want
                    parent[np.y][np.x] = p
                    # set color of current visited pixel
                    maze[np.y][np.x] = [20 + math.sin(lastTime / 100000) * 20, 50 + math.sin((lastTime / 100000 + 1)) * 50, 80 + math.sin(lastTime / 100000 + 3) * 80]
                    bfsQueue.append(np)
                    if np == end: 
                        found = True
                        del bfsQueue[:] # delete all elements instead of deleting the ref
                        break
        # scale the animation speed by the number of currently explored points
        exploringPointCount = len(bfsQueue)
        if exploringPointCount <= 0:
            exploringPointCount = 1
        sleepTime = explorationDelayNs / exploringPointCount * (int(time.time() * 1000000) - lastTime)
        time.sleep(sleepTime)
    
    # reconstruct the path
    path = []
    if found:
        p = end
        while p != start:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)

        # path is in reverse order prior to this
        path.reverse()
        print("Path Found")
    else:
        print("Path Not Found")

    # old padding method
    # pad optimal path from boundary
    # paddedPath = []
    # for _, p in enumerate(path):
    #     for dir in dirs:
    #         np = p + dir * paddingAmt
    #         paddDirections = []
    #         if pointInBounds(np) \
    #             and maze [np.y][np.x][0] == 0 \
    #             and maze[np.y][np.x][1] == 0 \
    #             and maze[np.y][np.x][2] == 0:
    #                 paddDirections.append(dir)
    #                 break
    #     if len(paddDirections) > 0:
    #         for dir in paddDirections:
    #             p = p - dir * paddingAmt
    #     paddedPath.append(p)
    
    for p in path:
        cv2.rectangle(maze, (p.x-lineWidth, p.y-lineWidth), (p.x+lineWidth, p.y+lineWidth), (50, 50, 255), -1)

    time.sleep(0.2) # wait so the drawing thread can display the path

def mouse_event(event, pX, pY, flags, param):
    global maze, start, end, p
    pW = lineWidth + 2
    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(maze, (pX-pW, pY-pW), (pX+pW, pY+pW), (0, 0, 255), -1)
            start = Point(pX, pY)
            p += 1
        elif p == 1:
            cv2.rectangle(maze, (pX-pW, pY-pW), (pX+pW, pY+pW), (0, 255, 0), -1)
            end = Point(pX, pY)
            p += 1

def disp():
    global maze
    cv2.imshow('maze', maze)
    cv2.imshow('mazeD', mazeD)
    cv2.setMouseCallback('maze', mouse_event)
    while cv2.waitKey(1) != 27:
        cv2.imshow('maze', maze)


t = threading.Thread(target=disp, args=(), daemon=True)
t.start()

print("Select start and end points")

while p < 2:
    pass

BFS(start, end)
t.join()
cv2.destroyAllWindows()