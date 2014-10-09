#!/usr/bin/env python

def distinguishable_colors(n_colors):
	import numpy as np
	from colormath.color_objects import sRGBColor, LabColor
	from colormath.color_conversions import convert_color
	from matplotlib.colors import rgb2hex
	
	bg = [1,1,1]	#Assumes background is white


	#Generate 30^3 RGB triples to choose from.

	n_grid = 30	
	x = np.linspace(0,1,n_grid)
	R = np.array([x]*900).flatten()
	G = np.array([[i]*30 for i in x]*30).flatten()
	B = np.array([[i]*900 for i in x]).flatten()

	rgb = np.array([R,G,B]).T			#27000 by 3 matrix 

	if n_colors > len(rgb)/3:	#>27000
		print "You can't distinguish that many colors, dingus"
		return None

	#Convert to Lab colorspace
	lab = np.array([list(convert_color(sRGBColor(i[0], i[1], i[2]), LabColor).get_value_tuple()) for i in rgb])
	bglab = list(convert_color(sRGBColor(bg[0], bg[1], bg[2]), LabColor).get_value_tuple())

	#Compute the distance from background to candicate colors
	arr_length = len(rgb)
	mindist2 = np.empty(arr_length)
	mindist2.fill(float('Inf'))
	dX = lab - bglab
	dist2 = np.sum(np.square(dX), axis=1)
	mindist2 = np.minimum(dist2, mindist2)	

	#Pick the colors
	colors = np.zeros((n_colors, 3))
	lastlab = bglab
	
	for i in range(n_colors):
		dX = lab - lastlab	#subtract last from all colors in the list
		dist2 = np.sum(np.square(dX), axis=1)
		mindist2 = np.minimum(dist2, mindist2)
		index = np.argmax(mindist2)
		colors[i] = rgb[index]
		lastlab = lab[index]

	hex_colors =  [rgb2hex(item) for item in colors]

	return hex_colors
