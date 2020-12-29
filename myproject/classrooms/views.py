from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from flask_login import login_user,login_required,logout_user,current_user
from myproject import db,g
from myproject.models import Classroom, Assignments, Assignments_in_Classroom, Students_in_Classroom,Assignment_Data,Solved_Classroom_Assignment
from myproject.classrooms.form import AddClassroom, AddClassroomAssignments, StudentJoinClassroom, DeleteClassroomAssignment,SolveClassAssignment
from wtforms import RadioField,SubmitField, StringField, SelectField, Form, validators
from wtforms.fields.html5 import DateTimeLocalField
from myproject.search.form import Searching
import datetime 
from sqlalchemy import func, and_

day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

classrooms_blueprint = Blueprint('classrooms', __name__ , template_folder='templates/classrooms')


@classrooms_blueprint.route('/teacher_classrooms',  methods=['GET', 'POST'])
def teacher_class_list():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    temp = []
    total_assignments = []
    all_classrooms = []
    available_assignments = []
    all_classrooms = Classroom.query.filter_by(teacher_id = g.whichTeacher.id).all()

    for classroom in all_classrooms:
        for assignment in  Assignments.query.filter_by(teacher_id = g.whichTeacher.id).all():
            assignment_exists = Assignments_in_Classroom.query.filter(
                                                                and_(
                                                                        Assignments_in_Classroom.classroom_id.like(classroom.id),
                                                                        Assignments_in_Classroom.assignment_id.like(assignment.id),
                                                                )
                ).first()
            if assignment_exists != None:
                today = datetime.datetime.today()
                #calculate duedate here
                deadline = Assignments_in_Classroom.query.filter_by(assignment_id = assignment.id).first().deadline
                
                check_month_year_today = today.strftime("%Y-%m")
                check_month_year_deadline = deadline.strftime("%Y-%m")
           

                if check_month_year_today == check_month_year_deadline:
                    if ( (int(deadline.strftime("%d")) - int(today.strftime("%d"))) <= 7) and ( (int(deadline.strftime("%d")) - int(today.strftime("%d"))) >= 0):
                        date=str(deadline)
                        day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
                        temp.append(assignment.assignment_name)
                        temp.append(deadline.strftime("%I:%M %p"))
                        temp.append(day_name[day])
                        available_assignments.append(temp)
                        temp = []
        
        total_assignments.append(available_assignments)
        available_assignments = []
    
    return render_template('teacher_list_classrooms.html', all_classrooms = all_classrooms, total_assignments = total_assignments, teacher_object = g.whichTeacher, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)

@classrooms_blueprint.route('/student_classrooms',  methods=['GET', 'POST'])
def student_class_list():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    temp = []
    total_assignments = []
    all_classrooms = []
    available_assignments = []

    classrooms = Students_in_Classroom.query.filter_by(student_id = current_user.id).all()

    for classroom in classrooms:
        #looping through all classes
        #if student exists in that class append that class to all_classrooms[]
        temp.append(classroom.classroom.id)
        temp.append(classroom.classroom.classroom_name)
        temp.append(classroom.classroom.teacher.teacher_fname)
        temp.append(classroom.classroom.teacher.teacher_lname)
        temp.append(classroom.classroom.teacher.teacher_uname)
        all_classrooms.append(temp)
        temp = []

    for classroom in classrooms:
        for assignments in Assignments_in_Classroom.query.filter_by(classroom_id = int(classroom.classroom_id)).all():

            assignment_already_solved = Solved_Classroom_Assignment.query.filter(
                                    and_(
                                            Solved_Classroom_Assignment.classroom_id.like(classroom.classroom.id),
                                            Solved_Classroom_Assignment.assignment_id.like(assignments.assignment_id),
                                            Solved_Classroom_Assignment.student_id.like(current_user.id),
                                    )
                                ).first()
                
            today = datetime.datetime.today()
            deadline = assignments.deadline
            
            check_month_year_today = today.strftime("%Y-%m")
            check_month_year_deadline = deadline.strftime("%Y-%m")
        

            if check_month_year_today == check_month_year_deadline and assignment_already_solved == None:
                if ( (int(deadline.strftime("%d")) - int(today.strftime("%d"))) <= 7) and ( (int(deadline.strftime("%d")) - int(today.strftime("%d"))) >= 0):
                    date=str(assignments.deadline)
                    day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
                    temp.append(assignments.assignment.id)
                    temp.append(assignments.assignment.assignment_name)
                    temp.append(deadline.strftime("%I:%M %p"))
                    temp.append(day_name[day])
                    available_assignments.append(temp)
                    temp = []
        
        total_assignments.append(available_assignments)
        available_assignments = []

    return render_template('student_list_classrooms.html', all_classrooms = all_classrooms, total_assignments = total_assignments, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)


