from flask import Blueprint,render_template,redirect,url_for,flash,session
from flask_login import login_required,current_user
from myproject import db,g
from myproject.models import Student, Teacher, Assignments, Assignment_Data, Courses, Assignment_Review, Solved_Assignemnts, Assignments_in_Classroom, Solved_Classroom_Assignment
from myproject.assignments.forms import SolveAssignment, AddAssignment, DeleteAssignment, SubmitAssignment
from wtforms import RadioField,SubmitField, StringField,SelectField, Form, validators
from myproject.search.form import Searching
from sqlalchemy import func, and_ , inspect
import time

assignments_blueprint = Blueprint('assignments', __name__ , template_folder='templates/assignments')

@assignments_blueprint.route('/<category>',  methods=['GET', 'POST'])
def categories(category):
    courses = None
    if int(category) == 1:
        assignments = Assignments.query.filter_by(course_id = 1)
    elif int(category) == 2:
        assignments = Assignments.query.filter_by(course_id = 2)
    elif int(category) == 5:
        assignments = Assignments.query.filter_by(course_id = 5)
    elif int(category) == 6:
        assignments = Assignments.query.filter_by(course_id = 6)
    elif int(category) == 8:
        assignments = Assignments.query.filter_by(course_id = 8)
    elif int(category) == 9:
        assignments = Assignments.query.filter_by(course_id = 9)
    elif int(category) == 10:
        assignments = Assignments.query.filter_by(course_id = 10)
    elif int(category) == 11:
        assignments = Assignments.query.filter_by(course_id = 11)
    elif int(category) == 12:
        assignments = Assignments.query.filter_by(course_id = 12)
    elif int(category) == 13:
        assignments = Assignments.query.filter_by(course_id = 13)
    else:
        assignments = None
        courses = Courses.query.all()
    #endif

    if assignments == None:
        assignments = Assignments.query.filter_by(course_id = int(category))
    


    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('display_category.html', assignments = assignments, teacherLoggedIn = g.teacherLoggedIn, searchForm = searchForm, courses=courses )


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
    for x in range (1): #for no of questions
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
            new_assignment = Assignments(assignment_name, course_id, difficulty, 0, 0, 0, 1, g.whichTeacher.id)
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





@assignments_blueprint.route('/delete_assignment/<aid>',  methods=['GET', 'POST'])
def delete_assignment(aid):
    searchForm = Searching()
    if searchForm.searched.data != '' and searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    assignment_data = Assignment_Data.query.filter_by(assignment_id = aid).all()
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

    form = DeleteAssignment()
    #try with multiple questions
    if form.validate_on_submit():
      

        assignment = Assignments.query.filter_by(id = aid).first()
        updated_course = Courses.query.filter_by(id = assignment.course_id).first()
        if updated_course.no_of_assignments == 0:
            updated_course.no_of_assignments = 0
        else:
            updated_course.no_of_assignments -= 1  #incrementing the number of assignments for a course
        db.session.add(updated_course)
        db.session.commit()
      
        assignment = Assignments.query.filter_by(id = aid).first()
        db.session.delete(assignment)
        db.session.commit()

        # Now updating Teacher teacher_rating and teacher_no_Of_reviews.
        teacher = Teacher.query.filter_by(id = g.whichTeacher.id).first()
        teacher_assignments = Assignments.query.filter_by(teacher_id = teacher.id).all()

        count = 0
        avg_teacher_rating = 0
        for assignment in teacher_assignments:
            if assignment.assignment_rating > 0:
                count += 1
                avg_teacher_rating += assignment.assignment_rating
            #endif
        #endfor

        if count == 0:
            teacher.teacher_rating = 0
            teacher.teacher_no_Of_reviews = 0
        else:    
            teacher.teacher_rating = avg_teacher_rating/count
            teacher.teacher_no_Of_reviews -= assignment.assignment_no_of_reviews
        #endif
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('assignments.list_assignment'))

    return render_template('delete_assignment.html', form = form, teacherLoggedIn = g.teacherLoggedIn, assignment_data = assignment_data, searchForm = searchForm, total_points = total_points , points =points )


