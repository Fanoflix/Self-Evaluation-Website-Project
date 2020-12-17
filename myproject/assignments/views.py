from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher, Assignments, Assignment_Data, Courses, Assignment_Review, Saved_Assignemnts
from myproject.assignments.forms import SolveAssignment, AddAssignment, DeleteAssignment, SubmitAssignment
from wtforms import RadioField,SubmitField, StringField,SelectField, Form, validators
from myproject.search.form import Searching
from sqlalchemy import func
import time

assignments_blueprint = Blueprint('assignments', __name__ , template_folder='templates/assignments')


@assignments_blueprint.route('/description',  methods=['GET', 'POST'])
def description():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('description.html' , teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm)

@assignments_blueprint.route('/add_assignment',  methods=['GET', 'POST'])
def add_assignment():
    searchForm = Searching()
    if searchForm.searched.data != '' and searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    course = SelectField("Courses",[validators.Required()], choices = [(course.id, course.course_name) for course in Courses.query.all()])
    setattr(AddAssignment, 'course', course)
 

    all_questions = [] 
    questions = []
    index = []
    assignment_questions = 1
    for x in range (3): #for no of questions
        field = StringField([ validators.Required() ])
        setattr(AddAssignment, 'Question' + str(assignment_questions), field)
        questions.append('Question' + str(assignment_questions))
        choice = 1
        for y in range (4):
            setattr(AddAssignment, 'Choice' + str(assignment_questions) + str(choice), field)
            questions.append('Choice' + str(assignment_questions) + str(choice))
            choice += 1
        setattr(AddAssignment, 'Answer' + str(assignment_questions), field)
        questions.append('Answer' + str(assignment_questions))
        index.append(str(assignment_questions))
        assignment_questions += 1
        all_questions.append(questions)
        questions = []
    setattr(AddAssignment, 'submit', SubmitField('Add Assignment') )


    form = AddAssignment()

    if form.validate_on_submit():
        assignment_name = form.assignment_name.data
        difficulty = form.difficulty.data
        course_id = form.course.data

        updated_course = Courses.query.filter_by(id = course_id).first()
        updated_course.no_of_assignments += 1  #incrementing the number of assignments for a course
        db.session.add(updated_course)
        db.session.commit()
        
        CheckAssignment = bool(Assignments.query.filter(func.lower(Assignments.assignment_name) == func.lower(assignment_name)).first())

        if not CheckAssignment:
            new_assignment = Assignments(assignment_name, course_id, difficulty, 0, 0, 1, g.whichTeacher.id)
            db.session.add(new_assignment)
            db.session.commit()

            question = []
            for x in range(1,assignment_questions): 
                question.append(new_assignment.id)
                question.append(x)
                question.append( getattr( form , 'Question' + str(x) ).data )
                for y in range(1,5):
                    question.append( getattr(form,'Choice' + str(x) + str(y)).data )

                question.append (getattr(form, 'Answer' + str(x)).data )

                new_question = Assignment_Data(question[0], question[1], question[2], question[3], question[4], question[5], question[6], question[7])
                db.session.add(new_question)
                db.session.commit()
                question = []
        else:
            pass
        
        return redirect(url_for('assignments.list_assignment'))

    return render_template('add_assignment.html', all_questions = all_questions, index = index, form = form, teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm)





