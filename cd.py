from vpython import *
import numpy as np


scene = canvas(width=400, height=450, center =vec(0, 0, 0),axis=vec(0.5,0,0))
CD = cylinder(pos = vec(0, 0.0, 0),radius = 0.5, axis=vec(0,0.1,0))
for i in range(1000):
    a = np.random.rand(1,1)/2
    b = np.random.rand(1,1)/2
    if a**2+b**2<=0.25: 
        i= box (pos = vec(a,0.1,b),size= vec(0.01,np.random.rand(1,1)/20,0.01),color = color.red)
for j in range(1000):
    a = np.random.rand(1,1)/2
    b = np.random.rand(1,1)/2
    if a**2+b**2<=0.25: 
        j= box (pos = vec(-a,0.1,b),size= vec(0.01,np.random.rand(1,1)/20,0.01),color = color.red)
for k in range(1000):
    a = np.random.rand(1,1)/2
    b = np.random.rand(1,1)/2
    if a**2+b**2<=0.25:
        k= box (pos = vec(-a,0.1,-b),size= vec(0.01,np.random.rand(1,1)/20,0.01),color = color.red)
for l in range(1000):
    a = np.random.rand(1,1)/2
    b = np.random.rand(1,1)/2
    if a**2+b**2<=0.25: 
        l= box (pos = vec(a,0.1,-b),size= vec(0.01,np.random.rand(1,1)/20,0.01),color = color.red)  



