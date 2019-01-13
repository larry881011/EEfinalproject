from vpython import *
import math
import numpy as np

n = [1,1.5,1.33]							# refraction index (air, oil, water)
class light:
	def __init__(self,wl,origin,direction,length=0,amplitude=1):   
		self.wl = wl 					# wavelength 				( m )
		self.source = origin			# light source 				( vector, m )
		self.direction = direction		# light beam direction 		( vector )
		self.amplitude = amplitude		# amplitude 
		self.length = length  			# length of light path 		( m, but actually measured in λs)
		self.phase = 0					# phase 					(radian 0~2pi)
		self.medium = 0 				# medium, 0=air 1=oil 2=water
		
class interface:
	def __init__(self,x0,y0,z0,r,number):
	# interface: a sphere which has radius r and its center at (x0,y0,z0)
		self.center = vec(x0,y0,z0)
		self.r = r
		self.no = number				# number of interface, air-oil=0 oil-water=1

def get_length_and_origin(light,interface):
	# the function to get how far does light goes and the new origin
	# now calculate source + r * lightdirection = on interface 
	A = mag2(light.direction)
	B = dot(light.direction,light.source-interface.center)
	C = mag2(light.source-interface.center)-interface.r**2
	r1 = ( -B - sqrt(B*B - A*C) ) / A
	r2 = ( -B + sqrt(B*B - A*C) ) / A
	if r1<0:
		t = r2
	else:
		t = r1
	new_source = light.source + t * light.direction
	length = mag( new_source - light.source ) * n[light.medium]  # count length
	return length, new_source
	

def refraction_or_reflection(light1,interface,case):  
	#case0	reflection + refraction 
	#case1	reflection only 
	#case2	refraction only

	l,o = get_length_and_origin(light1,interface)
	NormVec = o - interface.center
	theta_in = diff_angle(light1.direction,NormVec)	#入射角(可能大於pi/2)
	sin_theta_in = abs(sin(theta_in))
	cos_theta_in = abs(cos(theta_in))
	n1 = n[light1.medium]								  	#決定n1
	
	#決定n2

	if light1.medium == interface.no :	#如果光是往下射				############################  MODIFIED
		n2 = n[light1.medium+1]				
	else:
		n2 = n[interface.no]
				
	#print(n1,n2)
	light1.length += l*n1	#更新光程
	light1.source = o 		#更新原點
	#print(o)
	
	sin_theta_out = sin_theta_in*(n1/n2)
	cos_theta_out = sqrt(1-sin_theta_out**2)

	#by Fresnel equations
	R = ((n1*cos_theta_out-n2*cos_theta_in)/(n1*cos_theta_out+n2*cos_theta_in))**2  # reflectance(ratio of reflection)
	T = 1 - R   # transmitance(ratio of refraction)

	if dot(light1.direction,NormVec)<0:
		direction_out = NormVec.rotate(angle = (pi-asin(sin_theta_out)),axis = cross(NormVec,light1.direction))
		reflection_direction = light1.direction.rotate(angle=(pi-2*asin(sin_theta_in)),axis=cross(light1.direction,NormVec))
	else:
		direction_out = NormVec.rotate(angle = asin(sin_theta_out), axis = cross(NormVec,light1.direction))
		reflection_direction = light1.direction.rotate(angle=(pi-2*asin(sin_theta_in)),axis=cross(NormVec,light1.direction))

	#reflection + refraction
	if case == 0:
		if n2>n1:
			re_beam	= light(wl=light1.wl, origin=light1.source, direction=reflection_direction, length=l+1/2 * light1.wl, amplitude=R**0.5)
		else:
			re_beam	= light(wl=light1.wl, origin=light1.source, direction=reflection_direction, length=l, amplitude=R**0.5)
		re_beams.append(re_beam)

		light1.direction = direction_out
		light1.medium += 1
		light1.amplitude *= T**0.5

	#reflection
	if case == 1:
		light1.direction = reflection_direction
		light1.amplitude *= R**0.5
		

	#refraction
	if case == 2:
		light1.direction = direction_out
		light1.amplitude *= T**0.5
		light1.medium -= 1


		
if __name__ =="__main__":
	a = graph(width = 600,height = 600, align = 'left')

##-------- VARIABLE DEFINITION --------##
# INTERFACE
	Xoil, Yoil, Zoil = 0,-300,0				# center of oil shell
	Roil = sqrt(300**2 + 1**2)					# radius of oil shell

	Xwater, Ywater, Zwater = 0,-10000,0		# center of water shell
	Rwater = 10000							# radius of water shell

# LIGHT
	precise = 10000*9			# number of light beams
	wavelength = [450,540,680] 	# blue, green, red
	source_x_range = 0
	source_y_range = 0
	axis_x_range = 5
	area_divide = 500

	Xmax = 1
	Xmin = -1
	Xrange = Xmax - Xmin
	Zmax = 1
	Zmin = -1
	Zrange = Zmax - Zmin	

	
## GENERATE LIGHTS
	
	air_oil = interface(Xoil,Yoil,Zoil,Roil,0)
	oil_water = interface(Xwater,Ywater,Zwater,Rwater,1)
	light_sum = np.zeros((area_divide**2,4))

	for j in range(int(precise**0.5)):
		print(str(j/precise**0.5*100)+'%')
		for k in range(len(wavelength)):
			beams = []
			re_beams = []
			for i in range(int(precise**0.5)):
				beam = light(wavelength[k]*1E-7,vec(0,5,0),vec(-0.5+1.0*i/precise**0.5,-5,-0.5+1.0*j/precise**0.5))
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

## now list beams[] / re_beams[] stores 1 certain WL & 1-D of light beams

## MEAN_amplitude IN EACH SMALL AREA		
			for i in range(int(precise**0.5)):
				area_index_x = floor((beams[i].source.x-Xmin)/Xrange*area_divide)
				area_index_z = floor((beams[i].source.z-Zmin)/Zrange*area_divide)

				sum_amplitude = sqrt(beams[i].amplitude**2 + re_beams[i].amplitude**2 + 2*beams[i].amplitude*re_beams[i].amplitude*cos(beams[i].phase - re_beams[i].phase))  

				light_sum[area_divide*area_index_z + area_index_x,k] += sum_amplitude**2
				light_sum[area_divide*area_index_z + area_index_x,3] += 1

## SHOW ON SCREEN

	for i in range(area_divide**2):
		if(light_sum[i,3]!=0):
			light_sum[i,0] = light_sum[i,0] * 3 / light_sum [i,3]
			light_sum[i,1] = light_sum[i,1] * 3 / light_sum [i,3]
			light_sum[i,2] = light_sum[i,2] * 3 / light_sum [i,3]

		d = gdots(color = 20*vec(light_sum[i,2],light_sum[i,1],light_sum[i,0]))
		if (light_sum[i,3]!=0) :
			d.plot(Xmin+Xrange*(i % area_divide)/area_divide,  Zmin+Zrange*floor(i/area_divide)/area_divide)			

	'''
	for i in range(area_divide):
		blue.plot(i,all_light_sum[0][i,0])
		red.plot(i,all_light_sum[2][i,0])
		green.plot(i,all_light_sum[1][i,0])
	'''