@assignments_blueprint.route('/<aid>',  methods=['GET', 'POST'])
def delete_assignment(aid):
    searchForm = Searching()
    if searchForm.searched.data != '' and searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    assignment_data = Assignment_Data.query.filter_by(assignment_id = aid).all()
    no_of_question = 0
    for question in assignment_data:
        no_of_question +=1
    
    if assignment_data[0].assignment.difficulty == 'expert':
        total_points = 5* (no_of_question)
        points = 5
    elif assignment_data[0].assignment.difficulty == 'intermediate':
        total_points = 3* (no_of_question)
        points = 3
    else:
        total_points = 1* (no_of_question)
        points = 1

    form = DeleteAssignment()
    #try with multiple questions
    if form.validate_on_submit():
        for q in Assignment_Data.query.filter_by(assignment_id = aid).all():
            db.session.delete(q)
            db.session.commit()

        assignment = Assignments.query.filter_by(id = aid).first()
        updated_course = Courses.query.filter_by(id = assignment.course_id).first()
        updated_course.no_of_assignments -= 1  #incrementing the number of assignments for a course
        db.session.add(updated_course)
        db.session.commit()
        db.session.delete(assignment)
        db.session.commit()

        return redirect(url_for('assignments.list_assignment'))

    return render_template('delete_assignment.html', form = form, teacherLoggedIn = g.teacherLoggedIn, assignment_data = assignment_data, searchForm = searchForm, total_points = total_points , points =points )


@assignments_blueprint.route('/list_assignment', methods=['GET', 'POST'])
def list_assignment():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    total_assignments = 0
    total_reviews = 0
    total_assignment_rating = 0
    all_assignments = Assignments.query.filter_by(teacher_id = g.whichTeacher.id)

    for assignment in all_assignments:
        for review in Assignment_Review.query.filter_by(assignment_id = assignment.id):
            total_reviews += 1

        total_assignments += 1
        # total_reviews += assignment.assignment_review
        total_assignment_rating += assignment.assignment_rating
    
    average_rating = total_assignment_rating/total_assignments
    return render_template('list_assignment.html',average_rating=average_rating, total_reviews=total_reviews, all_assignments=all_assignments, teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm, total_assignments=total_assignments)

@assignments_blueprint.route('/solve_assignment/<aid>',  methods=['GET', 'POST'])
def solve_assignment(aid):
    earned_points = 0
    passed = False
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    questions = Assignment_Data.query.filter_by(assignment_id = aid)

    #-----------Making a form------------------
    no_of_question = 1
    field_list = []

    for record in questions:
        field = RadioField(choices=[('1' , record.choice1) , ('2' , record.choice2), ('3' , record.choice3), ('4' , record.choice4) ])
        setattr(SolveAssignment, 'radioField' + str(no_of_question), field) 
        # i.e: choice1 = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
        field_list.append('radioField'+str(no_of_question))
        no_of_question = no_of_question + 1

    setattr(SolveAssignment, 'submit', SubmitField("Submit"))
    #----------------------------------------------

    if questions[0].assignment.difficulty == 'expert':
        total_points = 5* (no_of_question - 1)
        points = 5
    elif questions[0].assignment.difficulty == 'intermediate':
        total_points = 3* (no_of_question - 1)
        points = 3
    else:
        total_points = 1* (no_of_question - 1)
        points = 1


    form = SolveAssignment()   
    
    if form.validate_on_submit():
        student = Student.query.filter_by(id = g.whichStudent.id).first()
        student.student_attempted += 1
        db.session.add(student)
        db.session.commit()

        count = -1
        for record in questions:
            count = count + 1
            if getattr(form,field_list[count]).data == record.answer:
                getattr(form,field_list[count]).data = ''
                earned_points += points 
                
        print(earned_points)
        if  (questions[0].assignment.difficulty == 'expert') and (earned_points >= (total_points*0.70) ):
            student.student_solved += 1
            student.student_score += earned_points
            passed = True
        elif (questions[0].assignment.difficulty == 'intermediate') and (earned_points >= (total_points*0.60) ):
            student.student_solved += 1
            student.student_score += earned_points
            passed = True
        elif (questions[0].assignment.difficulty == 'beginner') and (earned_points >= (total_points*0.50) ):
            student.student_solved += 1
            student.student_score += earned_points
            passed = True
        else:
            passed = False
        
        db.session.add(student)
        db.session.commit()

        this_position = (student.student_score * student.student_solved) /student.student_attempted
        student.student_rank = 1
        all_students = Student.query.order_by(Student.student_rank.asc()).filter(Student.student_attempted > 0)
        
        # counting no of students
        no_of_students = 0
        for studs in all_students:
            no_of_students += 1
       
        print(no_of_students)
       # checking if there is only for one student with condition Student.student_attempted > 0
        if no_of_students == 1 and passed == True and all_students[0].student_rank == 0:         
            all_students[0].student_rank += 1
            db.session.add(all_students[0])
        else:
            for stud in all_students:
                if stud.id != student.id:
                        position  = (stud.student_score * stud.student_solved) /stud.student_attempted
                        if this_position > position:
                            student.student_rank = stud.student_rank
                            stud.student_rank += 1
                            db.session.add(stud)
                            break
                        elif student.student_rank > stud.student_rank:
                            stud.student_rank -= 1
                            student.student_rank += 1
                            db.session.add(stud)
                            break
                        else:
                            student.student_rank += 1
                            db.session.add(stud)

        db.session.add(student)
        db.session.commit()
        return redirect(url_for('assignments.after_submit',passed = passed, aid = int(aid)))

    #Too View the answers..................Delete this when done
    temp_assignment_data = Assignment_Data.query.filter_by(assignment_id = aid)
    return render_template('solve_assignment.html', temp_assignment_data = temp_assignment_data, form = form, teacherLoggedIn = g.teacherLoggedIn, studentLoggedIn = g.studentLoggedIn ,questions = questions ,total_points = total_points, points = points, field_list = field_list,searchForm = searchForm)

    
        
