from flask import Flask
from sqlalchemy import create_engine


app = Flask(__name__)


@app.route('/')
def dashboard():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    engine = create_engine('mysql+pymysql://sat:123@172.17.0.1:3306/satellites', echo=True)
    connection = engine.connect()
