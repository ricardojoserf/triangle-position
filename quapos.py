import re, time, os, math, argparse,sys
from geopy.distance import vincenty, great_circle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from plot import drawMap


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c1', '--coordenadas1', required=True, action='store', help='Coordenadas 1')
	parser.add_argument('-c2', '--coordenadas2', required=True, action='store', help='Coordenadas 2')
	parser.add_argument('-c3', '--coordenadas3', required=True, action='store', help='Coordenadas 3')
	parser.add_argument('-c4', '--coordenadas4', required=True, action='store', help='Coordenadas 4')
	parser.add_argument('-r1', '--ratio1', required=True, action='store', help='Ratio 1')
	parser.add_argument('-r2', '--ratio2', required=True, action='store', help='Ratio 2')
	parser.add_argument('-r3', '--ratio3', required=True, action='store', help='Ratio 3')
	parser.add_argument('-r4', '--ratio4', required=True, action='store', help='Ratio 4')
	my_args = parser.parse_args()
	return my_args


def getHeight(D,rA,rB):
	s = float((D+rA+rB)/2.0)
	h = (2/D)*math.sqrt(s*(s-D)*(s-rA)*(s-rB))
	return h


def getCat(hip,cat):
	c = math.sqrt(hip*hip-cat*cat)
	return c


def generateCoord(coord_string):
	lat = coord_string[:coord_string.index(",")]
	lon = coord_string[(coord_string.index(",")+1):]
	return( (lat,lon) )


def drawMap_basemap(base_coords,calculated_coords,ratios):
	deg_diff=1.5
	m = Basemap(llcrnrlon=(float(base_coords[3][1])),llcrnrlat=(float(base_coords[3][0])-deg_diff),urcrnrlon=(float(base_coords[3][1])+deg_diff ),urcrnrlat=(float(base_coords[3][0]) +deg_diff), epsg=5520)
	m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 1500, verbose= False)

	#Paint coords
	colors = ['red','green','blue','purple']
	counter = 0
	for coord in base_coords:
		drawPoint(coord[0],coord[1],m,colors[counter])
		counter+=1
	#Paint polygon
	lats = []
	lons = []
	for coord in calculated_coords:
		lats.append(coord[0])
		lons.append(coord[1])
	x,y = m(lons,lats)
	xy = zip(x,y)
	poly = Polygon( list(xy), facecolor='yellow', alpha=0.4 )
	plt.gca().add_patch(poly)
	plt.show()


def drawPoint(lat,lon,map_,color_):
	xpt,ypt = map_(lon,lat)
	lonpt, latpt = map_(xpt,ypt,inverse=True)
	map_.plot(xpt,ypt,'bo', color=color_)


def getNewCoord(baseCoord,x_,y_):
	gkmlat = (float(baseCoord[0]),     float(baseCoord[1])+1.0)
	gkmlon = (float(baseCoord[0])+1.0, float(baseCoord[1]))
	gradeKmLat = vincenty( baseCoord , gkmlat ).kilometers
	gradeKmLon = vincenty( baseCoord , gkmlon ).kilometers
	newLat = float(baseCoord[0]) + (float(x_)/float(gradeKmLat) )
	newLon = float(baseCoord[1]) + (float(y_)/float(gradeKmLon) )
	return (newLat,newLon)


def checkRatiosInside(ratios,D_diag_1,D_diag_2):
	mal=False
	for i in ratios:
		if ( i > D_diag_1 or i > D_diag_2 ):
			mal = True
	if mal:
		print ("\nPoint is NOT inside")
	else:
		print("\nPoint is inside")


def checkValues(r1, r2, r3, r4, D1, D2, D3, D4, D_diag_1, D_diag_2):
	if(D1>(r1+r2)):
		print("\nProblem: D1>(r1+r2)")
	if(D2>(r2+r3)):
		print("\nProblem: D2>(r2+r3)")
	if(D3>(r3+r4)):
		print("\nProblem: D3>(r3+r4)")
	if(D4>(r1+r4)):
		print("\nProblem: D4>(r1+r4)")
	if(D_diag_1>(r1+r3)):
		print("D_diag_1= "+D_diag_1)
		print("\nProblem: D_diag_1>(r1+r3)")
	if(D_diag_2>(r2+r4)):
		print("\nProblem: D_diag_2>(r2+r4) ")


