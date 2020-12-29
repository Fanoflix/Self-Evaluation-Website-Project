from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from flask_login import login_user,login_required,logout_user,current_user
from myproject import db,g
from myproject.models import Student, Teacher, Settings,Students_in_Classroom,Solved_Classroom_Assignment,Solved_Assignemnts,Assignment_Review, Assignments
from myproject.students.forms import SignUp,LogIn,ProfileTab,AccountTab,PrivacyTab,DeactivateTab
from myproject.search.form import Searching
from sqlalchemy import func, and_

students_blueprint = Blueprint('students', __name__ , template_folder='templates/students')

@students_blueprint.route('/signup',  methods=['GET', 'POST'])
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
        checkStudentEmail = bool(Student.query.filter_by(student_email=email).first())
        checkTeacherUname = bool(Teacher.query.filter(func.lower(Teacher.teacher_uname) == func.lower(uname)).first())
        checkStudentUname = bool(Student.query.filter(func.lower(Student.student_uname) == func.lower(uname)).first())

         
        if checkTeacherUname or checkStudentUname: # Check if Uname is already taken
            return render_template('signup.html',form=form, signupFailed1 = True, searchForm = searchForm)      
        elif checkTeacherEmail or checkStudentEmail:  # Check if Email is already registered
            return render_template('signup.html',form=form, signupFailed2 = True, searchForm = searchForm)
       

        if password1 != '' and password1 == password2:
                new_student = Student(fname, lname, uname, email, password1, 0, 0, 0, 0, "", True, 4)
                db.session.add(new_student)
                db.session.commit()
                settings = Settings(new_student.id, True, True)
                db.session.add(settings)
                db.session.commit()
                return redirect(url_for('students.login'))
        else:
            return render_template('signup.html',form=form, signupFailed3 = True, searchForm = searchForm)
    
    return render_template('signup.html',form=form, searchForm = searchForm )


@students_blueprint.route('/login' , methods =['GET' , 'POST'])
def login():

    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    form = LogIn()
    loginFailed = False

    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        CheckStudent = Student.query.filter_by(student_email = email).first()

        if CheckStudent != None and CheckStudent.student_email == email and CheckStudent.check_password(password):
            login_user(CheckStudent)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')

            # session['user'] = 'student'
            return redirect(next)
        else:
            return render_template('login.html' , form=form , loginFailed = True, searchForm = searchForm)

    return render_template('login.html', form=form, loginFailed = False, searchForm = searchForm)
            
@students_blueprint.route('/' )
@login_required
def signout():
    logout_user()
    return redirect( url_for('index') )

@students_blueprint.route('/profile',  methods =['GET' , 'POST'])
@login_required
def profile():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = ProfileTab()

    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = current_user.student_email).first()
        if form.uname.data != "":

            CheckTeacher = bool(Teacher.query.filter(func.lower(Teacher.teacher_uname) == func.lower(form.uname.data)).first()) 
                                
            CheckStudent = bool(Student.query.filter(
                                and_(
                                        (func.lower(Student.student_uname) == func.lower(form.uname.data)),
                                        (func.lower(Student.student_uname) != func.lower(current_user.student_uname)),
                                    )
                                ).first())

            CheckUser = CheckTeacher or CheckStudent

            if not CheckUser:
                user.student_uname = form.uname.data
            else:
                pass

        if form.fname.data != "":
            user.student_fname = form.fname.data
        if form.lname.data != "":
            user.student_lname = form.lname.data
        if form.bio.data != "":
            user.student_bio = form.bio.data    
        db.session.add(user)
        db.session.commit()
        form.fname.data = ""
        form.lname.data = ""
        form.bio.data = ""
        form.uname.data = ""

    return render_template('profile.html', form = form, fname = current_user.student_fname, lname = current_user.student_lname, searchForm = searchForm )   


@students_blueprint.route('/photo'  , methods =['GET' , 'POST'])
@login_required
def photo():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('photo.html',  fname = current_user.student_fname, lname = current_user.student_lname, searchForm = searchForm) 

