# -*- coding: utf-8 -*-
#Dependencies Set up
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
measurement = Base.classes.measurement
station = Base.classes.station

#Flask Set up
app = Flask(__name__)


#Flask Routes
@app.route("/")
def home():
    return(
        f'Welcome to the home page! Here are a list of routes <br/>'
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
        f"<br/>"
        f"<br/>"
        f"Note that for dates, please enter YYYYMMDD Format"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine) #Created Session
    
    #Created the query
    data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= dt.date(2016,8,23))
    
    session.close()
    
    prec_dict ={}
    for date, prcp in data:
        prec_dict[f'{date}'] = prcp
    
    return jsonify(prec_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    data2 = session.query(station.station).all()
    
    session.close()
    
    all_stations = list(np.ravel(data2))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    data3 = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281"). \
            filter(measurement.date >= dt.date(2016,8,23))
    
    session.close()
    
    temp_dict ={}
    for date, tobs in data3:
        temp_dict[f'{date}'] = tobs
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def start_dates(start):
    
    year = start[0:4]
    month = start[4:6]
    day = start[6:8]
    session = Session(engine)
    
    data4 = session.query(measurement). \
            filter(measurement.date >= dt.date(int(year),int(month),int(day)))
            
    
    session.close()
    Temperatures = []
    for x in data4:
        Temperatures.append(x.tobs)
    
    min_temp = min(Temperatures)
    max_temp = max(Temperatures)
    mean_temp = round(np.mean(Temperatures),1)
    temp_summary_dict = {
        "Minimum Temperature (F)" : min_temp,
        "Maximum Temperature (F)" : max_temp,
        "Average Temperature (F)" : mean_temp
        }
    return jsonify(temp_summary_dict)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    startyear = start[0:4]
    startmonth = start[4:6]
    startday = start[6:8]
    endyear = end[0:4]
    endmonth = end[4:6]
    endday = end[6:8]
    
    session = Session(engine)
    
    data5 = session.query(measurement). \
            filter(measurement.date >= dt.date(int(startyear),int(startmonth),int(startday))).\
            filter(measurement.date <= dt.date(int(endyear),int(endmonth),int(endday)))
        
    session.close()
    
    Temperatures = []
    for x in data5:
        Temperatures.append(x.tobs)
    
    min_temp = min(Temperatures)
    max_temp = max(Temperatures)
    mean_temp = round(np.mean(Temperatures),1)
    temp_summary_dict = {
        "Minimum Temperature (F)" : min_temp,
        "Maximum Temperature (F)" : max_temp,
        "Average Temperature (F)" : mean_temp
        }
    return jsonify(temp_summary_dict)
if __name__ == "__main__":
    app.run(debug=True)