@classrooms_blueprint.route('/join_classroom/<teacher_id>',  methods=['GET', 'POST'])
def join_classroom(teacher_id):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    all_classrooms = Classroom.query.filter_by(teacher_id = int(teacher_id)).all()
    return render_template('join_classroom.html' , searchForm = searchForm , all_classrooms = all_classrooms)



# display contents of classrooms
@classrooms_blueprint.route('/display_classroom/<classroom_id>',  methods=['GET', 'POST'])
def display_classroom(classroom_id):
    inClass = False
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))


    classroom_owner_id = Classroom.query.filter_by(id = int(classroom_id)).first().teacher_id
    available_assignments = []

    #loop to calculate all the assignments in that classroom
    for assignment in  Assignments.query.filter_by(teacher_id = classroom_owner_id).all():
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
    #loop to calculate all the days/dates in that classroom
    for assignment in available_assignments:
        deadline = Assignments_in_Classroom.query.filter_by(assignment_id = assignment.id).first().deadline
        date=str(deadline)
        day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
        all_deadline_days.append(day_name[day])
        all_deadline_dates.append(deadline.strftime("%I:%M %p"))

    #all the students displayed here
    if g.teacherLoggedIn:
        return render_template('display_classroom.html', classroom_id = int(classroom_id) ,all_deadline_days = all_deadline_days, all_deadline_dates = all_deadline_dates, available_assignments = available_assignments, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)

    else:
        #check if student is already on pending
        #yes so dont display the button instead so pending

        already_in_class = Students_in_Classroom.query.filter( and_(
            Students_in_Classroom.classroom_id.like(int(classroom_id)),
            Students_in_Classroom.student_id.like(current_user.id),
        )).first()

        form = StudentJoinClassroom()
        
        if already_in_class == None:
            if form.validate_on_submit():
                student = Students_in_Classroom(int(classroom_id), current_user.id)
                db.session.add(student)
                db.session.commit()

                return redirect(url_for('classrooms.display_classroom',classroom_id = int(classroom_id)))
        else:
            inClass = True
        
        return render_template('display_classroom.html', form = form, classroom_id = int(classroom_id), all_deadline_days = all_deadline_days, all_deadline_dates = all_deadline_dates, available_assignments = available_assignments, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn, inClass = inClass)


@classrooms_blueprint.route('/add_classroom',  methods=['GET', 'POST'])
def add_classroom():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = AddClassroom()
    if form.validate_on_submit():
        new_class = Classroom(form.class_name.data, form.class_section.data, g.whichTeacher.id)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('classrooms.teacher_class_list'))
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
    deadline = DateTimeLocalField("Deadline", [validators.Required()], format='%Y-%m-%dT%H:%M')
    setattr(AddClassroomAssignments, 'deadline', deadline)
    setattr(AddClassroomAssignments, 'submit', SubmitField('Add Assignment to classroom') )
    
    
    form = AddClassroomAssignments()

    if form.validate_on_submit():
        assignment_id = form.available_assignments.data
        deadline = form.deadline.data
        new_deadline = str(deadline)
        new_assignment_in_classroom = Assignments_in_Classroom(int(classroom_id), assignment_id, deadline)
        db.session.add(new_assignment_in_classroom)
        db.session.commit()
        return redirect(url_for('classrooms.display_classroom', classroom_id = int(classroom_id)))
    return render_template('add_classroom_assignment.html', form = form, classroom_id = classroom_id, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)