@students_blueprint.route('/account',  methods =['GET' , 'POST'] )
@login_required
def account():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    
    form = AccountTab()
    passwordChangeFailed = False 
    passwordMatchFailed = False 

    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = current_user.student_email).first()
        if not user.check_password(form.password1.data):
            passwordChangeFailed = True
            return render_template('account.html', form = form, fname = current_user.student_fname,
            lname = current_user.student_lname, passwordChangeFailed = passwordChangeFailed,passwordMatchFailed = passwordMatchFailed ,  searchForm = searchForm) 
            
        if form.password2.data == form.password3.data:
            user.hash_password(form.password2.data)
            db.session.add(user)
            db.session.commit()
        else:
            passwordMatchFailed = True

    return render_template('account.html', form = form, fname = current_user.student_fname,
        lname = current_user.student_lname, passwordChangeFailed = passwordChangeFailed ,passwordMatchFailed = passwordMatchFailed, searchForm = searchForm ) 

@students_blueprint.route('/payment_method' , methods =['GET' , 'POST'])
@login_required
def payment_method():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    return render_template('payment_method.html', fname = current_user.student_fname, lname = current_user.student_lname,  searchForm = searchForm)

@students_blueprint.route('/privacy',  methods =['GET' , 'POST']  )
@login_required
def privacy():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    user = Settings.query.filter_by(student_id= current_user.id).first()
    displayRankCheck = user.display_rank
    displayStatCheck = user.display_stats

    form = PrivacyTab()
    if form.validate_on_submit():
        
        if form.validate_on_submit():
            user.display_rank = form.displayRank.data
            user.display_stats = form.displayStats.data 
            displayRankCheck = user.display_rank
            displayStatCheck = user.display_stats   
            
            db.session.add(user)
            db.session.commit()
           
    return render_template('privacy.html', form = form,  fname = current_user.student_fname, lname = current_user.student_lname,  searchForm = searchForm, displayRankCheck = displayRankCheck, displayStatCheck = displayStatCheck )  

@students_blueprint.route('/deactivate_account' ,  methods =['GET' , 'POST'] )
@login_required
def deactivate_account():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    form = DeactivateTab()
    passwordMatchFailed = False 
    if form.validate_on_submit():
        user = Student.query.filter_by(student_email = current_user.student_email).first()
       
        if user.check_password(form.password.data):
            
            for q in Students_in_Classroom.query.filter_by(student_id = current_user.id).all():
                db.session.delete(q)
            
            for q in Solved_Classroom_Assignment.query.filter_by(student_id = current_user.id).all():
                db.session.delete(q)
            
            for q in Solved_Assignemnts.query.filter_by(student_id = current_user.id).all():
                db.session.delete(q)
            
            for q in Assignment_Review.query.filter_by(student_id = current_user.id).all():
                # Now updating Assignment assignment_rating,assignment_no_of_reviews and assignment_no_of_ratings.
                assignment = Assignments.query.filter_by(id = q.assignment_id).first()
                assignment.assignment_no_of_reviews -= 1
                if assignment.assignment_no_of_ratings == 1:
                    assignment.assignment_rating = 0
                else:
                    assignment.assignment_rating = ( (assignment.assignment_rating * assignment.assignment_no_of_ratings) - float(q.assignment_rating)) / (assignment.assignment_no_of_ratings - 1)
                #endif
                assignment.assignment_no_of_ratings -= 1
                db.session.add(assignment)
                
                # Now updating Teacher teacher_rating and teacher_no_Of_reviews.
                teacher = Teacher.query.filter_by(id = q.assignment.teacher_id).first()
                teacher_assignments = Assignments.query.filter_by(teacher_id = teacher.id).all()
                db.session.delete(q)
                db.session.commit()

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
                    teacher.teacher_no_Of_reviews -= 1
                #endif
                db.session.add(teacher)
                db.session.commit()
            #endfor

            settings = Settings.query.filter_by(student_id = current_user.id).first()
            db.session.delete(settings)
            db.session.delete(user)
            db.session.commit()
            return redirect( url_for('students.signout') )
        else:
            passwordMatchFailed = True 

    return render_template('deactivate_account.html', form = form, fname = current_user.student_fname, lname = current_user.student_lname, passwordMatchFailed = passwordMatchFailed, searchForm = searchForm)


@students_blueprint.route('/<uname>' , methods =['GET' , 'POST'])
def public_profile(uname):
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    student = Student.query.filter_by(student_uname = uname).first()

    # Calculating student's accuracy
    accuracy = 0
    if student.student_attempted != 0:
        accuracy = (student.student_solved/student.student_attempted)*100
    return render_template('spublic_profile.html', student=student, searchForm = searchForm, accuracy=accuracy)
