from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Teacher,Student
from myproject.teachers.forms import SignUp,LogIn, ProfileTab,AccountTab, PrivacyTab, DeactivateTab

teachers_blueprint = Blueprint('teachers', __name__ , template_folder='templates/teachers')

@teachers_blueprint.route('/signup',  methods=['GET', 'POST'])
def signup():
    form = SignUp()

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
            return render_template('tsignup.html',form=form, signupFailed = True)

        if password1 != '' and password1 == password2:
            new_teacher = Teacher(fname,lname,email,password1,0,0)
            db.session.add(new_teacher)
            db.session.commit()
            return redirect(url_for('teachers.login'))
    
    return render_template('tsignup.html',form=form )


@teachers_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():
    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        
        CheckTeacher = Teacher.query.filter_by(teacher_email = email).first()

        if CheckTeacher != None and CheckTeacher.teacher_email == email and CheckTeacher.check_password(password):
            g.teacherLoggedIn = True
            g.whichTeacher = CheckTeacher
            return redirect( url_for('index') )
        else:
            return render_template('tlogin.html' , form=form , loginFailed = True)

        
    return render_template('tlogin.html' , form=form , loginFailed = False)
            
@teachers_blueprint.route('/')
def signout():
    g.teacherLoggedIn = False
    g.whichTeacher = False 
    return redirect( url_for('index') )


    
@teachers_blueprint.route('/profile', methods =['GET' , 'POST'])
def profile():
    form = ProfileTab()
    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        # if form.uname.data != "":
            # updated_teacher.teacher_uname = form.uname.data
        if form.fname.data != "":
            updated_teacher.teacher_fname = form.fname.data
        if form.lname.data != "":
            updated_teacher.teacher_lname = form.lname.data
        # if form.bio.data != "":
        #     updated_teacher.teacher_bio = form.bio.data

        db.session.add(updated_teacher)
        db.session.commit()
        g.whichTeacher = updated_teacher
        form.fname.data = ""
        form.lname.data = ""
        form.bio.data = ""

    return render_template('tprofile.html', form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname =g.whichTeacher.teacher_lname)


# To Be done after updating models
@teachers_blueprint.route('/photo', methods =['GET' , 'POST'])
def photo():
    form = ProfileTab()
    if form.validate_on_submit():
       updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
       updated_teacher.teacher_fname = form.fname.data
       updated_teacher.teacher_lname = form.lname.data
       db.session.add(updated_teacher)
       db.session.commit()
       g.whichTeacher = updated_teacher
       form.fname.data = ""
       form.lname.data = ""
       form.description.data = ""

    return render_template('tphoto.html', form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname) 

@teachers_blueprint.route('/account', methods =['GET' , 'POST'])
def account():
    form = AccountTab()
    passwordChangeFailed = False 
    passwordMatchFailed = False 

    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        if not updated_teacher.check_password(form.password1.data):
            passwordChangeFailed = True
            return render_template('taccount.html', form = form, teacherLoggedIn = g.teacherLoggedIn, fname = g.whichTeacher.teacher_fname,
            lname = g.whichTeacher.teacher_lname, passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichTeacher.teacher_email ) 
            
        if form.password2.data == form.password3.data:
            updated_teacher.hash_password(form.password2.data)
            db.session.add(updated_teacher)
            db.session.commit()
            g.whichTeacher = updated_teacher
        else:
            passwordMatchFailed = True

    return render_template('taccount.html', form = form, teacherLoggedIn = g.teacherLoggedIn, fname = g.whichTeacher.teacher_fname,
        lname = g.whichTeacher.teacher_lname,passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichTeacher.teacher_email ) 


# To Be done after updating models
@teachers_blueprint.route('/payment_method', methods =['GET' , 'POST'])
def payment_method():
    form = ProfileTab()
    if form.validate_on_submit():
       updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
       updated_teacher.teacher_fname = form.fname.data
       updated_teacher.teacher_lname = form.lname.data
       db.session.add(updated_teacher)
       db.session.commit()
       g.whichTeacher = updated_teacher
       form.fname.data = ""
       form.lname.data = ""
       form.description.data = ""
    return render_template('tpayment_method.html', form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname) 

@teachers_blueprint.route('/privacy', methods =['GET' , 'POST'])
def privacy():
    form = PrivacyTab()
    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        if form.validate_on_submit():
            print(form.displayRank.data)
            print(form.displayStats.data)

            # additional code here
           
    return render_template('tprivacy.html', form = form, teacherLoggedIn = g.teacherLoggedIn ,  fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname)

@teachers_blueprint.route('/deactivate_account', methods =['GET' , 'POST'] )
def deactivate_account():
    form = DeactivateTab()
    passwordMatchFailed = False 

    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        print(updated_teacher.check_password(form.password.data))
        if updated_teacher.check_password(form.password.data):
            db.session.delete(updated_teacher)
            db.session.commit()
            whichTeacher = False
            g.teacherLoggedIn = False
            return redirect( url_for('teachers.signout') )
        else:
            print('here')
            passwordMatchFailed = True 

    return render_template('tdeactivate_account.html' , form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname, passwordMatchFailed = passwordMatchFailed)     