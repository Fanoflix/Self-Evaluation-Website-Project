from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Courses

courses_blueprint = Blueprint('courses', __name__ , template_folder = 'templates/courses')

@courses_blueprint.route('/add_courses',  methods=['GET', 'POST'])
def add_courses():
    pass


