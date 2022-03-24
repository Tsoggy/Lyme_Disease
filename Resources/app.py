from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from ml import load_file

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE'] = 'sqlite:///lyme.sqlite'

db = SQLAlchemy(app)

engine = create_engine("sqlite:///lyme.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

LymeModel = Base.classes.ML_Demographic_LymeCase_HealthRank

model = load_file('SMOTEENN.pkl')

df = pd.DataFrame([{'FIPS': 19135,
 'Lifespan_Rank': 76,
 'Life_Quality_Rank': 83,
 'Health_Behaviors_Rank': 71,
 'Clinical_Care_Rank': 92,
 'Social_Economic_Factors_Rank': 71,
 'Physical_Environment_Rank': 80,
 'Population': 7845.0,
 '%<18_Yrs_Old': 24.04,
 '%65_Yrs_Old_and_over': 19.6,
 'Income($)': 520.47,
 'African_American(%)': 1.11,
 'American_Indian/Alaskan_Native(%)': 0.22,
 'Asian(%)': 0.45,
 'Native_Hawaiian/Other_Pacific_Islander(%)': 0.01,
 'Hispanic(%)': 3.0,
 'Non-Hispanic_White(%)': 94.25,
 'Female(%)': 50.29,
 'Rural(%)': 55.17,
 'Life_Expectancy': 76.58,
 'Deaths(Count)': 116.0,
 'Lat': 41.0298,
 'Long': -92.869,
 'Ticks_With_Lyme': 0,
 'Norm_Incidence': 0.0}
 ])
prediction = model.predict(df)


@app.route('/')
def home():
    print('==================')
    print(prediction)
    print('==================')
    return render_template("index_test.html")


@app.route('/signup', methods = ['POST'])
def signup():
    data = pd.DataFrame([request.form])
    print(data)
   
    return render_template('index_test.html')

@app.route('/counties')
def counties():
    session = Session(engine)

    results = session.query(LymeModel.Lyme_Disease_Incidence_Reported).all()
    parse_results = pd.DataFrame(results).to_dict('records')
    session.close()

    return jsonify(parse_results)

# @app.route('/ML_Model', methods=['POST','GET'])
# def ml_model():
#     return render_template()


if __name__ == "__main__":
    app.run(debug=True)
