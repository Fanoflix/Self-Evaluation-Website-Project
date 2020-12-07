from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student
from myproject.students.forms import SignUp,LogIn

students_blueprint = Blueprint('students', __name__ , template_folder='templates/students')

@students_blueprint.route('/signup',  methods=['GET', 'POST'])
def signup():
    form = SignUp()

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 != '' and password1 == password2:
            new_student = Student(fname,lname,email,password1,0,0,0)
            db.session.add(new_student)
            db.session.commit()

            return redirect(url_for('index'))
    
    return render_template('signup.html',form=form )


@students_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():
    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        checkEmail = bool(Student.query.filter_by(student_email = email).first())

        if checkEmail:
            CheckStudent = Student.query.filter_by(student_email = email).first()

            if CheckStudent.student_email == email and CheckStudent.student_password == password:
                g.studentLoggedIn = True
                g.whichStudent = email
                return redirect( url_for('index') )
            else:
                return render_template('login.html' , form=form , loginFailed = True)

        else:
            return render_template('login.html' , form=form , loginFailed = True)

    return render_template('login.html', form=form, loginFailed = False)
            
@students_blueprint.route('/' )
def signout():
    g.studentLoggedIn = False
    return redirect( url_for('index') )

@students_blueprint.route('/profile' )
def profile():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()

    return render_template('profile.html' , studentLoggedIn = studentLoggedIn , fname = user.student_fname, lname = user.student_lname)   











@students_blueprint.route('/photo' )
def photo():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()
    return render_template('photo.html' , studentLoggedIn = studentLoggedIn , username = user.student_name) 

@students_blueprint.route('/account' )
def account():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()
    return render_template('account.html' , studentLoggedIn = studentLoggedIn , username = user.student_name)  

@students_blueprint.route('/payment_method' )
def payment_method():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()
    return render_template('payment_method.html' , studentLoggedIn = studentLoggedIn , username = user.student_name) 

@students_blueprint.route('/privacy' )
def privacy():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()
    return render_template('privacy.html' , studentLoggedIn = studentLoggedIn , username = user.student_name)   

@students_blueprint.route('/deactivate_account' )
def deactivate_account():
    studentLoggedIn = g.studentLoggedIn
    user = Student.query.filter_by(student_email = g.whichStudent).first()
    return render_template('deactivate_account.html' , studentLoggedIn = studentLoggedIn , username = user.student_name)     
