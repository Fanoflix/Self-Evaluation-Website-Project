from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher, Assignments, Assignment_Data, Courses
from myproject.assignments.forms import SolveAssignment, AddAssignment, DeleteAssignment
from wtforms import RadioField,SubmitField, StringField,SelectField, Form, validators
from myproject.search.form import Searching
from sqlalchemy import func

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
            new_assignment = Assignments(assignment_name, course_id, difficulty, 0, 1, g.whichTeacher.id)
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

                new_question = Assignment_Data(question[0],question[1],question[2] ,question[3],question[4] ,question[5],question[6] ,question[7] )
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

    return render_template('delete_assignment.html', form = form, teacherLoggedIn = g.teacherLoggedIn, assignment_data = assignment_data, searchForm = searchForm)


@assignments_blueprint.route('/list_assignment', methods=['GET', 'POST'])
def list_assignment():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    all_assignments = Assignments.query.filter_by(teacher_id = g.whichTeacher.id)
    return render_template('list_assignment.html', all_assignments = all_assignments, teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm)

@assignments_blueprint.route('/solve_assignment/<aid>',  methods=['GET', 'POST'])
def solve_assignment(aid):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    #---------------------------Displaying from DB---------------------------
    # records = []
    # questions = []

    # for q in Assignment_Data.query.filter_by(assignment_id = aid).all():
    #     questions.append(aid)
    #     questions.append(q.question_id)
    #     questions.append(q.question_text)
    #     questions.append(q.choice1)
    #     questions.append(q.choice2)
    #     questions.append(q.choice3)
    #     questions.append(q.choice4)
    #     questions.append(q.answer)
    #     records.append(questions)
    #     questions = []


    # count = 1
    # field_list = []

    # for record in records:
    #     field = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
    #     setattr(DeleteAssignment, 'choice' + str(count), field) 
    #     field_list.append('choice' + str(count))
    #     count = count + 1

    # setattr(DeleteAssignment, 'submit', SubmitField("Delete"))
    
    # questions = []
    # for record in records:  
    #     questions.append(record[2])

    #---------------------------Displaying from DB---------------------------
    
    # assignment = TableName1.query.filter_by(assignment_name = 'some name').first():
    # id = assignment.TableName.assignment_id
    # a sample 

    records = [ 
                ['1','1','How do you do when you cant do?','you do', 'you dont' ,'you cant' , 'you suck' ,'2'] ,
                ['1','2','What is your name?','I', 'you' ,'no' , 'yes' ,'4'] ,
                ['1','3','Is Abdullah a bot? Wrong answers only','yes', 'yes' ,'yes' , 'yes' ,'1'] ,
                ['1','4','You done fucked up','yes', 'no' ,'I am' , 'hahaha' ,'3'] ,
                ['1','5','How is testing going?','perfect', 'good' ,'not bad' , 'fucked' ,'4'] 
                ]
        


    questions = []
    # for record in TableName.query.filter_by(assignment_id = id).all():
    for record in records:  
            questions.append(record[2])
  

    #-----------Making a form------------------
    count = 1
    field_list = []

    # for record in TableName.query.filter_by(assignment_id = id).all():
    for record in records:
        field = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
        setattr(SolveAssignment, 'choice' + str(count), field) 
        # i.e: choice1 = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
        field_list.append('choice'+str(count))
        count = count + 1

    setattr(SolveAssignment, 'submit', SubmitField("Submit"))
    #----------------------------------------------
    form = SolveAssignment()   

    if form.validate_on_submit():
        count = -1
        for record in records:
            count = count + 1
            if getattr(form,field_list[count]).data == record[7]:
                # points++
                print(getattr(form,field_list[count]).data)
            
            getattr(form,field_list[count]).data = ''
        
        return redirect(url_for('assignments.after_submit'))

    return render_template('solve_assignment.html' , form = form, teacherLoggedIn = g.teacherLoggedIn, questions = questions , field_list = field_list,searchForm = searchForm)

    
        
@assignments_blueprint.route('/after_submit',  methods=['GET', 'POST'])
def after_submit():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    return render_template('after_submit.html' , teacherLoggedIn = g.teacherLoggedIn,searchForm = searchForm)  
    