@classrooms_blueprint.route('/delete_classroom_assignments/<classroom_id>/<assignment_id>',  methods=['GET', 'POST'])
def delete_classroom_assignments(classroom_id,assignment_id):
    searchForm = Searching()
    if searchForm.searched.data != '' and searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    student_results = Solved_Classroom_Assignment.query.filter_by(classroom_id = int(classroom_id))

    assignment_data = Assignment_Data.query.filter_by(assignment_id = int(assignment_id)).all()
    no_of_question = 0
    for question in assignment_data:
        no_of_question +=1
    
    if assignment_data[0].assignment.difficulty == 'Expert':
        total_points = 5* (no_of_question)
        points = 5
    elif assignment_data[0].assignment.difficulty == 'Intermediate':
        total_points = 3* (no_of_question)
        points = 3
    else:
        total_points = 1* (no_of_question)
        points = 1

    form = DeleteClassroomAssignment()
    if form.validate_on_submit():
        assignment = Assignments_in_Classroom.query.filter(
        and_( 
            Assignments_in_Classroom.assignment_id.like(int(assignment_id)),
            Assignments_in_Classroom.classroom_id.like(int(classroom_id)),
        )).first()

        db.session.delete(assignment)
        db.session.commit()
        return redirect(url_for('classrooms.display_classroom', classroom_id = int(classroom_id)))
    
    return render_template('delete_assignment_classroom.html', form = form ,teacherLoggedIn = g.teacherLoggedIn, searchForm = searchForm, assignment_data = assignment_data, total_points = total_points, points = points, student_results = student_results)


@classrooms_blueprint.route('/solve_classroom_assignment/<classroom_id>/<assignment_id>',  methods=['GET', 'POST'])
def solve_classroom_assignment(assignment_id,classroom_id):
    done = False
    earned_points = None
    # ----------Searching Section------------
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    questions = Assignment_Data.query.filter_by(assignment_id = assignment_id)

    #-----------Making a form------------------
    no_of_question = 1
    field_list = []

    for record in questions:
        field = RadioField(choices=[('1' , record.choice1) , ('2' , record.choice2), ('3' , record.choice3), ('4' , record.choice4) ])
        setattr(SolveClassAssignment, 'radioField' + str(no_of_question), field) 
        # i.e: choice1 = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
        field_list.append('radioField'+str(no_of_question))
        no_of_question = no_of_question + 1

    setattr(SolveClassAssignment, 'submit', SubmitField("Submit"))


    #----- Checking Assignment Difficulty and Points ------------
    if questions[0].assignment.difficulty == 'Expert':
        total_points = 5* (no_of_question - 1)
        points = 5
    elif questions[0].assignment.difficulty == 'Intermediate':
        total_points = 3* (no_of_question - 1)
        points = 3
    else:
        total_points = 1* (no_of_question - 1)
        points = 1

    #checking if student has already solved this assignment or not.        
    assignment_already_solved = Solved_Classroom_Assignment.query.filter(
                                    and_(
                                            Solved_Classroom_Assignment.classroom_id.like(classroom_id),
                                            Solved_Classroom_Assignment.assignment_id.like(assignment_id),
                                            Solved_Classroom_Assignment.student_id.like(current_user.id),
                                    )
                                ).first()

    if assignment_already_solved != None:
        earned_points = assignment_already_solved.points
        done = True 
    #endif
    form = SolveClassAssignment()   
    
    # The Entire SOLVE ASSIGNMENT LOGIC with maintainence of Leaderboard starts from here...
    if form.validate_on_submit():
        earned_points = 0
        passed = False

        # Calculating student earned points for this assignment
        count = -1
        for record in questions:
            count = count + 1
            if getattr(form,field_list[count]).data == record.answer:
                getattr(form,field_list[count]).data = ''
                earned_points += points


    
        if assignment_already_solved == None: 
            # then check whether student has passed or failed 
            if  (questions[0].assignment.difficulty == 'Expert') and (earned_points >= (total_points*0.70) ):
                passed = True
            elif (questions[0].assignment.difficulty == 'Intermediate') and (earned_points >= (total_points*0.60) ):
                passed = True
            elif (questions[0].assignment.difficulty == 'Beginner') and (earned_points >= (total_points*0.50) ):
                passed = True
            else:
                passed = False
            #endif
            solved = Solved_Classroom_Assignment(int(classroom_id), int(assignment_id), current_user.id, earned_points)
            
            db.session.add(solved)
            db.session.commit()
        #endif
 
        return render_template('class_after_submit.html', passed = passed, searchForm = searchForm , earned_points = earned_points, total_points = total_points)

    #endif

    return render_template('solve_class_assignment.html',  form = form, questions = questions ,total_points = total_points, points = points, field_list = field_list,searchForm = searchForm , done = done, earned_points = earned_points)

@classrooms_blueprint.route('/display_class_students/<classroom_id>',  methods=['GET', 'POST'])
def display_class_students(classroom_id):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    students = Students_in_Classroom.query.filter_by(classroom_id = int(classroom_id))

    return render_template('display_class_students.html' , students = students , searchForm = searchForm , teacherLoggedIn = g.teacherLoggedIn)