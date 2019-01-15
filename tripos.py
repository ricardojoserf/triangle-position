import re, time, os, math, argparse
from geopy.distance import vincenty, great_circle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys

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


def getHeight(D,r1,r2):
	s = float((D+r1+r2)/2.0)
	h = (2/D)*math.sqrt(s*(s-D)*(s-r1)*(s-r2))
	return h


def getCat(hip,cat):
	c = math.sqrt(hip*hip-cat*cat)
	return c


def generateCoord(coord_string):
	lat = coord_string[:coord_string.index(",")]
	lon = coord_string[(coord_string.index(",")+1):]
	return( (lat,lon) )


def drawMap(c1,c2,c3,newCoord):
	deg_diff=1.5
	m = Basemap(llcrnrlon=(float(c1[1])),llcrnrlat=(float(c1[0])-deg_diff),urcrnrlon=(float(c1[1])+deg_diff ),urcrnrlat=(float(c3[0]) +deg_diff), epsg=5520)
	m.arcgisimage(service='ESRI_StreetMap_World_2D', xpixels = 1500, verbose= False)
	drawPoint(c1[0],c1[1],m,'r')
	drawPoint(c2[0],c2[1],m,'g')
	drawPoint(c3[0],c3[1],m,'b')
	drawPoint(newCoord[0],newCoord[1],m,'y')
	plt.show()


def drawPoint(lat,lon,map_,color_):
	xpt,ypt = map_(lon,lat)
	lonpt, latpt = map_(xpt,ypt,inverse=True)
	map_.plot(xpt,ypt,'bo', color=color_)


def checkValues(r1, r2, r3, D1, D2, D3):
	problem = False
	if(D1>(r1+r2)): 
		print("Problem: D1>(r1+r2)")
		problem=True
	if(D2>(r1+r3)): 
		print("Problem: D2>(r1+r3)")
		problem=True
	if(D3>(r2+r3)): 
		print("Problem: D3>(r2+r3)")
		problem=True
	if problem:
		print ("\nr1="+str(r1)+"\nr2="+str(r2)+"\nr3="+str(r3)+"\nD1="+str(D1)+" \nD2="+str(D2)+" \nD3="+str(D3))
		sys.exit(0)


def getCoords(args):
	c1 = generateCoord(args.coordenadas1)
	c2 = generateCoord(args.coordenadas2)
	c3 = generateCoord(args.coordenadas3)
	r1 = float(args.ratio1)
	r2 = float(args.ratio2)
	r3 = float(args.ratio3)
	
	D1 = vincenty(c1,c2).kilometers
	D2 = vincenty(c1,c3).kilometers
	D3 = vincenty(c2,c3).kilometers
	# D1 = great_circle(c1,c2).kilometers
	# D2 = great_circle(c1,c3).kilometers
	# D3 = great_circle(c2,c3).kilometers
		
	checkValues(r1, r2, r3, D1, D2, D3)

	h1 = getHeight(D=D1,r1=r1,r2=r2)
	n1 = getCat(hip=r1,cat=h1)
	h2 = getHeight(D=D2,r1=r1,r2=r3)
	m2 = getCat(hip=r1,cat=h2)

	gkmlat = (float(c1[0]),     float(c1[1])+1.0)
	gkmlon = (float(c1[0])+1.0, float(c1[1]))

	gradeKmLat = vincenty( c1 , gkmlat ).kilometers
	gradeKmLon = vincenty( c1 , gkmlon ).kilometers

	newLat = float(c1[0]) + (float(n1)/float(gradeKmLat) )
	newLon = float(c1[1]) + (float(m2)/float(gradeKmLon) )
	newCoord= (newLat,newLon)

	#print ("D1 = "+str(D1)+"  \nD2 = "+str(D2)+"  \nD3 = "+str(D3)+"\nn1 = "+str(n1)+"\nm2 = "+str(m2) + "\ngradeKmLat = "+str(gradeKmLat)+"\ngradeKmLon = "+str(gradeKmLon) +"\n")	
	print("Calulated points:")
	print ("[Red]\t c1 = ("+args.coordenadas1+") \n[Green]\t c2 = ("+args.coordenadas2+") \n[Blue]\t c3 = ("+args.coordenadas3+") \n[Yellow] c0 = ("+str(newCoord)+")")

	drawMap(c1,c2,c3,newCoord)


def main():
		args = get_args()	
		getCoords(args)

		
if __name__ == "__main__":
    main()
