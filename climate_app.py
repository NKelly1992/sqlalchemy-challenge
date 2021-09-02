# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

import numpy as np
import pandas as pd
import datetime as dt

from flask import flask

# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a database session object
session = Session(engine)

# Set up flask
app = Flask(__name__)

# date variables
date = dt.datetime(2017, 8, 23)
lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
year_ago = date - dt.timedelta(days=365)

# Set up routes
@app.route("/")
def welcome():
    return (
        f"Welcome to Honolulu, Hawaii!"
        f"/api/v1.0/precipitation displays the precipitation analysis in Honolulu over the past year"
        f"/api/v1.0/stations returns a list of weather stations from the dataset"
        f"/api/v1.0/tobs provides the temperature observations of the most active station for the last year of data"
        f"/api/v1.0/<start> gives the minimum temperature, the average temperature, and the maximum temperature for August 23, 2017"
        f"/api/v1.0/<start>/<end> gives the minimum temperature, the average temperature, and the maximum temperature for a given 12-month period"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= year_ago).group_by(Measurement.date).all()
    
    precip_data = []
    
    for day in precip_results:
        precip_dict = {}
        precip_dict[day.date] = day.prcp
        precip_data.append(precip_dict)
    
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.name).all()
    
    return jsonify(station_results)
    

@app.route("/api/v1.0/tobs")
def tobs():
    tob_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    return jsonify(tob_results)

@app.route("/api/v1.0/<start>")
def temperature(start):
    temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date)
    temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date)
    temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date)
    
    temp_dict = {}
    temp_dict["Average temperature"] = temp_avg
    temp_dict["Minimum temperature"] = temp_min
    temp_dict["Maximum temperature"] = temp_max
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):
    temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= year_ago).all()
    temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= year_ago).all()
    temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= year_ago).all()
    
    temp_dict = {}
    temp_dict["Average temperature"] = temp_avg
    temp_dict["Minimum temperature"] = temp_min
    temp_dict["Maximum temperature"] = temp_max
    
    return jsonify(temp_dict)

if __name__=="__main__":
    app.run(debug=True)