from flask import render_template
from rssimap_app import app, db
from rssimap_app.model import Points
import math
import decimal
import time


@app.route('/')
@app.route('/index')
def index():
	points = Points.query.group_by(Points.lat,Points.lon).all()

	lat_step = 0.00002695686901 #Für die Entfernung bei Latitude von 3m wurde ein Step ausgerechnet
	#lat_step = 0.00002695686901
	diameter = 3 #Durchmesser eines Punktes auf der Karte in Meter
	lat = 0.0
	lon = 0.0

	decimal.getcontext().prec = 6

	#Die einzelnen Punkte werde in ein geoJson verpackt und der leaflet Karte in der index.html übergeben.
	geo_json = "["
	for p in points:

		#Hier werden die Koordinaten der Points vorbereitet, damit sie auf der Kerte geordnet angezeigt werden.
		uErde = ((2*math.pi*6378*math.cos(math.radians(p.lat)))*1000)
		lon_step = (360*diameter)/uErde

		lat = p.lat - math.fmod(p.lat, lat_step)
		lon = p.lon - math.fmod(p.lon, lon_step)

		lat = decimal.Decimal(lat)
		lon = decimal.Decimal(lon)

		if(points.index(p)>0) and (points.index(p)<len(points)):
			geo_json += ","
		geo_json += "{ 'type':'Point', 'rssi':'"+str(p.rssi)+"', 'coordinates':["+str(lon)+","+str(lat)+"]}"

	geo_json += "]"
	#rssiPoints="[{ 'type': 'Point', 'rssi':'-30', 'coordinates': [7.114578, 50.830734]}, { 'type': 'Point', 'rssi':'-60', 'coordinates': [7.114578, 50.830653]}]"
	return render_template('index.html', title=u'Freifunk RSSI Map', rssiPoints=geo_json, points=points)


@app.route('/addPoint')
def addPoint():
	print("test")

