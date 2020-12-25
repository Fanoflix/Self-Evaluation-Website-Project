from re import search
from flask import Blueprint,render_template,redirect,url_for,flash,session
from flask_login import login_user,login_required,logout_user,current_user
from myproject import db,g
from myproject.models import Teacher,Student
from myproject.teachers.forms import SignUp,LogIn, ProfileTab,AccountTab, PrivacyTab, DeactivateTab
from myproject.search.form import Searching
from sqlalchemy import func, and_

teachers_blueprint = Blueprint('teachers', __name__ , template_folder='templates/teachers')


# TEACHERS ( teacher_fname, teacher_lname, teacher_uname, teacher_email, teacher_password, teacher_rating, teacher_no_Of_reviews, teacher_account_status, teacher_bio )
@teachers_blueprint.route('/signup',  methods=['GET', 'POST'])
def signup():
    
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = SignUp()
    signupFailed1 = False
    signupFailed2 = False
    signupFailed3 = False

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        uname = form.uname.data
        email = form.email.data.lower()
        password1 = form.password1.data
        password2 = form.password2.data

        checkTeacherEmail = bool(Teacher.query.filter_by(teacher_email = email).first())
        checkStudentEmail = bool(Student.query.filter_by(student_email = email).first())
        checkTeacherUname = bool(Teacher.query.filter(func.lower(Teacher.teacher_uname) == func.lower(uname)).first())
        checkStudentUname = bool(Student.query.filter(func.lower(Student.student_uname) == func.lower(uname)).first())

        if checkTeacherUname or checkStudentUname: # Check if Uname is already taken
            return render_template('tsignup.html',form=form, signupFailed1 = True, searchForm = searchForm)        
        elif checkTeacherEmail or checkStudentEmail:  # Check if Email is already registered
            return render_template('tsignup.html',form=form, signupFailed2 = True, searchForm = searchForm)

        if password1 != '' and password1 == password2:
            new_teacher = Teacher(fname,lname,uname,email,password1,0,0,True,"")
            db.session.add(new_teacher)
            db.session.commit()
            return redirect(url_for('teachers.login'))
        else:
            return render_template('tsignup.html',form=form, signupFailed3 = True, searchForm = searchForm)
    
    return render_template('tsignup.html',form=form, searchForm = searchForm )


@teachers_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        
        CheckTeacher = Teacher.query.filter_by(teacher_email = email).first()

        if CheckTeacher != None and CheckTeacher.teacher_email == email and CheckTeacher.check_password(password):
            g.teacherLoggedIn = True
            g.whichTeacher = CheckTeacher
            return redirect( url_for('index') )
        else:
            return render_template('tlogin.html' , form=form , loginFailed = True, searchForm = searchForm)

        
    return render_template('tlogin.html' , form=form , loginFailed = False, searchForm = searchForm)
            
@teachers_blueprint.route('/')
def signout():
    g.teacherLoggedIn = False
    g.whichTeacher = False 
    return redirect( url_for('index') )


    
@teachers_blueprint.route('/profile', methods =['GET' , 'POST'])
def profile():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = ProfileTab()
    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        if form.uname.data != "":
            CheckStudent = bool(Student.query.filter(func.lower(Student.student_uname) == func.lower(form.uname.data)).first()) 
                                
            CheckTeacher = bool(Teacher.query.filter(
                                and_(
                                        (func.lower(Teacher.teacher_uname) == func.lower(form.uname.data)),
                                        (func.lower(Teacher.teacher_uname) != func.lower(updated_teacher.teacher_uname)),
                                    )
                                ).first())

            CheckUser = CheckTeacher or CheckStudent

            if not CheckUser:
                updated_teacher.teacher_uname = form.uname.data
            else:
                pass
        if form.fname.data != "":
            updated_teacher.teacher_fname = form.fname.data
        if form.lname.data != "":
            updated_teacher.teacher_lname = form.lname.data
        if form.bio.data != "":
            updated_teacher.teacher_bio = form.bio.data

        db.session.add(updated_teacher)
        db.session.commit()
        g.whichTeacher = updated_teacher
        form.uname.data = ""
        form.fname.data = ""
        form.lname.data = ""
        form.bio.data = ""

    return render_template('tprofile.html', form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname.capitalize() , lname =g.whichTeacher.teacher_lname.capitalize() , uname = g.whichTeacher.teacher_uname,bio = g.whichTeacher.teacher_bio, searchForm = searchForm)


# To Be done after updating models
@teachers_blueprint.route('/photo', methods =['GET' , 'POST'])
def photo():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('tphoto.html',  teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname, searchForm = searchForm)

@teachers_blueprint.route('/account', methods =['GET' , 'POST'])
def account():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = AccountTab()
    passwordChangeFailed = False 
    passwordMatchFailed = False 

    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        if not updated_teacher.check_password(form.password1.data):
            passwordChangeFailed = True
            return render_template('taccount.html', form = form, teacherLoggedIn = g.teacherLoggedIn, fname = g.whichTeacher.teacher_fname,
            lname = g.whichTeacher.teacher_lname, passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichTeacher.teacher_email, searchForm = searchForm ) 
            
        if form.password2.data == form.password3.data:
            updated_teacher.hash_password(form.password2.data)
            db.session.add(updated_teacher)
            db.session.commit()
            g.whichTeacher = updated_teacher
        else:
            passwordMatchFailed = True

    return render_template('taccount.html', form = form, teacherLoggedIn = g.teacherLoggedIn, fname = g.whichTeacher.teacher_fname,
        lname = g.whichTeacher.teacher_lname,passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed , userEmail = g.whichTeacher.teacher_email, searchForm = searchForm)


# To Be done after updating models
@teachers_blueprint.route('/payment_method', methods =['GET' , 'POST'])
def payment_method():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('tpayment_method.html',  teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname, searchForm = searchForm) 

@teachers_blueprint.route('/privacy', methods =['GET' , 'POST'])
def privacy():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = PrivacyTab()
    if form.validate_on_submit():
        updated_teacher = Teacher.query.filter_by(teacher_email = g.whichTeacher.teacher_email).first()
        if form.validate_on_submit():
            print(form.displayRank.data)
            print(form.displayStats.data)

            # additional code here
           
    return render_template('tprivacy.html', form = form, teacherLoggedIn = g.teacherLoggedIn ,  fname = g.whichTeacher.teacher_fname.capitalize() , lname = g.whichTeacher.teacher_lname.capitalize() , searchForm = searchForm)

@teachers_blueprint.route('/deactivate_account', methods =['GET' , 'POST'] )
def deactivate_account():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

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

    return render_template('tdeactivate_account.html' , form = form, teacherLoggedIn = g.teacherLoggedIn , fname = g.whichTeacher.teacher_fname, lname = g.whichTeacher.teacher_lname, passwordMatchFailed = passwordMatchFailed, searchForm = searchForm)     


@teachers_blueprint.route('/<uname>' , methods =['GET' , 'POST'])
def public_profile(uname):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    teacher = Teacher.query.filter_by(teacher_uname = uname).first()

    return render_template('tpublic_profile.html', teacher=teacher, searchForm = searchForm, teacherLoggedIn = g.teacherLoggedIn)