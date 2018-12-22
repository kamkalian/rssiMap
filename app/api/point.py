from app.api import bp
from app import db
from app.model import Point
from flask import jsonify
from flask import request
from math import sqrt
import datetime


@bp.route('/points/<float:lat>:<float:lon>:<int:distance>', methods=['GET'])
def get_points(lon, lat, distance):
    points = Point.query.group_by(Point.lat, Point.lon).all()
    geo_json = []
    for p in points:
        dx = 71500 * (lon - p.lon)
        dy = 111300 * (lat - p.lat)
        dist = sqrt(dx * dx + dy * dy)
        print(dist)

        if dist < distance:
            geo_json.append(p.to_dict())

    return jsonify(geo_json)


@bp.route('/points', methods=['POST'])
def input_points():
    data = request.get_json() or {}

    try:
        lat = data['lat']
        lon = data['lon']
        rssi = data['rssi']
        pdop = data['pdop']
        sat = data['sat']
        token = data['token']

        dt = datetime.datetime.now()

        if token == "E3xte.rna0lEnUcloSsurBe":
            point = Point(lat=lat, lon=lon, rssi=rssi, pdop=pdop, sat=sat, timestamp=dt)
            db.session.add(point)
            db.session.commit()
            response = jsonify('success')
            response.status_code = 201
        else:
            response = jsonify('invalid token')
            response.status_code = 400

    except KeyError:
        response = jsonify('bad request')
        response.status_code = 400

    return response