### TO DO
def reorder(c1,c2,c3,c4,r1,r2,r3,r4):
	coords = [c1,c2,c3,c4]
	lats = []
	lons = []
	for coord in coords:
		lats.append(coord[0])
		lons.append(coord[1])

	max_lat = max(lats)
	max_lat_index = lats.index(max_lat)
	max_lon = max(lons)
	max_lon_index = lons.index(max_lon)

	print (max_lat, max_lat_index)
	print (max_lon, max_lon_index)


def getCoords(args):
	# Coordinates
	c1 = generateCoord(args.coordenadas1)
	c2 = generateCoord(args.coordenadas2)
	c3 = generateCoord(args.coordenadas3)
	c4 = generateCoord(args.coordenadas4)
	
	# Ratios
	r1 = float(args.ratio1)
	r2 = float(args.ratio2)
	r3 = float(args.ratio3)
	r4 = float(args.ratio4)
	
	# Distances between points	
	D1 = vincenty(c1,c2).kilometers
	D2 = vincenty(c2,c3).kilometers
	D3 = vincenty(c3,c4).kilometers
	D4 = vincenty(c4,c1).kilometers
	D_diag_1 = vincenty(c1,c3).kilometers
	D_diag_2 = vincenty(c2,c4).kilometers
	checkValues(r1, r2, r3, r4, D1, D2, D3, D4, D_diag_1, D_diag_2)
	
	# Heights
	h1 = getHeight(D=D1,rA=r1,rB=r2)
	h2 = getHeight(D=D2,rA=r2,rB=r3)
	h3 = getHeight(D=D3,rA=r3,rB=r4)
	h4 = getHeight(D=D4,rA=r4,rB=r1)
	
	# Relative distances
	n1 = getCat(hip=r1,cat=h1)
	m1 = getCat(hip=r2,cat=h1)
	n2 = getCat(hip=r2,cat=h2)
	m2 = getCat(hip=r3,cat=h2)
	n3 = getCat(hip=r3,cat=h3)
	m3 = getCat(hip=r4,cat=h3)
	n4 = getCat(hip=r4,cat=h4)
	m4 = getCat(hip=r1,cat=h4)
	
	# Calculating new coords
	newCoord_1 = getNewCoord(c1,+n1,-m4)
	newCoord_2 = getNewCoord(c2,-m1,-n2)
	newCoord_3 = getNewCoord(c3,-n3,+m2)
	newCoord_4 = getNewCoord(c4,+m3,+n4)
	
	base_coords = [c1,c2,c3,c4]
	ratios=[r1,r2,r3,r4]
	calculated_coords = [newCoord_1,newCoord_2,newCoord_3,newCoord_4]
	
	verbose = True
	if verbose:
		print("\nVerbose: True")
		print("\nD1="+str(D1)+" \nD2="+str(D2)+" \nD3="+str(D3)+" \nD4="+str(D4)+" \nD_diag_1="+str(D_diag_1)+" \nD_diag_2="+str(D_diag_2) )
		print ("\n[Red]\t c1 = ("+args.coordenadas1+") \n[Green]\t c2 = ("+args.coordenadas2+") \n[Blue]\t c3 = ("+args.coordenadas3+") \n[Purple] c4 = ("+args.coordenadas4+")")
		print ("\n[Yellow] newCoord_1 = "+str(newCoord_1)+"\n[Yellow] newCoord_2 = "+str(newCoord_2)+"\n[Yellow] newCoord_3 = "+str(newCoord_3)+"\n[Yellow] newCoord_4 = "+str(newCoord_4) )
		checkRatiosInside(ratios,D_diag_1,D_diag_2)
	try:
		print("Trying to plot results using Plotly")
		points = base_coords + calculated_coords
		drawMap(points)

	except:
		print("\nIt was not possible to plot results using Plotly")
		print("\nTrying to plot results using Matplotlib")
		drawMap_basemap(base_coords,calculated_coords,ratios)


def main():
		args = get_args()	
		getCoords(args)


if __name__ == "__main__":
    main()

