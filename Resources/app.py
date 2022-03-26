from flask import Flask, redirect, url_for, render_template, request, jsonify
import pandas as pd
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ml import load_file

# Database setup
engine = create_engine("sqlite:///lyme.sqlite")

# Reflect existing db into model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to Demographics/Lyme Cases Table
LymeTable = Base.classes.ML_Demographic_LymeCase_HealthRank

# Initiate Flask App
app = Flask(__name__)

# Import ML Models
brfmodel = load_file('brfmodel.pkl')

df = pd.DataFrame([{
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


@app.route('/')
def home():
    prediction = brfmodel.predict(df)
    print('++++++++++')
    print(prediction)
    print('++++++++++')
    return render_template("index.html")


@app.route('/predict', methods=['POST', 'GET'])
def predictions():
    if request.method == "POST":
        data = request.form.get("county", "state")
        # float_features = [str(x) for x in data]
        # features = [np.array(float_features)]
        prediction = brfmodel.predict(df)
        # print('++++++++++')
        print(prediction)
        # print('++++++++++')
        try:
            session = Session(engine)

            results = session.query(LymeTable.County, LymeTable.State).filter(
                LymeTable.FIPS == data)
            parse_results = pd.DataFrame(results).to_dict('records')
            session.close()
            return redirect(url_for("index.html", prediction_text="The incidence of Lyme is {}".format(parse_results)))
        except:
            # data = pd.DataFrame([request.form])
            # print(data)

            return render_template('index.html', 404)


@app.route('/counties')
def counties():
    session = Session(engine)

    results = session.query(LymeTable.Norm_Incidence,
                            LymeTable.County, LymeTable.State, LymeTable.FIPS).all()
    session.close()
    county_summary = []
    for cases, county, state, fips in results:
        counties_dict = {}
        counties_dict['Incidences of Lyme Reported per 1000'] = cases
        counties_dict['County'] = county
        counties_dict['State'] = state
        counties_dict['FIPS'] = fips
        county_summary.append(counties_dict)

    return jsonify(county_summary)

# @app.route('/ML_Model', methods=['POST','GET'])
# def ml_model():
#     return render_template()


if __name__ == "__main__":
    app.run(debug=True)
