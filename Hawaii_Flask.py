import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#Setting up Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

#Reflecting an existing database
Base = automap_base()

#reflecting the tables
Base.prepare(engine, reflect=True)

#Saving on to the tables
Measure= Base.classes.measurement
Station = Base.classes.station

#Create session with python on to the Data Base
session = Session(engine)


#_____________________Setting up Flask______________________________________

app = Flask(__name__)

@app.route("/")
def echo():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of dates and percipitation observations from the last year<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of Temperature Observations (tobs) for the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range, inclusive<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Date 12 months ago
    p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= last_twelve_months).group_by(Measurement.date).all()
    return jsonify(p_results)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations_results = session.query(Station.station, Station.name).all()
    return jsonify(s_results)


# /api/v1.0/tobs
# Return a JSON list of Temperature for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    temp_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= last_twelve_months).all()
    return jsonify(t_results)


# /api/v1.0/<start>
# Return a JSON list of the minimum,average and the max temperature for a given start or start-end.
# When given the start only, calculate MIN, AVG, and MAX. For all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(day_temp_results)


# /api/v1.0/<start>/<end>
# Return a JSON list of the minimum,average, and the max temperature for a given start or start-end.
# When given the start and the end date, calculate the MIN, AVG, and MAX. For dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == "__main__":
    app.run(debug=True)
