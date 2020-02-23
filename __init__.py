from flask import Flask, jsonify, render_template

from config import Config
from models import init_db


app = Flask(__name__)
app.config.from_object(Config)

db_session = init_db(app)


@app.route('/')
def dashboard():
    time_measurement = measure_time()
    return render_template(
        'dashboard.html',
        time_measurement=time_measurement
    )


def measure_time():
    """Task 1"""
    sql = """
        select
            min(measurement_dt) min,
            max(measurement_dt) max,
            max(measurement_dt) - min(measurement_dt) total,
            s.name
        from
            satellite_data sd
            inner join satellites s on sd.satellite_id = s.id
        group by
            sd.satellite_id
    """
    q = db_session.execute(sql)
    results = q.fetchall()
    return [{'label': m.name, 'y': m.total} for m in results]


@app.route('/task2/spot7')
def task2():
    sql = """
        select
            min(ionosphere) min_iono,
            max(ionosphere) max_iono,
            min(ndvi) min_ndvi,
            max(ndvi) max_ndvi,
            min(radiation) min_radiation,
            max(radiation) max_radiation,
            s.name
        from
            satellite_data sd
            inner join satellites s on sd.satellite_id = s.id
        where
            s.name = 'SPOT7'
        group by
            sd.satellite_id
    """
    q = db_session.execute(sql)
    results = q.fetchall()
    output = '\n'.join([f'{m.name}: IONO-{m.min_iono}/{m.max_iono}' for m in results])
    return jsonify(output)


@app.route('/task3')
def task3():
    sql = """
        select
            avg(ionosphere) avg_iono,
            avg(ndvi) avg_ndvi,
            avg(radiation) avg_radiation,
            s.name
        from
            satellite_data sd
            inner join satellites s on sd.satellite_id = s.id
        group by
            sd.satellite_id
    """
    q = db_session.execute(sql)
    results = q.fetchall()
    output = '\n'.join([f'{m.name}: IONO-{m.avg_iono}' for m in results])
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
