# Satellite Data Dashboard

This project provides a means for viewing various data points in a graphical UI. The data are pulled from satellites and imported to a database.

The dashboard is built on the Bootstrap framework and is thus responsive. On a typical computer screen, the dashboard widgets will be two to a row, but as you decrease the screen width, they will move to one widget per row.

## Getting started
First, you need to clone this repo into a directory of your choosing. Also, you must have Docker installed and have some working knowledge of using Docker. All commands listed here are assumed to be run from the directory you clone to.

### Starting the container
```bash
$ docker-compose up --build
```
This will take a little while the first time, as a few images will need to be downloaded and/or built.

### Setting up the database
The database will initially be empty. After the MySQL container appears to be completely ready (should take a few minutes, but you'll eventually see the logging cease), you will need to run the following to build the database tables necessary. It will also populate the `satellites` table with the 4 initial satellites needed.
```bash
$ docker exec -i satellites_web_1 python db_init.py
```
Next, you will want to import the initial set of data.
```bash
$ docker exec -i satellites_web_1 python csv_import.py satDataCSV2.csv
```

## Connecting to MySQL
Two options exist for looking at the MySQL database (now that it is set up and worth looking at):

### Use Adminer
1. Go to http://127.0.0.1:8080/?server=172.17.0.1&username=sat&db=satellites
2. Enter the password: `123`

### Connect to the Docker container
```bash
$ docker exec -it satellites_db_1 mysql -usat -p123
...
mysql>
```

## Viewing the Dashboard
Open up http://127.0.0.1:5000/ in your browser.

## Running Unit Tests
```bash
$ docker exec -i satellites_web_1 pytest tests/test_app.py
```

## Development Details on this project
The following explains some of the approach taken for making this dashboard possible.

### Database Design
The database is a MySQL database, and contains 3 tables:

* `file_imports` - stores details from each imported file, including the start and end time and the imported filename.
* `satellites` - stores details about each satellite such as a unique identifier, human readable name, and a metric specific to said satellite.
* `satellite_data` - stores individual data points measured by each satellite over it's flyover of the area in question; it has foreign keys to both of the other tables (`file_import_id` and `satellite_id`) and lists out a few different measurements, including the metric specifically assigned to said satellite.

The tables are all defined within `models/__init__.py` for simple creation, but they are also mirrored by `CREATE` statements stored in `sql/db_setup.sql`. There are also some helper methods in `models/__init__.py` such as the CSV importer and DB initializer.

### Flask
The application is built using the Flask framework. There is one template file used to show the entire dashboard, and thus also only one route. All of the Flask setup is in `app.py` for simplicity.

### SatMeasure Class
There is one class to represent each satellite and its measurements. From this class, all of the metrics can be determined to show on the dashboard. After grabbing all the data from the `satellite_data` table, this class is instantiated for each satellite. Each calculation is documented within the docstrings of the class.