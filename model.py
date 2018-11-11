from rssimap_app import db

class Points(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)
	rssi = db.Column(db.Integer)
	pdop = db.Column(db.Float)
	sat = db.Column(db.Integer)
	device = db.Column(db.String)
	timestamp = db.Column(db.DateTime)
