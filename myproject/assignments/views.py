from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher
# from myproject.students.forms import 

assignments_blueprint = Blueprint('assignments', __name__ , template_folder='templates/assignments')


@assignments_blueprint.route('/home_assignment',  methods=['GET', 'POST'])
def home_assignment():
    return render_template('home_assignment.html' , teacherLoggedIn = g.teacherLoggedIn)


@assignments_blueprint.route('/description',  methods=['GET', 'POST'])
def description():
    return render_template('description.html' , teacherLoggedIn = g.teacherLoggedIn)

@assignments_blueprint.route('/add_assignment',  methods=['GET', 'POST'])
def add_assignment():
    return render_template('add_assignment.html' , teacherLoggedIn = g.teacherLoggedIn)

@assignments_blueprint.route('/update_assignments',  methods=['GET', 'POST'])
def update_assignment():
    return render_template('update_assignment.html' , teacherLoggedIn = g.teacherLoggedIn)

@assignments_blueprint.route('/delete_assignment',  methods=['GET', 'POST'])
def delete_assignment():
    return render_template('delete_assignment.html' , teacherLoggedIn = g.teacherLoggedIn)

@assignments_blueprint.route('/solve_assignment',  methods=['GET', 'POST'])
def solve_assignment():
    return render_template('solve_assignment.html' , teacherLoggedIn = g.teacherLoggedIn)


