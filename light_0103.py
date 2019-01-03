# AM 12/29 (light is as a linear function)
from vpython import *
import math
n = [1, 1.7, 1.33] 						# refraction index (air, oil, water)
y_oil = 4
y_water = 2

class light:
	def __init__(self,wl,origin,direction,length=0):   
		self.wl = wl 					# wavelength
		self.source = origin			# light source
		self.direction = direction		# light beam direction 

		self.amplitude = 1				# amplitude (strength)
		self.length = length  			# length of light path
		self.phase = 0					# BJ4
		self.medium = 0 				# medium, 0=air 1=oil 2=water
		self.finish = False

class interface:
	def __init__(self,y,number):		# a,b = index of medium
		self.y = y 						# interface height
		self.no = number				# number of interface, air-oil=0 oil-water=1

##-----目前先做這樣-----##
def get_length_and_origin(light,interface):   # the function to get how far does light goes and the new origin
	
	delta_y = abs(light.source.y-interface.y) # count delta y from old origin to new origin
	times = delta_y/abs(light.direction.y)    
	new_origin = light.source + light.direction*times # 算 delta y 是 light.direction 的幾倍 
	length = mag(light.direction*times)  # count length
	return length, new_origin
	

def refraction(light,interface,reflected):  # function to refraction 
	             
	sin_theta_in = light.direction.x/mag(light.direction) #算入射角的sin值
	cos_theta_in = math.sqrt(1-sin_theta_in**2)			  #算入射角的cos值
	n1 = n[light.medium]								  #決定n1
	
	#決定n2
	if light.direction.y<= 0:	#如果光是往下射
		n2 = n[light.medium+1]
		light.medium += 1
				
	else:
		n2 = n[interface.no]
		light.medium -= 1

		
	print(n1,n2)
	l,o = get_length_and_origin(light,interface) 
	light.length += l 		#更新光程
	light.source = o 		#更新原點
	
	
	sin_theta_out = sin_theta_in*(n1/n2)
	cos_theta_out = math.sqrt(1-sin_theta_out**2)
	#by Fresnel equations
	R = ((n1*cos_theta_out-n2*cos_theta_in)/(n1*cos_theta_out+n2*cos_theta_in))**2  # reflectance(ratio of reflection)
	T = 1 - R   # transmitance(ratio of refraction)
	light.amplitude *= T
	if not reflected:

		


		

	light.direction = vec(sin_theta_out,-cos_theta_out,0)
	light.medium += 1

	print(light.direction)

def reflection(light,interface):
	light.direction.y = - light.direction.y
	


if __name__ =="__main__":

	air_oil = interface(y_oil,0)
	oil_water = interface(y_water,1)
	
	for i in range(1):
		for j in range(1):
			
			beam = light(400*10**(-7),vec(-5+0.01*i,5*0.01*j,0),vec(1,-0.1,0))
			beams.append(beam)
	
	for beam in beams:
		refraction(beam,air_oil)
		print(111)
		refraction(beam,oil_water)
		print(222)
		refraction(beam,air_oil)
		print(333)

	for beam in beams:
		print(beam.wl,beam.source,beam.direction,beam.amplitude,beam.length,beam.phase,beam.medium,beam.finish) 






