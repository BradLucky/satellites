"""Main Flask app for presenting a dashboard of satellite data."""
from collections import Counter

from flask import Flask, jsonify, render_template

from config import Config
from models import init_db, SatelliteData


app = Flask(__name__)
app.config.from_object(Config)

db_session = init_db(app)


class SatMeasure:
    """Represents a single satellite and its full data
    set as well as some calculated data points.
    """
    def __init__(self, details, data_set):
        """`name` is the human-readable name
        `metric` is what this satellite uniquely measures
        """
        self.name = details.name
        self.metric = details.metric
        self.data_set = data_set

    @property
    def time_invested(self):
        """Return the length of time the satellite was over the area.

        This is calculated by taking the last measurement time and
        subtracting the first measurement time.

        The output is expressed with zero-padded hours and minutes,
        but only shows the hours if it is more than zero.
        """
        times = [n.measurement_dt for n in self.data_set]
        elapsed = str(max(times) - min(times))
        hours, mins, secs = elapsed.split(':')

        if int(hours) > 0:
            return f'{hours}h{mins}min'

        return f'{mins}min'

    @property
    def ionosphere(self):
        """Return a list of all ionosphere readings."""
        return [n.ionosphere for n in self.data_set]

    @property
    def ndvi(self):
        """Return a list of all NDVI readings."""
        return [n.ndvi for n in self.data_set]

    @property
    def radiation(self):
        """Return a list of all radiation readings."""
        return [n.radiation for n in self.data_set]

    @property
    def measurement(self):
        """Return a list of all unique metric readings."""
        return [n.measurement for n in self.data_set]

    @property
    def metric_measure(self):
        """Return graph-able data for the unique metric.

        If this satellite looks at the vegetation, we need to know
        how many time each type of vegetation is encountered.

        If this satellite measures earth altitude or sea salinity,
        we need to know the measurement at each point in time.
        """
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
    """Render and return the dashboard template.

    First, grab all the data from the database and convert that to a
    dictionary using the satellite details as the key and its data
    as the values.

    From there, create the SatMeasure classes for each satellite and use
    that list of satellites to calculate all the data for the dashboard.
    """
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
    """Return a satellite-keyed listing of aggregated measurements.

    Simply get the min() and max() for lowest and highest readings,
    and calculate the average, for Ionosphere, NDVI, and Radiation.

    For the unique metric for this satellite, simply use what was
    defined in the class based on the metric measured.
    """
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
    """Return all the averages per measurement in descending order."""
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')