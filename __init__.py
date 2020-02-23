from flask import Flask, jsonify, render_template

from config import Config
from models import init_db


app = Flask(__name__)
app.config.from_object(Config)

db_session = init_db(app)


@app.route('/')
def dashboard():
    time_measurement = measure_time()
    measures = min_max()
    return render_template(
        'dashboard.html',
        time_measurement=time_measurement,
        measures=measures,
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


def min_max():
    """Task 2"""
    sql = """
        select
            min(ionosphere) min_iono,
            max(ionosphere) max_iono,
            avg(ionosphere) avg_iono,
            min(ndvi) min_ndvi,
            max(ndvi) max_ndvi,
            avg(ndvi) avg_ndvi,
            min(radiation) min_radiation,
            max(radiation) max_radiation,
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
    return {
        m.name: {
            'ionosphere': {
                'min': m.min_iono,
                'max': m.max_iono,
                'avg': m.avg_iono,
            },
            'ndvi': {
                'min': m.min_ndvi,
                'max': m.max_ndvi,
                'avg': m.avg_ndvi,
            },
            'radiation': {
                'min': m.min_radiation,
                'max': m.max_radiation,
                'avg': m.avg_radiation,
            },
        } for m in results}


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
