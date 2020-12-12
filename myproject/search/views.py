from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher, Assignments, Courses, Assignment_Data
from sqlalchemy import and_, or_, not_


search_blueprint = Blueprint('search', __name__ , template_folder='templates/search')

@search_blueprint.route('/search' , methods = ['GET' , 'POST'])
def searching():
    

    assignment = Assignments.query.filter_by(assignment_name = g.searchForm.searched.data).first()
    ref_teacher = Assignments.query.filter_by(teacher_id = assignment.teacher_id)
    
    student = Student.query.filter(
        or_(
            Student.student_fname.like( g.searchForm.searched.data),
            Student.student_lname.like( g.searchForm.searched.data),
            Student.student_uname.like( g.searchForm.searched.data),
        )
    )

    teacher = Teacher.query.filter(
        or_(
            Teacher.teacher_fname.like( g.searchForm.searched.data),
            Teacher.teacher_lname.like( g.searchForm.searched.data),
            Teacher.teacher_uname.like( g.searchForm.searched.data),
        )
    )
    
    
    if g.searchForm.validate_on_submit():
        return redirect(url_for('search.searching'))
    
    
    return render_template('results.html' ,searchForm = g.searchForm , teacher = teacher , student = student , assignment= assignment , ref_teacher = ref_teacher)
