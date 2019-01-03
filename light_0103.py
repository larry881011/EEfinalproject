# AM 12/29 (light is as a linear function)
from vpython import *
import math
n = [1, 1.7, 1.33] 						# refraction index (air, oil, water)
y_oil = 0.2
y_water = 0.1

class light:
	def __init__(self,wl,origin,direction,length=0,amplitude=1):   
		self.wl = wl 					# wavelength
		self.source = origin			# light source
		self.direction = direction		# light beam direction 

		self.amplitude = amplitude		# amplitude (strength)
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
	length = mag(light.direction*times)*n[light.medium]  # count length
	return length, new_origin
	

def refraction_or_reflection(light1,interface,case):  # function to refraction 
	#case: 0.reflection and refraction 1.reflection only 2.refraction only
	             
	sin_theta_in = light1.direction.x/mag(light1.direction) #算入射角的sin值
	cos_theta_in = math.sqrt(1-sin_theta_in**2)			  #算入射角的cos值
	n1 = n[light1.medium]								  #決定n1
	
	#決定n2
	if light1.direction.y<= 0:	#如果光是往下射
		n2 = n[light1.medium+1]					
	else:
		n2 = n[interface.no]
				
	#print(n1,n2)
	l,o = get_length_and_origin(light1,interface) 
	light1.length += l 		#更新光程
	light1.source = o 		#更新原點
	#print(o)
	
	
	sin_theta_out = sin_theta_in*(n1/n2)
	cos_theta_out = math.sqrt(1-sin_theta_out**2)
	#by Fresnel equations
	R = ((n1*cos_theta_out-n2*cos_theta_in)/(n1*cos_theta_out+n2*cos_theta_in))**2  # reflectance(ratio of reflection)
	T = 1 - R   # transmitance(ratio of refraction)

	if case == 0:
		a = vec(light1.direction.x,-light1.direction.y,0)
		re_beam	= light(wl=light1.wl,origin=light1.source,\
			direction=a,length=l,amplitude=R)
		re_beams.append(re_beam)

		light1.direction = vec(sin_theta_out,-cos_theta_out,0)
		light1.medium += 1
		light1.amplitude *= T

	if case == 1:
		light1.direction = vec(light1.direction.x,-light1.direction.y,0)
		light1.amplitude *= R

	if case == 2:
		light1.direction = vec(sin_theta_out,cos_theta_out,0)
		light1.amplitude *= T
		light1.medium -= 1


		
if __name__ =="__main__":
	a = graph(width = 1200, align = 'left', ymin=0)
	g = gcurve(color = color.blue)
	f = gcurve(color = color.red)


	beams = []
	re_beams = []

	air_oil = interface(y_oil,0)
	oil_water = interface(y_water,1)
	
	precise = 100
	for i in range(precise):
		for j in range(1):
			
			beam = light(400*10**(-7),vec(-5+1/precise*i,5+1/precise*i,1/precise*j),vec(1,-1,0))
			beams.append(beam)
	
	for beam in beams:
		refraction_or_reflection(beam,air_oil,0)
		
		refraction_or_reflection(beam,oil_water,1)
		
		refraction_or_reflection(beam,air_oil,2)

	for b in beams:
		b.phase = (b.length/b.wl)%1*2*pi 

	for b in re_beams:
		b.phase = (b.length/b.wl)%1*2*pi 
		"""
	for beam in beams:
		print("wavelength",beam.wl,"source",beam.source,"direction",beam.direction,\
			"amplitude",beam.amplitude,"length",beam.length,"phase",beam.phase,"medium",\
			beam.medium,"finish",beam.finish) 

	for beam in re_beams:
		print("wavelength",beam.wl,"source",beam.source,"direction",beam.direction,\
			"amplitude",beam.amplitude,"length",beam.length,"phase",beam.phase,"medium",\
			beam.medium,"finish",beam.finish) 
			"""
	for b in beams:
		g.plot(b.source.x,b.phase)
	for b in re_beams:
		f.plot(b.source.x,b.phase)








