#!/bin/bash

echo "Choose Python version: \n - Press 2 to install Python 2.x dependencies \n - Press any other key to install Python3.x dependencies \n - Write 'quit' to quit"

read opt	

if [ $opt = "2" ]; then
	echo 'Escenario avanzado'
    echo "Installing Python 2.x dependencies"
	# Python 2.x
	sudo apt-get install libgeos-3.6.2 libgeos-dev python-tk
	sudo pip install pyproj geopy numpy matplotlib geopy matplotlib plotly
	sudo pip install https://github.com/matplotlib/basemap/archive/master.zip

elif [ $opt = "quit" ]; then
	break

else
    echo "Installing Python 3.x dependencies"
	# Python 3.x
	sudo apt-get install libgeos-3.6.2 libgeos-dev python3-tk
	sudo pip3 install pyproj geopy numpy matplotlib geopy matplotlib plotly
	sudo pip3 install https://github.com/matplotlib/basemap/archive/master.zip
fi