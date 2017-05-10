import re, time, os, math
from geopy.distance import vincenty




def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c1', '--coordenadas1', required=True, action='store', help='Coordenadas 1')
  parser.add_argument('-c2', '--coordenadas2', required=True, action='store', help='Coordenadas 2')
  parser.add_argument('-c3', '--coordenadas3', required=True, action='store', help='Coordenadas 3')
  my_args = parser.parse_args()
  return my_args


def getCoords():
	
	# c1 = args.c1
	# c2 = args.c2
	# c3 = args.c3

	c1 = (40.32, -3.8500)
	c2 = (40.32, -3.8400)
	c3 = (40.35, -3.85)

	D1 = vincenty(c1,c2).kilometers
	D2 = vincenty(c1,c3).kilometers

	r1 = 1.0
	r2 = 1.5
	r3 = 2.5

	h1 = getHeight(D=D1,r1=r1,r2=r2)
	n1 = getCat(hip=r1,cat=h1)
	
	h2 = getHeight(D=D2,r1=r1,r2=r3)
	m2 = getCat(hip=r1,cat=h2)

	print("D1 = "+str(D1)+"  \nD2 = "+str(D2)+"\nn1 = "+str(n1)+"\nm2 = "+str(m2) )

def getHeight(D,r1,r2):
	s = float((D+r1+r2)/2.0)
	if (s*(s-D)*(s-r1)*(s-r2) < 0):
		print("s    = "+str(s) )
		print("s-D  = "+str(s-D) )
		print("s-r1 = "+str(s-r1) )
		print("s-r2 = "+str(s-r2) )

	h = (2/D)*math.sqrt(s*(s-D)*(s-r1)*(s-r2))
	return h

def getCat(hip,cat):
	c = math.sqrt(hip*hip-cat*cat)
	return c

def main():
		# args = get_args_pos()	
		getCoords()
		
if __name__ == "__main__":
    main()
