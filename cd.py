from vpython import *
import numpy as np


class light:
	def __init__(self,wavelength=None,v=vec(0,0,0)):
		self.wl = wavelength
		self.v = v
		self.pos = vec(0,0,0)
		self.length = 0
		self.phase = 0
	def refraction(self):
		self.v.y = -self.v.y

ball = light(400*10**(-7))
ball.v = vec(6,-6,0)
ball.pos = vec(-7,7,0)	

scene = canvas(width=400, height=450, center =vec(0, 0, 0),axis=vec(0.5,0,0))
CD = cylinder(pos = vec(0, 0.0, 0),radius = 0.5, axis=vec(0,0.1,0))
a = []
r = 0
theta = 0 
dr = 0.05
dtheta = 0.01
dt = 10**(-3)

while r <0.5 :   
    theta = 0 
    while theta<2*pi:
        a.append(box (pos = vec(r*cos(theta),0.1,r*sin(theta)),\
        size= vec(0.03*r,np.random.randint(1,10)*10**(-5),0.03*r),color = color.red))
        theta += dtheta
    r += dr

condition = 0
while True :
	ball.pos += ball.v*dt
	print(ball.pos)
	for balls in a:
		if ball.pos.x - balls.pos.x < balls.size.x and ball.pos.y - balls.pos.y < balls.size.y \
		and ball.pos.z - balls.pos.z < balls.size.z and  ball.v.y<0 and condition == 0:
			ball.refraction()		
			print('have reflected')
			condetion = 1
			
	if condition == 0 and ball.pos.x - CD.pos.x < CD.size.x and ball.pos.y - CD.pos.y < CD.size.y and ball.pos.z - CD.pos.z < CD.size.z:
		ball.refraction()
		print('hit wall')
		condition = 1


	
