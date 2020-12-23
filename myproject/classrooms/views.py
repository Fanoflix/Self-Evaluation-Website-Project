from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from flask_login import login_user,login_required,logout_user,current_user
from myproject import db,g
# from myproject.models import Student, Teacher, Settings
# from myproject.classrooms.forms import 
from myproject.search.form import Searching
# from sqlalchemy import func, and_

classrooms_blueprint = Blueprint('classrooms', __name__ , template_folder='templates/classrooms')

@classrooms_blueprint.route('/list',  methods=['GET', 'POST'])
def class_list():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('classrooms.html' ,searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)