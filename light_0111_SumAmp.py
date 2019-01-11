from vpython import *
import math
import numpy as np

class light:
	def __init__(self,wl,origin,direction,length=0,amplitude=1):   
		self.wl = wl 					# wavelength 				( m )
		self.source = origin			# light source 				( vector, m )
		self.direction = direction		# light beam direction 		( vector )
		self.amplitude = amplitude		# amplitude 
		self.length = length  			# length of light path 		( m, but actually measured in λs)
		self.phase = 0					# phase 					(radian 0~2pi)
		self.medium = 0 				# medium, 0=air 1=oil 2=water
		self.finish = False
		
class interface:
	def __init__(self,x0,y0,z0,a,b,c,number):
	# interface: ax + by + cz = CONST.
		self.CONST = a*x0 + b*y0 + c*z0
		self.NormVec = vector(a,b,c)
		self.no = number				# number of interface, air-oil=0 oil-water=1

def get_length_and_origin(light,interface):   # the function to get how far does light goes and the new origin
	# now calculate source + r * lightdirection = on interface 
	global count
	r = abs((interface.CONST - dot(interface.NormVec,light.source)) / dot(interface.NormVec,light.direction))
	if r<0:
		count += 1
		print("the light doesnt point to the surface, r<0 ",count)
	new_source = light.source + r * light.direction
	length = mag( new_source - light.source ) * n[light.medium]  # count length
	return length, new_source
	

def refraction_or_reflection(light1,interface,case):  
	#case0	reflection + refraction 
	#case1	reflection only 
	#case2	refraction only
	             
	theta_in = diff_angle(light1.direction,interface.NormVec)	#入射角(可能大於pi/2)
	sin_theta_in = abs(sin(theta_in))
	cos_theta_in = abs(cos(theta_in))
	n1 = n[light1.medium]								  	#決定n1
	
	#決定n2

	if light1.direction.y <= 0:	#如果光是往下射
		n2 = n[light1.medium+1]					
	else:
		n2 = n[interface.no]
				
	#print(n1,n2)
	l,o = get_length_and_origin(light1,interface) 
	light1.length += l 		#更新光程
	light1.source = o 		#更新原點
	#print(o)
	
	sin_theta_out = sin_theta_in*(n1/n2)
	cos_theta_out = sqrt(1-sin_theta_out**2)

	#by Fresnel equations
	R = ((n1*cos_theta_out-n2*cos_theta_in)/(n1*cos_theta_out+n2*cos_theta_in))**2  # reflectance(ratio of reflection)
	T = 1 - R   # transmitance(ratio of refraction)

	if dot(light1.direction,interface.NormVec)<0:
		direction_out = interface.NormVec.rotate(angle = (pi-asin(sin_theta_out)),axis = cross(interface.NormVec,light1.direction))
		reflection_direction = light1.direction.rotate(angle=(pi-2*asin(sin_theta_in)),axis=cross(light1.direction,interface.NormVec))
	else:
		direction_out = interface.NormVec.rotate(angle = asin(sin_theta_out), axis = cross(interface.NormVec,light1.direction))
		reflection_direction = light1.direction.rotate(angle=(pi-2*asin(sin_theta_in)),axis=cross(interface.NormVec,light1.direction))

	#reflection + refraction
	if case == 0:
		if n2>n1:
			re_beam	= light(wl=light1.wl, origin=light1.source, direction=reflection_direction, length=l+1/2 * light1.wl, amplitude=R)
		else:
			re_beam	= light(wl=light1.wl, origin=light1.source, direction=reflection_direction, length=l, amplitude=R)
		re_beams.append(re_beam)

		light1.direction = direction_out
		light1.medium += 1
		light1.amplitude *= T

	#reflection
	if case == 1:
		light1.direction = reflection_direction
		light1.amplitude *= R
		light1.length += 1/2 * light1.wl

	#refraction
	if case == 2:
		light1.direction = direction_out
		light1.amplitude *= T
		light1.medium -= 1


		
if __name__ =="__main__":
	a = graph(width = 1200, align = 'left', ymin=0)
		
##-------- VARIABLE DEFINITION --------##
# INTERFACE
	Xoil, Yoil, Zoil = 0.005,0,0				# a point on the air-oil interface
	thetaD = 87 #deg							# dip angle of the normal vector of the air-oil plane
	XoilD, YoilD, ZoilD = cos( thetaD* 2*pi/360),sin( thetaD* 2*pi/360),0

	Xwater, Ywater, Zwater = 0.005,0,0			# a point on the oil-water interface
	XwaterD,YwaterD,ZwaterD= 0,1,0				# normal vector ofthe oil-water interface

	n = [1,1.5,1.33]							# refraction index (air, oil, water)
# LIGHT
	precise = 10000				# number of ligh beams
	wavelength = [450,540,680] 	# blue, green, red
	source_x_range = 0.001
	source_y_range = 0
	area_divide = 1000

##-------- INTERNAL VARIABLES --------##
	count = 0	
	all_light_sum = []
	
## GENERATE LIGHTS	
	for k in range(len(wavelength)):
		beams = []
		re_beams = []

		air_oil = interface(Xoil,Yoil,Zoil,XoilD,YoilD,ZoilD,0)
		oil_water = interface(Xwater,Ywater,Zwater,XwaterD,YwaterD,ZwaterD,1)
	

		for i in range(precise):
			for j in range(1):
			
				beam = light(wavelength[k]*1E-7,vec(-5 + source_x_range /precise*i, 5 + source_y_range/precise*i, 0/precise*j),vec(cos(pi/4),-sin(pi/4),0))
				beams.append(beam)

## REFRACTION SIMULATION
		for beam in beams:
			refraction_or_reflection(beam,air_oil,0)
		
			refraction_or_reflection(beam,oil_water,1)
		
			refraction_or_reflection(beam,air_oil,2)

		for b in beams:
			b.phase = (b.length/b.wl)%1*2*pi 

		for b in re_beams:
			b.phase = (b.length/b.wl)%1*2*pi 

## MEAN_amplitude IN EACH SMALL AREA			
		Xmax = beams[-1].source.x
		Xmin = beams[0].source.x
		Xrange = Xmax - Xmin

		light_sum = np.zeros((area_divide,2))	# light_sum [ area, # of light ]
		for i in range(precise):
			area_index = floor((beams[i].source.x-Xmin)/Xrange*area_divide)
		#sum_amplitude = sqrt((Acos(a)+Bcos(b))**2 + (Asin(a)+Bsin(b))**2)	
		#sum_phase = atan([Asin(a)+Bsin(b)]/[Acos(a)+Bcos(b)])
		# the last light has index 1000 hence ignore
			if area_index < area_divide: 
				sum_amplitude = sqrt(beams[i].amplitude**2 + re_beams[i].amplitude**2 + \
					2*beams[i].amplitude*re_beams[i].amplitude*cos(beams[i].phase - re_beams[i].phase))  

				light_sum[area_index,0] += sum_amplitude
				light_sum[area_index,1] += 1

		for i in range(area_divide):
			if light_sum[i,1] !=0:
				light_sum[i,0] /= light_sum[i,1]

## RESULT OF CERTAIN WAVELENGTH ADD TO LIST		
		all_light_sum.append(light_sum)


## SHOW ON SCREEN
	dots = []
	for i in range(len(all_light_sum[0])):

		d = gdots(color = 128*vec(all_light_sum[2][i,0],all_light_sum[1][i,0],all_light_sum[0][i,0]))
		dots.append(d)

	for i in range(len(dots)):
		for j in range(50):

			dots[i].plot(i*0.000001,j/50)