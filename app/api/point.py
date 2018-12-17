from app.api import bp
from app.model import Point
from flask import jsonify
from flask import request
from math import sqrt


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
    data = request.get_json() or []
    print(data)
    response = jsonify(data)
    response.status_code = 201
    return response