@assignments_blueprint.route('/list_assignment', methods=['GET', 'POST'])
def list_assignment():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    all_assignments = Assignments.query.filter_by(teacher_id = g.whichTeacher.id)
    teacher = Teacher.query.filter_by(id = g.whichTeacher.id).first()
    
    total_assignments = 0
    for assignment in all_assignments:
        total_assignments += 1
    
    return render_template('list_assignment.html',teacher = teacher, all_assignments=all_assignments, teacherLoggedIn = g.teacherLoggedIn, searchForm = searchForm, total_assignments=total_assignments)

@assignments_blueprint.route('/solve_assignment/<aid>',  methods=['GET', 'POST'])
@login_required
def solve_assignment(aid):

    # ----------Searching Section------------
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


    form = SolveAssignment()   
    print(getattr(form,field_list[0]).data)
    # The Entire SOLVE ASSIGNMENT LOGIC with maintainence of Leaderboard starts from here...
    if form.validate_on_submit():
        earned_points = 0
        passed = False
        student = None

        # When student press submit: student_attempted =  student_attempted + 1 ;
        student = Student.query.filter_by(id = current_user.id).first()
        if student.student_attempted == 0:
            old_rank_points = 0   
        else:
            old_rank_points = (student.student_score * student.student_solved) /student.student_attempted
        
        student.student_attempted += 1
        

        # Calculating student earned points for this assignment
        count = -1
        for record in questions:
            count = count + 1
            if getattr(form,field_list[count]).data == record.answer:
                getattr(form,field_list[count]).data = ''
                earned_points += points


        #checking if student has already solved this assignment or not.        
        assignment_already_solved = Solved_Assignemnts.query.filter(
                                        and_(
                                                Solved_Assignemnts.assignment_id.like(aid),
                                                Solved_Assignemnts.student_id.like(current_user.id),
                                        )
                                    ).first()


        # if student has already solved this assignment before
        if assignment_already_solved != None:
            passed = True
            # then Check if student newScore is greated than his previousScore in this assignment; else score unchanged.
            if earned_points > assignment_already_solved.points:
                #if it is greater then : remove his previoseScore from his total score..
                student.student_score = student.student_score - assignment_already_solved.points
                # and add this new score to his total score
                student.student_score = student.student_score + earned_points
                assignment_already_solved.points = earned_points
                db.session.add(assignment_already_solved)
            elif assignment_already_solved.points == total_points:
                student.student_attempted -= 1
            #endif


        # if this is student first attempt..
        else: 
            
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

            # if passed
            if passed == True:
                #then student_solved ++ and student_score = student_score + earned_points
                student.student_solved += 1
                student.student_score += earned_points
            #endif
            solved = Solved_Assignemnts(student.id , int(aid), earned_points)
            db.session.add(solved)
        #endif
        
        # student record is updated
        db.session.add(student)
        db.session.commit()

        #Updating the Leaderboard
        #========================
        student = Student.query.filter_by(id = current_user.id).first()

        #student_new_position
        new_rank_points = (student.student_score * student.student_solved) /student.student_attempted 
        #finding all the students who have attempted atleast one assignment, sorted by thier rank in asc order.
        all_students = Student.query.order_by(Student.student_rank.asc()).filter(Student.student_attempted > 0)
        
        # counting no of students in all_students
        no_of_students = 0
        for studs in all_students:
            no_of_students += 1
       
       # check if there is only one student and his rank is 0 and he has passed the assignment.
        rank_increased = False
        rank_decreased = False
        temp = 1
        if no_of_students == 1:        
            for stud in all_students:
                stud.student_rank = 1
                db.session.add(stud)
            #endfor    
        # if more than one student (here there will always  be one student with rank = 1st)
        elif no_of_students > 1: 
            for stud in all_students:
                print(f"stud.id: {stud.id}")
                if stud.id == student.id:
                    if stud.student_rank == 0:
                        student.student_rank = no_of_students

                    if old_rank_points > new_rank_points:
                        print("continue")
                        continue

                    break
                #endif

                position  = (stud.student_score * stud.student_solved) /stud.student_attempted
                if new_rank_points > position and old_rank_points <= new_rank_points:
                    print("in first if")
                    temp = student.student_rank
                    new_rank = int(stud.student_rank)
                    rank_increased = True
                    break

                elif old_rank_points > new_rank_points and position > new_rank_points:
                    print("in second if")
                    new_rank = stud.student_rank
                    temp = student.student_rank
                    rank_decreased = True
                #endif    
            #endfor
        #endif

        if rank_increased == True:
            for stud in all_students:
                if stud.student_rank == temp:
                    break
                #endif
                if stud.student_rank >= new_rank:
                    stud.student_rank +=  1
                    db.session.add(stud)
                #endif
            #endfor 
            student.student_rank = new_rank
            db.session.add(student)
            
        elif rank_decreased == True:
            for stud in all_students:
                if stud.student_rank == new_rank + 1:
                    break
                #endif
                if stud.student_rank > student.student_rank:
                    stud.student_rank -= 1
                    db.session.add(stud)
                #endif
            #endfor 
            student.student_rank = new_rank
            db.session.add(student)
        #endif   
        
        db.session.commit()
        return redirect(url_for('assignments.after_submit',passed = passed, aid = aid, temp = temp))
    #endif

    return render_template('solve_assignment.html',  form = form, questions = questions ,total_points = total_points, points = points, field_list = field_list,searchForm = searchForm)

    
        
