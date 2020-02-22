# satellites

## Connecting to MySQL
Two options exist for looking at the MySQL database:

### Use Adminer
1. Go to 127.0.0.1:8080/?server=172.17.0.1&username=sat&db=satellites
2. Enter the password: `123`

### Connect to the Docker container
```bash
$ docker exec -it satellites_db_1 mysql -usat -p123
...
mysql>
```
