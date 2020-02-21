# satellites

## Connecting to MySQL
Two options exist for looking at the MySQL database:

### Use Adminer
1. Go to http://127.0.0.1:8080/?server=127.0.0.1%3A3306&username=sat&db=satellites
2. Enter the password: `123`

### Connect to the Docker container
```bash
$ docker exec -it satellites_db_1 mysql -usat -p123
...
mysql>
```
