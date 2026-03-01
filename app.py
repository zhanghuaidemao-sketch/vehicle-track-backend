# -*- coding: utf-8 -*-
import math
import requests
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# 高德地图API KEY（填你自己的）
GAODE_API_KEY = '835646d2a34ab928aa8c50d49e8aea76'


# ================= 坐标转换 =================
def wgs84_to_gcj02(lng, lat):

    def out_of_china(lng, lat):
        return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)

    def transform_lat(lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 * math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lng(lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
        ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * math.pi) + 40.0 * math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 * math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
        return ret

    if out_of_china(lng, lat):
        return lng, lat

    a = 6378245.0
    ee = 0.00669342162296594323

    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)

    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)

    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)

    mglat = lat + dlat
    mglng = lng + dlng

    return mglng, mglat


# ================= 轨迹接口 =================
@app.route('/api/track')
def track():

    track_points = [
        {"lat": 32.650906, "lng": 110.739725, "timestamp": "2024-01-01T10:00:00", "speed": 10},
        {"lat": 32.652000, "lng": 110.745000", "timestamp": "2024-01-01T10:05:00", "speed": 12},
        {"lat": 32.654000, "lng": 110.755000", "timestamp": "2024-01-01T10:10:00", "speed": 8},
        {"lat": 32.656000, "lng": 110.765000", "timestamp": "2024-01-01T10:15:00", "speed": 15},
        {"lat": 32.662013, "lng": 110.808914", "timestamp": "2024-01-01T10:45:00", "speed": 6}
    ]

    return jsonify(track_points)


# ================= 启动方式（必须这样） =================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
