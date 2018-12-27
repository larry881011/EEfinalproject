from vpython import *
import numpy as np


scene = canvas(width=400, height=450, center =vec(0, 0, 0),axis=vec(0.5,0,0))
CD = cylinder(pos = vec(0, 0.0, 0),radius = 0.5, axis=vec(0,0.1,0))
a = []
r = 0
theta = 0 
dr = 0.1
dtheta = 0.1
while r <0.5 :
    r += dr
    theta = 0 
    while theta<2*pi:
        a.append(box (pos = vec(r*cos(theta),0.1,r*sin(theta)),size= vec(0.01,0.01,0.01),color = color.red))
        theta += dtheta