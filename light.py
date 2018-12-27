from vpython import *
import math
n_oil = 1.7
n_water = 1.33

class light:
	def __init__(self,wl,pos,v):  # wl = wavelength 
		self.wl = wl
		self.v = v
		self.pos = pos
		self.length = 0
		self.phase = 0
		self.condition = 0

	def refraction(self,n1,n2):
		in_sintheta = self.v.x/mag(self.v)
		if n1*in_sintheta>=n2:
			self.v.y = -self.v.y
			print("total reflection")
		else:
			out_sintheta = in_sintheta*(n1/n2)
			new_v = self.v.mag*(n1/n2)
			self.v = vec(new_v*math.sqrt(1-out_sintheta**2),-new_v*out_sintheta,0)
			print("refraction")

	def reflection(self):
		self.v.y = -self.v.y

def touchsensor(pos):
	if pos.x>=5 and pos.x>=7 and pos.y>=5 and pos.y<=7 and pos.x+pos.y>12:
		return True
	else:
		return False


beam = light(400*10**(-7),vec(-6,6,0),vec(6,-6,0))

dt = 0.0001
count = 0

while True:
	beam.pos += beam.v*dt
	beam.length += mag(beam.v)*dt
	try:
		re_beam.pos += re_beam.v*dt
		re_beam.length += mag(re_beam.v)*dt
	except:
		pass
	
	if 2<=beam.pos.y and beam.pos.y<=4 and beam.condition == 0:
		
		beam.refraction(1,n_oil)		
		beam.condition = 1
		re_beam = light(beam.wl,beam.pos,vec(beam.v.x,-beam.v.y,beam.v.z))
		
	if  0<=beam.pos.y and beam.pos.y<=2 and beam.condition == 1:
		
		beam.refraction(n_oil,n_water)
		beam.condition = 2
		
	
	if  beam.pos.y>=4 and beam.condition == 2:
		print(111)
		beam.refraction(n_water,1)
		beam.condition = 3
	
	if touchsensor(beam.pos):
		count += 1
	try:
		if touchsensor(re_beam.pos):
			count += 1
	except:
		pass

	if count == 2:
		break


print(beam.length)
beam.phase = ((beam.length % beam.wl) /beam.wl) *2*pi 
print(beam.phase)
print("pos",beam.pos)

print(re_beam.length)
re_beam.phase = ((re_beam.length % re_beam.wl) / re_beam.wl) *2*pi 
print(re_beam.phase)

	