@assignments_blueprint.route('/after_submit/<passed>/<aid>',  methods=['GET', 'POST'])
def after_submit(passed, aid):
    rank_change = False
    rank_changed_by = 0
    points_earned = 0
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    student = Student.query.filter_by(id = g.whichStudent.id).first()

    if student.student_rank != g.whichStudent.student_rank:
        rank_changed_by = g.whichStudent.student_rank - student.student_rank
        rank_change = True

    if student.student_score != g.whichStudent.student_score:
        points_earned = student.student_score - g.whichStudent.student_score
    
    g.whichStudent = False 
    g.whichStudent = student

    form = SubmitAssignment()
    if form.validate_on_submit():
        total_avg_rating = 0
        aid = int(aid)
        review_text = form.review.data
        rating = float(form.rating.data)
        assignment = Assignments.query.filter_by(id = aid).first()
        assignment.assignment_no_of_reviews += 1
        assignment.teacher.teacher_no_Of_reviews += 1
        #Taking the average of rating
        # assignment.assignment_rating += rating #Adding new rating to the old rating
        # assignment.assignment_rating /= 2 #Averaging (this is not the correct way. The correct way would be to add all individual ratings all over again)
        for assignment_review in Assignment_Review.query.filter_by(assignment_id = int(aid)).all():
            total_avg_rating += assignment_review.individual_rating

        total_avg_rating += rating
        total_avg_rating /= assignment.assignment_no_of_reviews
        assignment.assignment_rating = total_avg_rating

        g.total_reviews += 1
        # THIS RATING IS NULL FOR SOME REASON IDK its beyond science
        assignment_review = Assignment_Review(g.total_reviews, int(aid), float(rating), review_text)
        save_assignment = Saved_Assignemnts(g.whichStudent.id, int(aid))
        db.session.add(save_assignment)
        db.session.add(assignment)
        db.session.add(assignment_review)
        db.session.commit()

        total_avg_rating = 0
        assignment_teacher = Assignments.query.filter_by(id = aid).first()
        for assignment in Assignments.query.filter_by(teacher_id = assignment_teacher.teacher.id):
            total_avg_rating += assignment.assignment_rating

        total_avg_rating /= assignment_teacher.teacher.teacher_no_Of_reviews
        assignment_teacher.teacher.teacher_rating = total_avg_rating
        db.session.add(assignment_teacher)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('after_submit.html' , form = form, teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm , passed = passed,rank_change = rank_change ,rank_changed_by = rank_changed_by , points_earned =points_earned , student = student , studentLoggedIn = g.studentLoggedIn)  
    


