from flask import render_template
from app import app
from app.model import Point
from flask import json
from sqlalchemy import desc

@app.route('/')
@app.route('/index')
def index():
	points = Point.query.order_by(desc(Point.timestamp)).group_by(Point.lat, Point.lon).all()

	# Die einzelnen Punkte werden in ein geoJson verpackt und der leaflet Karte in der index.html übergeben.
	# Das geoJson kommt jetzt über to_dict() vom Model. Mehrere Points werden in eine Liste gesteckt.
	geo_json = []
	koords = []
	for p in points:
		geo_dict = p.to_dict()
		is_dublicate = False
		for k in koords:
			if geo_dict['coordinates'][0] == k[0]:
				if geo_dict['coordinates'][1] == k[1]:
					is_dublicate = True
			if is_dublicate:
				break

		if not is_dublicate:
			print(p.timestamp)
			koords.append(geo_dict['coordinates'])
			geo_json.append(geo_dict)

	return render_template('index.html', title=u'Freifunk RSSI Map', rssiPoints=json.dumps(geo_json), points=points)
