# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > dt.date(2016, 8, 22)).order_by(measurement.date).all()

    session.close()
    
    all_results = []
    for date, prcp in results:
        results_dict = {}
        results_dict["date"] = date
        results_dict["prcp"] = prcp
        all_results.append(results_dict)
    return jsonify(all_results)
        
    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > dt.date(2016, 8, 22)).\
    filter(measurement.station == 'USC00519281').all()
    
    session.close()
    active_station = list(np.ravel(results))
    return jsonify(active_station)           
           

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).all()

    session.close()
    
    all_results = []
    for date, tobs in results:
        results_dict = {}
        results_dict["date"] = date
        results_dict["tobs"] = tobs
        all_results.append(results_dict)
    
    for temp in all_results:
        search_term = temp["tobs"]
        if search_term == start:
            return jsonify(all_results)
    
    
#@app.route("/api/v1.0/<start>/<end>")
#def start_end_date(start, end):
#    session = Session(engine)
   

if __name__ == '__main__':
    app.run(debug=True)