# triangle-position
Triangle position given 3 coordinates and 3 radios or 4 coordinates and 4 radios

- *tripos.py*: triangulate ONE coordinate from 3 coordinates + 3 ratios

- *quapos.py*: triangulate one AREA calculating 4 points from the 4 coordinates + 4 ratios (like executing tripos.py 4 times with 4 coordinates)


## 3 coordinates

```
python tripos.py -c1 {coord_1} -c2 {coord_2} -c3 {coord_3} -r1 {ratio_1} -r2 {ratio_2} -r3 {ratio_3}
```

#### Example 1:

```
python tripos.py -c1 40.443580,-3.727077 -c2 40.452052,-3.725831 -c3 40.451418,-3.717722 -r1 0.65 -r2 0.75
-r3 0.65
```

![Screenshot](images/tri2.png)

Result using Plotly:

![Screenshot](images/tri5.png)

Result not using Plotly (Matplotlib does not need Access Token or API KEY is not a good option):

![Screenshot](images/tri1.png)

#### Example 2. Changing C3:

```
python tripos.py -c1 40.443580,-3.727077 -c2 40.452052,-3.725831 -c3 40.443587,-3.715664 -r1 0.65 -r2 0.75
-r3 0.65
```

![Screenshot](images/tri4.png)

Result using Plotly:

![Screenshot](images/tri6.png)

Result using Basemap:

![Screenshot](images/tri3.png)

--------------------------------------------

## 4 coordinates
```
python quapos.py -c1 {coord_1} -c2 {coord_2} -c3 {coord_3} -c4 {coord_4} -r1 {ratio_1} -r2 {ratio_2} -r3 {ratio_3}
-r4 {ratio_4}
```

### Example:

```
python quapos.py -c1 40.443587,-3.715664 -c2 40.451418,-3.717722 -c3 40.452052,-3.725831 -c4 40.443580,-3.727077
-r1 0.47 -r2 0.5 -r3 0.82 -r4 0.785
```

![Screenshot](images/quatri2.png)

Result using Basemap (calculated area in yellow):

![Screenshot](images/quatri1.png)

Result using Plotly:

![Screenshot](images/quatri3.png)


--------------------------------------------

## Installation

- Fill config.py with Plotpy username and API Key -> Visit https://plot.ly/Auth/login/?next=%2Fsettings to sign up, visit "API Keys" and click "Regenerate Key"

- Fill config.py with Mapbox Access Token -> Visit https://www.mapbox.com/signup/?route-to=%22/account/access-tokens%22 and copy the Access Token

- Run *sudo sh intall.sh* to install dependencies


## Note

Tested both in Python2.x (2.7.15rc1) and Python 3.x (3.6.7)
