# Satellite Data Dashboard

This project provides a means for viewing various data points in a graphical UI. The data are pulled from satellites and imported to a database.

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