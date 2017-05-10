import re, time, os, math, argparse
from geopy.distance import vincenty
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


def generateCoord(coord_string):
	lat = coord_string[:coord_string.index(",")]
	lon = coord_string[(coord_string.index(",")+1):]
	return( (lat,lon) )

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c1', '--coordenadas1', required=True, action='store', help='Coordenadas 1')
	parser.add_argument('-c2', '--coordenadas2', required=True, action='store', help='Coordenadas 2')
	parser.add_argument('-c3', '--coordenadas3', required=True, action='store', help='Coordenadas 3')
	parser.add_argument('-r1', '--ratio1', required=True, action='store', help='Ratio 1')
	parser.add_argument('-r2', '--ratio2', required=True, action='store', help='Ratio 2')
	parser.add_argument('-r3', '--ratio3', required=True, action='store', help='Ratio 3')
	my_args = parser.parse_args()
	return my_args


def getCoords(args):
	
	c1 = generateCoord(args.coordenadas1)
	c2 = generateCoord(args.coordenadas2)
	c3 = generateCoord(args.coordenadas3)
	r1 = float(args.ratio1)
	r2 = float(args.ratio2)
	r3 = float(args.ratio3)

	D1 = vincenty(c1,c2).kilometers
	D2 = vincenty(c1,c3).kilometers

	if(D1>(r1+r2) or D2>(r1+r3)): print("D1>(r1+r2) or D2>(r1+r3)")

	h1 = getHeight(D=D1,r1=r1,r2=r2)
	n1 = getCat(hip=r1,cat=h1)
	
	h2 = getHeight(D=D2,r1=r1,r2=r3)
	m2 = getCat(hip=r1,cat=h2)

	gradeKmLat = vincenty(float(c1[0]), float(c1[0])+1).kilometers
	gradeKmLon = vincenty(float(c1[0]), float(c1[1])+1).kilometers
	
	newLat = float(c1[0]) + (n1/gradeKmLat)
	newLon = float(c1[1]) + (m2/gradeKmLon)
	newCoord= (newLat,newLon)

	# print("D1 = "+str(D1)+"  \nD2 = "+str(D2)+"\nn1 = "+str(n1)+"\nm2 = "+str(m2) + "\ngradeKmLat = "+str(gradeKmLat)+"\ngradeKmLon = "+str(gradeKmLon))	
	print ("c1 = ("+args.coordenadas1+") \nc2 = ("+args.coordenadas2+") \nc3 = ("+args.coordenadas3+") \nc0 = ("+str(newCoord)+")")

	


	# setup Lambert Conformal basemap.
	m = Basemap(width=12000000,height=9000000,projection='lcc',
	            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
	# draw a boundary around the map, fill the background.
	# this background will end up being the ocean color, since
	# the continents will be drawn on top.
	m.drawmapboundary(fill_color='aqua')
	# fill continents, set lake color same as ocean color.
	m.fillcontinents(color='coral',lake_color='aqua')
	# draw parallels and meridians.
	# label parallels on right and top
	# meridians on bottom and left
	parallels = np.arange(0.,81,10.)
	# labels = [left,right,top,bottom]
	m.drawparallels(parallels,labels=[False,True,True,False])
	meridians = np.arange(10.,351.,20.)
	m.drawmeridians(meridians,labels=[True,False,False,True])
	# plot blue dot on Boulder, colorado and label it as such.
	lon, lat = -104.237, 40.125 # Location of Boulder
	# convert to map projection coords.
	# Note that lon,lat can be scalars, lists or numpy arrays.
	xpt,ypt = m(lon,lat)
	# convert back to lat/lon
	lonpt, latpt = m(xpt,ypt,inverse=True)
	m.plot(xpt,ypt,'bo')  # plot a blue dot there
	# put some text next to the dot, offset a little bit
	# (the offset is in map projection coordinates)
	plt.text(xpt+100000,ypt+100000,'Boulder (%5.1fW,%3.1fN)' % (lonpt,latpt))
	plt.show()




def getHeight(D,r1,r2):
	s = float((D+r1+r2)/2.0)
	#if (s*(s-D)*(s-r1)*(s-r2) < 0):
	#	print("s    = "+str(s) )
	#	print("s-D  = "+str(s-D) )
	#	print("s-r1 = "+str(s-r1) )
	#	print("s-r2 = "+str(s-r2) )

	h = (2/D)*math.sqrt(s*(s-D)*(s-r1)*(s-r2))
	return h


def getCat(hip,cat):
	c = math.sqrt(hip*hip-cat*cat)
	return c


def main():
		args = get_args()	
		getCoords(args)

		
if __name__ == "__main__":
    main()
