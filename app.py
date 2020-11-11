from flask import Flask
from models.teacher import Teacher
# from flask_restful import Api


app = Flask(__name__)
app.secret_key = '_fano'


if __name__ == "__main__":
    Teacher.findbytid(1)
# api = Api(app)