from flask import Flask, redirect, url_for, render_template, request, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
import sqlite3 as sql
from ml import load_file

# Initiate Flask App
app = Flask(__name__)

# Import ML Models
brfmodel = load_file('brfmodel.pkl')

df = pd.DataFrame([{
    'Average_Health_Rank': 15.3,
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
    'Ticks_With_Lyme': 0}
])

engine = create_engine("sqlite:///lyme.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Cw = Base.classes.combo_wombo


@app.route('/')
def home():
    # prediction = brfmodel.predict(df)
    # print('------------')
    # print(prediction)
    # print('------------')
    con = sql.connect("lyme.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    # # if state_county:
    #     cur.execute(
    #         f"select * from combo_wombo WHERE State={state_county['state']} AND County={state_county['county']}")
    # # else:
    cur.execute("select * from combo_wombo")
    datas = cur.fetchall()
    return render_template("fips.html", datas=datas)


# @app.route('/fetch/<string:fips>', methods=['POST', 'GET'])
# def fetch(fips):
#     state = request.form['st']
#     county = request.form['cnty']
#     if request.method == 'POST':
#         session = Session(engine)
#         results = session.query(Cw.County).filter(Cw.FIPS == fips)

#         return render_template('index.html', datas=datas)

# @app.route("/index/<string:fips>", methods=['POST', 'GET'])
# def find_county(fips):
#     if request.method == 'POST':
#         state = request.form['st']
#         con = sql.connect("lyme.sqlite")
#         cur = con.cursor()
#         datas = cur.execute(
#             "SELECT * FROM combo_wombo WHERE STATE=?", (state))
#         return render_template("fips.html", datas=datas[0])
#     con = sql.connect("lyme.sqlite")
#     con.row_factory = sql.Row
#     cur = con.cursor()
#     cur.execute("SELECT * FROM combo_wombo WHERE FIPS=?", (fips,))
#     datas = cur.fetchone()
#     return render_template("fips.html", datas=datas[0])


# @app.route('/select/<string:fips>', methods=['POST', 'GET'])
# def state(fips):
#     if request.method == 'POST':
#         state = request.form['st']
#         county = request.form['cnty']
#         if state and county:
#             state_county = {'state': state, 'county': county}
#         else:
#             state_county = None
#         # con = sql.connect("lyme.sqlite")
#         # cur = con.cursor()
#         # cur.execute(
#         #     "SELECT * FROM combo_wombo WHERE STATE=?, COUNTY=?", (state,
#         #                                                           county))

#         return redirect("/")

@app.route('/data')
def get_data():
    session = Session(engine)
    result = session.query(Cw.State,
                           Cw.County,
                           Cw.Avg_Health_Rank,
                           Cw.Population,
                           Cw.Minors_Population,
                           Cw.Senior_Population,
                           Cw.Income,
                           Cw.African_American,
                           Cw.Native_Indian,
                           Cw.Asian,
                           Cw.Pacific_Islander,
                           Cw.Hispanic,
                           Cw.Caucasian,
                           Cw.Female,
                           Cw.Rural,
                           Cw.Life_Expectancy,
                           Cw.Number_of_Deaths,
                           Cw.Lat,
                           Cw.Long,
                           Cw.Ticks_With_Lyme
                           ).all()
    cols = ['State',
            'County',
            'Avg_Health_Rank',
            'Population',
            'Minors_Population',
            'Senior_Population',
            'Income',
            'African_American',
            'Native_Indian',
            'Asian',
            'Pacific_Islander',
            'Hispanic',
            'Caucasian',
            'Female',
            'Rural',
            'Life_Expectancy',
            'Number_of_Deaths',
            'Lat',
            'Long',
            'Ticks_With_Lyme']

    temp_df = pd.DataFrame(result, columns=cols)

    final_result = temp_df.to_dict('records')
    session.close()
    return jsonify(final_result)

# @app.route('/info/<text:st>')
# def retrieve_data(st):
#     session = Session(engine)
#     state = session.query(LymeTable).filter(LymeTable.State == st)
#     if request.method == 'POST':
#         try:
#             datas = session.query(LymeTable.Average_Health_Rank,
#                                   LymeTable.Population,
#                                   LymeTable.Minors_Population,
#                                   LymeTable.Senior_Population,
#                                   LymeTable.Income,
#                                   LymeTable.African_American,
#                                   LymeTable.Native_Indian,
#                                   LymeTable.Asian,
#                                   LymeTable.Pacific_Islander,
#                                   LymeTable.Hispanic,
#                                   LymeTable.Caucasian,
#                                   LymeTable.Female,
#                                   LymeTable.Rural,
#                                   LymeTable.Life_Expectancy,
#                                   LymeTable.Number_of_Deaths,
#                                   LymeTable.Lat,
#                                   LymeTable.Long,
#                                   LymeTable.Ticks_With_Lyme).all()
#         except:
#             print(f' Could not render {datas}: 404')


if __name__ == "__main__":
    app.run(debug=True)
