from flask import Blueprint,render_template,redirect,url_for,flash,session
from myproject import db,g
from myproject.models import Teacher
from myproject.teachers.forms import SignUp,LogIn

teachers_blueprint = Blueprint('teachers', __name__ , template_folder='templates/teachers')

@teachers_blueprint.route('/signup',  methods=['GET', 'POST'])
def signup():
    form = SignUp()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 != '' and password1 == password2:
            new_teacher = Teacher(name,email,password1,0,0)
            db.session.add(new_teacher)
            db.session.commit()

            return redirect(url_for('index'))
    
    return render_template('tsignup.html',form=form )


@teachers_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():
    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        checkEmail = bool(Teacher.query.filter_by(teacher_email = email).first())

        if checkEmail:
            CheckTeacher = Teacher.query.filter_by(teacher_email = email).first()

            if CheckTeacher.teacher_email == email and CheckTeacher.teacher_password == password:
                g.teacherLoggedIn = True
                return redirect( url_for('index') )
            else:
                return render_template('tlogin.html' , form=form , loginFailed = True)

        else:
            return render_template('login.html' , form=form , loginFailed = True)
    return render_template('tlogin.html' , form=form , loginFailed = False)
            
@teachers_blueprint.route('/' )
def signout():
    g.teacherLoggedIn = False
    return redirect( url_for('index') )
