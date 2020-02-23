from collections import Counter

from flask import Flask, jsonify, render_template

from config import Config
from models import init_db, SatelliteData


app = Flask(__name__)
app.config.from_object(Config)

db_session = init_db(app)


class SatMeasure:
    def __init__(self, details, data_set):
        self.name = details.name
        self.metric = details.metric
        self.data_set = data_set

    @property
    def time_invested(self):
        times = [n.measurement_dt for n in self.data_set]
        elapsed = str(max(times) - min(times))
        hours, mins, secs = elapsed.split(':')

        if int(hours) > 0:
            return f'{hours}h{mins}min'

        return f'{mins}min'

    @property
    def ionosphere(self):
        return [n.ionosphere for n in self.data_set]

    @property
    def ndvi(self):
        return [n.ndvi for n in self.data_set]

    @property
    def radiation(self):
        return [n.radiation for n in self.data_set]

    @property
    def measurement(self):
        return [n.measurement for n in self.data_set]

    @property
    def metric_measure(self):
        if self.metric.lower() == 'vegetation classification':
            return {val: occ for val, occ in Counter(self.measurement).items()}

        # metric is 'earth altitude' or 'sea salinity'
        # display is basically the same for either
        metrics = [{
            'x': n.measurement_dt.isoformat(),
            'y': n.measurement,
        } for n in self.data_set]
        return sorted(metrics, key=lambda n: n['x'])


@app.route('/')
def dashboard():
    all_data = db_session.query(SatelliteData).all()
    data_by_sat = {}

    for row in all_data:
        data_by_sat.setdefault(row.satellite, []).append(row)

    sats = []
    for sat, data in data_by_sat.items():
        sats.append(SatMeasure(sat, data))

    measures = get_satellite_details(sats)

    return render_template(
        'dashboard.html',
        time_measurement={sat.name: sat.time_invested for sat in sats},
        measures=measures,
        averages=get_category_averages(measures),
    )


def get_satellite_details(satellites):
    return {sat.name: {
        'Ionosphere': {
            'min': min(sat.ionosphere),
            'max': max(sat.ionosphere),
            'avg': sum(sat.ionosphere) / len(sat.ionosphere),
        },
        'NDVI': {
            'min': min(sat.ndvi),
            'max': max(sat.ndvi),
            'avg': sum(sat.ndvi) / len(sat.ndvi),
        },
        'Radiation': {
            'min': min(sat.radiation),
            'max': max(sat.radiation),
            'avg': sum(sat.radiation) / len(sat.radiation),
        },
        sat.metric: sat.metric_measure,
    } for sat in satellites}


def get_category_averages(satellites):
    cat_avgs = {}
    for sat_name, details in satellites.items():
        for metric, measurements in details.items():
            if metric in ['Ionosphere', 'NDVI', 'Radiation']:
                cat_avgs.setdefault(metric, {}).update({
                    sat_name: measurements['avg']
                })

    # sort by averages
    return {m: {
        s: v for s, v in sorted(d.items(), key=lambda n: n[1], reverse=True)
        } for m, d in cat_avgs.items()
    }

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