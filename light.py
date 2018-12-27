from vpython import *
import math
n_oil = 1.7
n_water = 1.33
"""
scene = canvas(width=800,height=800,center=vec(0,0,0),background=vec(0,0.3,0.3))
oil = box(pos=vec(0,2,0),size=vec(200,2,200),color=color.red)
water = box(pos=vec(0,0,0),size=vec(200,2,200))

"""
class light:
	def __init__(self,wavelength=None,v=vec(0,0,0)):
		self.wl = wavelength
		self.v = v
		self.pos = vec(0,0,0)
		self.length = 0
		self.phase = 0
	def refraction(self,n1,n2):
		in_sintheta = self.v.x/mag(self.v)
		if n1*in_sintheta>=n2:
			self.v.y = -self.v.y
			print("all reflection")
		else:
			out_sintheta = in_sintheta*(n1/n2)
			new_v = self.v.mag*(n1/n2)
			self.v = vec(new_v*math.sqrt(1-out_sintheta**2),-new_v*out_sintheta,0)
			print("refraction")



ball = light(400*10**(-7))

ball.v = vec(6,-6,0)
ball.pos = vec(-5.999999999,5.999999999,0)

dt = 0.001
condition = 0

while True:
	rate(10000)
	ball.pos += ball.v*dt
	print(ball.pos)
	print(ball.v)
	ball.length += mag(ball.v)*dt
	if 2<=ball.pos.y and ball.pos.y<=4 and condition == 0:
		ball.refraction(1,n_oil)		
		condition = 1
		print("*"*60)

	if  0<=ball.pos.y and ball.pos.y<=2 and condition==1:
		
		ball.refraction(n_oil,n_water)
		print("#"*60)
		condition = 2
		break
print(ball.length)
ball.phase = ((ball.length % ball.wl) /ball.wl) *2*pi 
print(ball.phase)

	#if ball.pos.y<=0 and :
		#ball.v.y = -ball.v.y