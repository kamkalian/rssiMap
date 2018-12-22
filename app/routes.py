from flask import render_template
from app import app
from app.model import Point
from flask import json

@app.route('/')
@app.route('/index')
def index():
	points = Point.query.group_by(Point.lat, Point.lon).all()

	# Die einzelnen Punkte werden in ein geoJson verpackt und der leaflet Karte in der index.html übergeben.
	# Das geoJson kommt jetzt über to_dict() vom Model. Mehrere Points werden in eine Liste gesteckt.
	geo_json = []
	for p in points:
		geo_json.append(p.to_dict())

	return render_template('index.html', title=u'Freifunk RSSI Map', rssiPoints=json.dumps(geo_json), points=points)