@assignments_blueprint.route('/after_submit/<passed>/<aid>/<temp>',  methods=['GET', 'POST'])
@login_required
def after_submit(passed, aid, temp):
    
    rank_changed = False
    points_earned = 0
    old_rank = int(temp)
    # assignment = Assignments.query.filter_by()
    # checking how much points earned by student in this assignment
    solve = Solved_Assignemnts.query.filter( and_(
                                            Solved_Assignemnts.assignment_id.like(int(aid)),
                                            Solved_Assignemnts.student_id.like(current_user.id),
                                        )).first()
    points_earned = solve.points

    # --- Searching ----
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))


    
    form = SubmitAssignment()

    # Check if student has already given his assignment review or not.
    aid = int(aid)
    review_already_given = Assignment_Review.query.filter(
        and_(
            Assignment_Review.assignment_id.like(aid),
            Assignment_Review.student_id.like(current_user.id),
        )
    ).first()
    
    
    # the Entire "Giving Assignment, Teacher rating and reviews" coding.
    if form.validate_on_submit(): 

        #if this happens, then this is the first time, student is rating and giving review AND student must have given both rating and review to the solved assignment(because validator required at both fields).

        # get all reviews of assignment whose assignment_id = aid.
        last_review = Assignment_Review.query.filter_by(assignment_id = aid).all()

        if last_review != []: # if not empty
            print("here")
            review_no = last_review[-1].review_id + 1 # add 1 to last review_id
        else:  
            review_no = 1
        #endif


        # Done with Assignment_Review Table
        assignment_review = Assignment_Review(review_no, aid, current_user.id, form.rating.data, form.review.data)
        db.session.add(assignment_review)
        

        # Now updating Assignment assignment_rating,assignment_no_of_reviews and assignment_no_of_ratings.
        assignment = Assignments.query.filter_by(id = aid).first()
        assignment.assignment_no_of_reviews += 1
        if assignment.assignment_no_of_ratings == 0:
            assignment.assignment_rating = form.rating.data
        else:
            assignment.assignment_rating = ( (assignment.assignment_rating * assignment.assignment_no_of_ratings) + float(form.rating.data)) / (assignment.assignment_no_of_ratings + 1)
        #endif

        assignment.assignment_no_of_ratings += 1
        db.session.add(assignment)
        db.session.commit()

        # Now updating Teacher teacher_rating and teacher_no_Of_reviews.
        teacher = Teacher.query.filter_by(id = assignment.teacher_id).first()
        teacher_assignments = Assignments.query.filter_by(teacher_id = teacher.id)

        count = 0
        avg_teacher_rating = 0
        for assignment in teacher_assignments:
            if assignment.assignment_rating > 0:
                count += 1
                avg_teacher_rating += assignment.assignment_rating
        #endfor

        teacher.teacher_rating = avg_teacher_rating/count
        teacher.teacher_no_Of_reviews += 1

        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('index'))
    #endif
    
    return render_template('after_submit.html', form = form, searchForm = searchForm, passed = passed, rank_changed = rank_changed, old_rank = old_rank, points_earned =points_earned, review_already_given = review_already_given)  
    


