from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher
from myproject.assignments.forms import SolveAssignment
from wtforms import RadioField,SubmitField

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


    # a sample 
    records = [ 
                ['1','1','How do you do when you cant do???????????????????????????????????????????????????????????????????????????????????????????????????????????????????','you do', 'you dont' ,'you cant' , 'you suck' ,'2'] ,
                ['1','2','What is your name?','I', 'you' ,'no' , 'yes' ,'4'] ,
                ['1','3','Is Abdullah a bot? Wrong answers only','yes', 'yes' ,'yes' , 'yes' ,'1'] ,
                ['1','4','You done fucked up','yes', 'no' ,'I am' , 'hahaha' ,'3'] ,
                ['1','5','How is testing going?','perfect', 'good' ,'not bad' , 'fucked' ,'4'] 
                ]
        


    questions = []
    # for record in TableName.query.filter_by(assignment_id = 'some number').all():
    for record in records:  
            questions.append(record[2])
  

    #-----------Making a form------------------
    count = 1
    field_list = []

    # for record in TableName.query.filter_by(assignment_id = 'some number').all():
    for record in records:
        field = RadioField(choices=[('1' , record[3]) , ('2' , record[4]), ('3' , record[5]), ('4' , record[6]) ])
        setattr(SolveAssignment, 'choice' + str(count), field) 
        field_list.append('choice'+str(count))
        count = count + 1

    submit = SubmitField("Submit")
    setattr(SolveAssignment, 'submit', submit)
    #----------------------------------------------
    form = SolveAssignment()   

    if form.validate_on_submit():
        print(form.choice1.data)
        print(form.choice2.data)
        print(form.choice3.data)
        print(form.choice4.data)
        print(form.choice5.data)
        #redirect to some other page

    return render_template('solve_assignment.html' , form = form, teacherLoggedIn = g.teacherLoggedIn, questions = questions , field_list = field_list)

    
        
    
    


