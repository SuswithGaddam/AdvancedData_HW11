#Dependencies
import pandas as pd
from datetime import datetime as dt, timedelta
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, desc, func

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#Flask class
from flask import Flask, jsonify

#Create an instance of flask class
app = Flask(__name__)

#Create an instance of create_engine
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#List available flask routes
@app.route("/")
def home():
    """Lists available routes"""
    return(
        f"You can choose one of the below routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

#Route 1: Precipitation Data
@app.route("/api/v1.0/precipitation")
def prcp():
    """Provides temperature observation from the last year in the JSON format"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # Calculate the date 1 year ago from today
    #Get the latest date to timedelta last 12 months
    current_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).all()[0][0]

    #convert to datetime to ude timedelta
    current_date = dt.strptime(current_date_str, '%Y-%m-%d')

    query_date = current_date - timedelta(days = 365)
    # Perform a query to retrieve the date and precipitation scores

    select = [Measurement.date, Measurement.prcp]
    prcp_data = session.query(*select).filter(Measurement.date >= query_date).all()
    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.DataFrame(prcp_data, columns = ['Date', 'Precipitation'])
    # Sort the dataframe by date
    prcp_dict = prcp_df.to_dict(orient = 'records')
    return jsonify(prcp_dict)

#Route 2: Stations List
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    station_data = session.query(Station.name, Station.station).all()
    station_df  = pd.DataFrame(station_data,columns=["Name", "ID"])
    station_dict = station_df.to_dict(orient='records')
    return jsonify(station_dict)

#Route 3: 
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    # Calculate the date 1 year ago from today
    #Get the latest date to timedelta last 12 months
    current_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).all()[0][0]

    #convert to datetime to ude timedelta
    current_date = dt.strptime(current_date_str, '%Y-%m-%d')

    query_date = current_date - timedelta(days = 365)
    sel = [Measurement.date, Measurement.tobs]
    tobs_data = session.query(*sel).filter((Measurement.date >= query_date)).all()
    tobs_df  = pd.DataFrame(tobs_data,columns=["Date", "Tobs"])
    tobs_dict= tobs_df.to_dict(orient='records')
    return jsonify(tobs_dict) 

#To run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)