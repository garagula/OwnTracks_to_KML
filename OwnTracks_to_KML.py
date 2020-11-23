#!/usr/bin/env python

import json
import pprint
import urllib
from flask import Flask, request
from textwrap import dedent

# KML Template
HEADER = """\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:kml="http://www.opengis.net/kml/2.2">
<Document>
    <Folder>
        <name>OwnTracks</name>
"""
ENTRY = """\
        <Placemark>
            <name>{device_id}</name>
            <Point>
                <coordinates>{lon},{lat},{alt}</coordinates>
                <altitudeMode>relativeToGround</altitudeMode>
            </Point>
        </Placemark>
"""
FOOTER = """\
    </Folder>
</Document>
</kml>
"""

app = Flask(__name__)

@app.route('/', methods=['POST'])  # GET requests will be blocked
def owntracks():
    req_data = request.get_json()
    print(req_data) # useful for debugging
    device_id = req_data["topic"].split("/")[2]

    with open("E:\\owntracks.kml", "w") as f:

        f.write(dedent(HEADER))
        lat = req_data["lat"]
        lon = req_data["lon"]
        alt = req_data["alt"]
        lines = dedent(ENTRY.format(device_id=device_id, lat=lat, lon=lon, alt=alt)).splitlines()
        for line in lines:
            f.write(f"{' ' * 8}{line}\n")
        f.write(dedent(FOOTER))

        return "ok"

app.run(host='0.0.0.0', debug=True, port=5000)