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

  
    questions = [ 'How do you do when you cant do?' ,
                'What is your name?' , 
                'Is Abdullah a bot? Wrong answers only' , 
                'You done fucked up',
                'How is testing going?']

    count = 1
    field_list = []
    for x in range(5):
        field = RadioField(choices=[('a1' , 'a1') , ('a2' , 'a2'), ('a3' , 'a3'), ('a4' , 'a4')])
        setattr(SolveAssignment, 'choice' + str(count), field) 
        field_list.append('choice'+str(count))
        count = count + 1

    submit = SubmitField("Submit")
    setattr(SolveAssignment, 'submit', submit)

    form = SolveAssignment()   

    if form.validate_on_submit():
        print(form.choice1.data)
        print(form.choice2.data)
        print(form.choice3.data)
        print(form.choice4.data)
        print(form.choice5.data)
        #redirect to some other page

    return render_template('solve_assignment.html' , form = form, teacherLoggedIn = g.teacherLoggedIn, questions = questions , field_list = field_list)

    
        
    
    


