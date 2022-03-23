from flask import Flask, render_template, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE'] = 'sqlite:///lyme.sqlite'

db = SQLAlchemy(app)

engine = create_engine("sqlite:///lyme.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)


LymeModel = Base.classes.ML_Demographic_LymeCase_HealthRank


@app.route('/')
def home():
    return render_template("index_test.html")

@app.route('/counties')
def counties():
    session = Session(engine)

    results = session.query(LymeModel.Lyme_Disease_Incidence_Reported).count()

    session.close()

    return results

# @app.route('/ML_Model', methods=['POST','GET'])
# def ml_model():
#     return render_template()


if __name__ == "__main__":
    app.run(debug=True)