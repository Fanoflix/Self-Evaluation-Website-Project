import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


# Often people will also separate these into a separate config.py file 
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

@app.before_first_request
def create_tables():
    db.create_all()

# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"

from myproject.students.views import students_blueprint
from myproject.teachers.views import teachers_blueprint
from myproject.assignments.views import assignments_blueprint
from myproject.leaderboard.views import leaderboard_blueprint
from myproject.search.views import search_blueprint

app.register_blueprint(students_blueprint,url_prefix='/students')
app.register_blueprint(teachers_blueprint,url_prefix='/teachers')
app.register_blueprint(assignments_blueprint,url_prefix='/assignments')
app.register_blueprint(leaderboard_blueprint,url_prefix='/leaderboard')
app.register_blueprint(search_blueprint,url_prefix='/search')