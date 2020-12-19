from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher, Assignments, Courses, Assignment_Data
from sqlalchemy import and_, or_, not_,func
from myproject.search.form import Searching


search_blueprint = Blueprint('search', __name__ , template_folder='templates/search')

@search_blueprint.route('/<searched>' , methods = ['GET' , 'POST'])
def searching(searched):
    
    searched = searched.lower()
    ref_teachers = None
    ref_assignments = None
    assignments = Assignments.query.filter(func.lower(Assignments.assignment_name) == searched).first()
    if assignments != None:
        ref_teachers = Assignments.query.filter_by(teacher_id = assignments.teacher_id)
    
    students = Student.query.filter(
        or_(
            (func.lower(Student.student_fname) == searched),
            (func.lower(Student.student_lname) == searched),
            (func.lower(Student.student_uname) == searched),
        )
    )

    teachers = Teacher.query.filter(
        or_(
            Teacher.teacher_fname.like( searched),
            Teacher.teacher_lname.like( searched),
            Teacher.teacher_uname.like( searched),
        )
    )

    courses = Courses.query.filter(func.lower(Courses.course_name) == searched).first()
    if courses != None:
        ref_assignments = Assignments.query.filter_by(course_id = courses.id)

    searchForm = Searching()
    if searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('results.html' ,searchForm = searchForm , teachers = teachers , students = students , assignments= assignments ,  courses = courses,ref_teachers = ref_teachers,ref_assignments = ref_assignments,teacherLoggedIn = g.teacherLoggedIn)
