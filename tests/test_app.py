from app import get_category_averages, get_satellite_details


class FakeSat:
    name = 'SEAGULL8'
    ionosphere = [1, 2, 3]
    ndvi = [4, 5, 6]
    radiation = [7, 8, 9]
    metric = 'Carrion'
    metric_measure = 3


class TestDetails:
    def test_get_satellite_details(self):
        expected = {'SEAGULL8': {
            'Ionosphere': {'min': 1, 'max': 3, 'avg': 2},
            'NDVI': {'min': 4, 'max': 6, 'avg': 5},
            'Radiation': {'min': 7, 'max': 9, 'avg': 8},
            'Carrion': 3,
        }}

        assert expected == get_satellite_details([FakeSat])

    def test_category_averages(self):
        satellite_details = {
            'SEAGULL8': {
                'Ionosphere': {'min': 1, 'max': 3, 'avg': 2},
                'NDVI': {'min': 4, 'max': 6, 'avg': 5},
                'Radiation': {'min': 7, 'max': 9, 'avg': 8},
                'Carrion': 3,
            },
            'PIGEON77': {
                'Ionosphere': {'min': 3, 'max': 3, 'avg': 3},
                'NDVI': {'min': 1, 'max': 4, 'avg': 2},
                'Radiation': {'min': 4, 'max': 9, 'avg': 6},
                'Gerbils': 27,
            }
        }

        expected = {
            'Ionosphere': {'PIGEON77': 3, 'SEAGULL8': 2},
            'NDVI': {'SEAGULL8': 5, 'PIGEON77': 2},
            'Radiation': {'SEAGULL8': 8, 'PIGEON77': 6},
        }

        assert expected == get_category_averages(satellite_details)