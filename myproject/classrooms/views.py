from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from flask_login import login_user,login_required,logout_user,current_user
from myproject import db,g
from myproject.models import Classroom, Assignments, Assignments_in_Classroom, Students_in_Classroom
from myproject.classrooms.form import AddClassroom, AddClassroomAssignments
from wtforms import RadioField,SubmitField, StringField, SelectField, Form, validators, DateTimeField
from myproject.search.form import Searching
import datetime 
from sqlalchemy import func, and_

day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

classrooms_blueprint = Blueprint('classrooms', __name__ , template_folder='templates/classrooms')

@classrooms_blueprint.route('/list',  methods=['GET', 'POST'])
def class_list():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    all_classrooms = []
    available_assignments = []
    all_classrooms = Classroom.query.filter_by(teacher_id = g.whichTeacher.id).all()
    total_assignments = []
    for classroom in all_classrooms:
        for assignment in  Assignments.query.filter_by(teacher_id = g.whichTeacher.id).all():
            assignment_exists = Assignments_in_Classroom.query.filter(
                                                                and_(
                                                                        Assignments_in_Classroom.classroom_id.like(classroom.id),
                                                                        Assignments_in_Classroom.assignment_id.like(assignment.id),
                                                                )
                ).first()
            if assignment_exists != None:
                available_assignments.append(assignment)
        
        total_assignments.append(available_assignments)

    return render_template('list_classrooms.html', all_classrooms = all_classrooms, total_assignments = total_assignments, teacher_object =  g.whichTeacher, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)

@classrooms_blueprint.route('/display_classroom/<classroom_id>',  methods=['GET', 'POST'])
def display_classroom(classroom_id):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    available_assignments = []
    for assignment in  Assignments.query.filter_by(teacher_id = g.whichTeacher.id).all():
        assignment_exists = Assignments_in_Classroom.query.filter(
                                                            and_(
                                                                    Assignments_in_Classroom.classroom_id.like(int(classroom_id)),
                                                                    Assignments_in_Classroom.assignment_id.like(assignment.id),
                                                            )
            ).first()
        if assignment_exists != None:
            available_assignments.append(assignment)

    all_deadline_dates = []
    all_deadline_days = []
    for assignment in available_assignments:
        deadline = Assignments_in_Classroom.query.filter_by(assignment_id = assignment.id).first().deadline
        date=str(deadline)
        day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
        all_deadline_days.append(day_name[day])
        all_deadline_dates.append(deadline)
    
    #all the students displayed here
    return render_template('display_classroom.html', classroom_id = int(classroom_id), all_deadline_days = all_deadline_days, all_deadline_dates = all_deadline_dates, available_assignments = available_assignments, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)

@classrooms_blueprint.route('/add_classroom',  methods=['GET', 'POST'])
def add_classroom():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = AddClassroom()
    if form.validate_on_submit():
        class_name = form.class_name.data
        new_class = Classroom(class_name, g.whichTeacher.id)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('classrooms.class_list'))
    return render_template('add_classroom.html', form = form, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)

@classrooms_blueprint.route('/add_classroom_assignments/<classroom_id>',  methods=['GET', 'POST'])
def add_classroom_assignments(classroom_id):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    classroom_id = int(classroom_id)
    #available_assignments are those assignments owned by the teacher adding the classroom
    #so he can only add his own assignments in the classroom with a deadline
    #work similar to courses in add_assignment (set attribute)

    #Checks if the assignment is already in the classroom so it doesnt display it as a choice because SQL insertion error ajayega warna
    all_assignments = []
    for assignment in  Assignments.query.filter_by(teacher_id = g.whichTeacher.id).all():
        assignment_exists = Assignments_in_Classroom.query.filter(
                                                            and_(
                                                                    Assignments_in_Classroom.classroom_id.like(int(classroom_id)),
                                                                    Assignments_in_Classroom.assignment_id.like(assignment.id),
                                                            )
            ).first()
        if assignment_exists == None:
            all_assignments.append(assignment)
    
    available_assignments = SelectField("Assignments", [validators.Required()], choices = [(assignment.id, assignment.assignment_name) for assignment in all_assignments])
    setattr(AddClassroomAssignments, 'available_assignments', available_assignments)
    deadline = DateTimeField("Deadline", [validators.Required()])
    setattr(AddClassroomAssignments, 'deadline', deadline)
    setattr(AddClassroomAssignments, 'submit', SubmitField('Add Assignment to classroom') )
    
    
    form = AddClassroomAssignments()

    if form.validate_on_submit():
        assignment_id = form.available_assignments.data
        deadline = form.deadline.data
        new_assignment_in_classroom = Assignments_in_Classroom(int(classroom_id), assignment_id, deadline)
        db.session.add(new_assignment_in_classroom)
        db.session.commit()
        return redirect(url_for('classrooms.display_classroom', classroom_id = int(classroom_id)))
    return render_template('add_classroom_assignment.html', form = form, classroom_id = classroom_id, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)
