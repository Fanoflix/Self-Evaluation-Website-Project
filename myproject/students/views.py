from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Student, Teacher
from myproject.students.forms import SignUp,LogIn,ProfileTab,AccountTab,PrivacyTab,DeactivateTab

students_blueprint = Blueprint('students', __name__ , template_folder='templates/students')

@students_blueprint.route('/signup',  methods=['GET', 'POST'])
def signup():
    form = SignUp()
    signupFailed = False

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data
        checkTeacherEmail = bool(Teacher.query.filter_by(teacher_email = email).first())
        checkStudentEmail = bool(Student.query.filter_by(student_email=email).first())

        # Check if Email is already registered
        if checkTeacherEmail or checkStudentEmail:
            return render_template('signup.html',form=form, signupFailed = True)

        if password1 != '' and password1 == password2:
                new_student = Student(fname, lname, email, password1,0,0,0)
                db.session.add(new_student)
                db.session.commit()
                return redirect(url_for('students.login'))
    
    return render_template('signup.html',form=form )


@students_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():
    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        CheckStudent = Student.query.filter_by(student_email = email).first()

        if CheckStudent != None and CheckStudent.student_email == email and CheckStudent.check_password(password):
            g.studentLoggedIn = True
            g.whichStudent = CheckStudent
            return redirect( url_for('index') )
        else:
            return render_template('login.html' , form=form , loginFailed = True)

    return render_template('login.html', form=form, loginFailed = False)
            
@students_blueprint.route('/' )
def signout():
    g.studentLoggedIn = False
    g.whichStudent = False 
    return redirect( url_for('index') )

@students_blueprint.route('/profile',  methods =['GET' , 'POST'])
def profile():
    form = ProfileTab()

    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = g.whichStudent.student_email).first()
        # if form.uname.data != "":
        #     user.student_uname = form.uname.data
        if form.fname.data != "":
            user.student_fname = form.fname.data
        if form.lname.data != "":
            user.student_lname = form.lname.data
        # if form.bio.data != "":
        #     user.student_bio = form.bio.data    
        db.session.add(user)
        db.session.commit()
        g.whichStudent = user
        form.fname.data = ""
        form.lname.data = ""
        form.bio.data = ""

    return render_template('profile.html', form = form, studentLoggedIn = g.studentLoggedIn , fname = g.whichStudent.student_fname, lname =g.whichStudent.student_lname )   


@students_blueprint.route('/photo' )
def photo():

    return render_template('photo.html' , studentLoggedIn = g.studentLoggedIn , fname = g.whichStudent.student_fname, lname = g.whichStudent.student_lname) 

@students_blueprint.route('/account',  methods =['GET' , 'POST'] )
def account():
    form = AccountTab()
    passwordChangeFailed = False 
    passwordMatchFailed = False 

    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = g.whichStudent.student_email).first()
        if not user.check_password(form.password1.data):
            passwordChangeFailed = True
            return render_template('account.html', form = form, studentLoggedIn = g.studentLoggedIn, fname = g.whichStudent.student_fname,
            lname = g.whichStudent.student_lname, passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichStudent.student_email ) 
            
        if form.password2.data == form.password3.data:
            user.hash_password(form.password2.data)
            db.session.add(user)
            db.session.commit()
            g.whichStudent = user
        else:
            passwordMatchFailed = True

    return render_template('account.html', form = form, studentLoggedIn = g.studentLoggedIn, fname = g.whichStudent.student_fname,
        lname = g.whichStudent.student_lname,passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichStudent.student_email ) 

@students_blueprint.route('/payment_method' )
def payment_method():

    return render_template('payment_method.html' , studentLoggedIn = g.studentLoggedIn , fname = g.whichStudent.student_fname, lname = g.whichStudent.student_lname) 

@students_blueprint.route('/privacy',  methods =['GET' , 'POST']  )
def privacy():
    form = PrivacyTab()
    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = g.whichStudent.student_email).first()
        if form.validate_on_submit():
            print(form.displayRank.data)
            print(form.displayStats.data)

            # additional code here
           
    return render_template('privacy.html', form = form, studentLoggedIn = g.studentLoggedIn ,  fname = g.whichStudent.student_fname, lname = g.whichStudent.student_lname)  

@students_blueprint.route('/deactivate_account' ,  methods =['GET' , 'POST'] )
def deactivate_account():
    form = DeactivateTab()
    passwordMatchFailed = False 
    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = g.whichStudent.student_email).first()
       
        if user.check_password(form.password.data):
            db.session.delete(user)
            db.session.commit()
            whichStudent = False
            g.studentLoggedIn = False
            return redirect( url_for('students.signout') )
        else:
            passwordMatchFailed = True 

    return render_template('deactivate_account.html' , form = form, studentLoggedIn = g.studentLoggedIn , fname = g.whichStudent.student_fname, lname = g.whichStudent.student_lname, passwordMatchFailed = passwordMatchFailed)    
