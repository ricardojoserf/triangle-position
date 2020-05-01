import plotly.plotly as py
import plotly.graph_objs as go
import config


def sign_in(pyplot_user, pyplot_pass):
    py.sign_in(pyplot_user, pyplot_pass)


def createMap(points, mapbox_access_token):
    lats = []
    lons = []
    for c in points:
        lats.append(c[0])
        lons.append(c[1])
    lats_float = [float(n) for n in lats if n]
    lons_float = [float(n) for n in lons if n]
    lat_avge = sum(lats_float) / len(lats_float)
    lon_avge = sum(lons_float) / len(lons_float)
    counter = 0
    texts = []
    for i in lats_float:
        texts.append("Point C"+str(counter))
        counter += 1

    data = [
        go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=dict(
                size=16
            ),
            text=texts,
        )
    ]
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(lat=lat_avge,lon=lon_avge),
            pitch=0,
            zoom=12
        ),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='Multiple Mapbox')


def drawMap(points):
    mapbox_access_token = config.mapbox_access_token
    pyplot_user = config.pyplot_user
    pyplot_pass = config.pyplot_pass
    
    sign_in(pyplot_user, pyplot_pass)
    createMap(points, mapbox_access_token)
