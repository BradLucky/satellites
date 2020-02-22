FROM python:3.8-slim

COPY ./requirements.txt . 
RUN pip install -r requirements.txt

# mysqlclient is a more performant alternativei
# to pymysql, but costs more in container resources
# https://stackoverflow.com/a/46396881
#RUN apt-get install \\
#    default-libmysqlclient-dev \\
#    build-essential
#
#RUN pip install mysqlclient

COPY . /app

WORKDIR /app

ENTRYPOINT ["python"]
CMD ["__init__.py"]
