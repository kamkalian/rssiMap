import math

from app import db


class Point(db.Model):
	__tablename__ = 'point'
	id = db.Column(db.Integer, primary_key=True)
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)
	rssi = db.Column(db.Integer)
	pdop = db.Column(db.Float)
	sat = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)

	def to_dict(self):
		lat_step = 0.00002695686901  # Für die Entfernung bei Latitude von 3m wurde ein Step ausgerechnet
		diameter = 3  # Durchmesser eines Punktes auf der Karte in Meter

		u_earth = ((2 * math.pi * 6378 * math.cos(math.radians(self.lat))) * 1000)
		lon_step = (360 * diameter) / u_earth

		lat = self.lat - math.fmod(self.lat, lat_step)
		lon = self.lon - math.fmod(self.lon, lon_step)

		data = {
			'type': 'Point',
			'rssi': str(self.rssi),
			'coordinates': [lon, lat]
		}
		return data
