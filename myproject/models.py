from collections import UserList
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from myproject import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(student_id):
    return Student.query.get(student_id)

    
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer,primary_key = True)
    teacher_fname = db.Column(db.Text)
    teacher_lname = db.Column(db.Text)
    teacher_uname = db.Column(db.Text, unique=True)
    teacher_email = db.Column(db.Text)
    teacher_password_hash = db.Column(db.Text)
    teacher_rating = db.Column(db.Float)
    teacher_no_Of_reviews = db.Column(db.Integer)
    teacher_account_status = db.Column(db.Boolean)
    teacher_bio = db.Column(db.Text)

    def __init__(self, teacher_fname, teacher_lname, teacher_uname, teacher_email, teacher_password, teacher_rating, teacher_no_Of_reviews, teacher_account_status, teacher_bio):
        self.teacher_fname = teacher_fname
        self.teacher_lname = teacher_lname
        self.teacher_uname = teacher_uname
        self.teacher_email = teacher_email
        self.teacher_password_hash = generate_password_hash(teacher_password)
        self.teacher_rating = teacher_rating
        self.teacher_no_Of_reviews = teacher_no_Of_reviews
        self.teacher_account_status = teacher_account_status
        self.teacher_bio = teacher_bio

    def check_password(self, mypassword):
        return check_password_hash(self.teacher_password_hash, mypassword)
    
    def hash_password(self, mypassword):
        self.teacher_password_hash = generate_password_hash(mypassword)

    def __repr__(self):
        return f"Teacher Id: {self.id} First Name: {self.teacher_fname} Last Name: {self.teacher_lname}"

class Student(db.Model,UserMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key = True)
    student_fname = db.Column(db.Text)
    student_lname = db.Column(db.Text)
    student_uname = db.Column(db.Text, unique=True)
    student_email = db.Column(db.Text)
    student_password_hash = db.Column(db.Text)
    student_attempted = db.Column(db.Integer)
    student_solved = db.Column(db.Integer)
    student_rank = db.Column(db.Integer)
    student_score = db.Column(db.Integer)
    student_bio = db.Column(db.Text)
    student_account_status = db.Column(db.Boolean)
    student_privacy_settings = db.Column(db.Integer)

    # Backrefs
    settings = db.relationship('Settings', backref='Settings_JOIN_Student', uselist=False) # One to One relationship: Student can have 1 setting


    def __init__(self, student_fname, student_lname, student_uname, student_email, student_password,student_attempted, student_solved, student_rank, student_score, student_bio, student_account_status, student_privacy_settings):
        self.student_fname = student_fname
        self.student_lname = student_lname
        self.student_email = student_email
        self.student_uname = student_uname
        self.student_password_hash = generate_password_hash(student_password)
        self.student_attempted = student_attempted
        self.student_solved = student_solved
        self.student_rank = student_rank
        self.student_score = student_score
        self.student_bio = student_bio
        self.student_account_status = student_account_status
        self.student_solved = student_solved
        self.student_privacy_settings = student_privacy_settings
    
    def check_password(self, mypassword):
        return check_password_hash(self.student_password_hash, mypassword)

    def hash_password(self, mypassword):
        self.student_password_hash = generate_password_hash(mypassword)

    def __repr__(self):
       return f"Student Id: {self.id} First Name: {self.student_fname} Last Name: {self.student_lname}"

class Settings(db.Model):
    __tablename__ = 'settings'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key = True) # Can be a PK because its a 1-1 Relationship
    display_rank = db.Column(db.Boolean)
    display_stats = db.Column(db.Boolean)
    student = db.relationship('Student', backref="Student_JOIN_Settings", uselist = False) # Backref

    def __init__(self, student_id, display_rank, display_stats):
        self.student_id = student_id
        self.display_rank = display_rank
        self.display_stats = display_stats
    
    # Function that returns settings code
    def return_setting_preset(self):
        if self.display_rank and self.display_stats:
            return 1 # Display both == 1
        elif self.display_rank and not self.display_stats:
            return 2 # Display rank only == 2
        elif self.display_stats and not self.display_rank:
            return 3 # Display stats only == 3
        else:
            return 4 # Hide both == 4
 
class Courses(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.Text , unique = True)
    no_of_assignments = db.Column(db.Integer)

    def __init__(self, course_name, no_of_assigmnets):
        self.course_name = course_name
        self.no_of_assignments = no_of_assigmnets


class Assignments(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key = True)
    assignment_name = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id')) # Assignment tag
    course = db.relationship('Courses', backref='Courses_JOIN_Assignments') # Backref
    difficulty = db.Column(db.Text)
    assignment_rating = db.Column(db.Float)
    assignment_no_of_reviews = db.Column(db.Integer)
    assignment_no_of_ratings = db.Column(db.Integer)
    active_status = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', backref=backref("Teacher_JOIN_Assignments", cascade="all,delete")) # Backref

    def __init__(self, assignment_name, course_id, difficulty, assignment_rating, assignment_no_of_reviews, assignment_no_of_ratings, active_status, teacher_id):
        self.assignment_name = assignment_name
        self.course_id = course_id
        self.difficulty = difficulty
        self.assignment_rating = assignment_rating
        self.assignment_no_of_reviews = assignment_no_of_reviews
        self.assignment_no_of_ratings = assignment_no_of_ratings
        self.active_status = active_status
        self.teacher_id = teacher_id
        

class Assignment_Review(db.Model):
    __tablename__ = 'assignment_review'
    
    review_id = db.Column(db.Integer)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_rating = db.Column(db.Float)
    review_text = db.Column(db.Text)
    
    assignment = db.relationship('Assignments', backref = backref("Assignment_Review_JOIN_Assignments", cascade="all,delete")) #(not redundent)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            review_id, assignment_id, student_id
        ),
    )

    def __init__(self, review_id, assignment_id, student_id, assignment_rating, review_text):
        self.review_id = review_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.assignment_rating = assignment_rating
        self.review_text = review_text


class Assignment_Data(db.Model):
    __tablename__ = 'assignment_data'
    
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    question_id = db.Column(db.Integer)
    question_text = db.Column(db.Text)
    
    assignment = db.relationship('Assignments', backref = backref("Assignment_Data_JOIN_Assignments", cascade="all,delete")) # Backref
    choice1 = db.Column(db.Text)
    choice2 = db.Column(db.Text)
    choice3 = db.Column(db.Text)
    choice4 = db.Column(db.Text)
    answer = db.Column(db.Text)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            assignment_id, question_id,
        ),
    )

    def __init__(self, assignment_id, question_id, question_text,choice1, choice2, choice3, choice4, answer):
        self.assignment_id = assignment_id
        self.question_id = question_id
        self.question_text = question_text
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3
        self.choice4 = choice4
        self.answer = answer

class Solved_Assignemnts(db.Model):
    __tablename__ = 'solved_assignments'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    points = db.Column(db.Integer)
    student = db.relationship('Student', backref="Solved_Assignemnts_JOIN_Student")
    assignment = db.relationship('Assignments', backref=backref("Solved_Assignemnts_JOIN_Assignments", cascade="all,delete"))

    __table_args__ = (
        db.PrimaryKeyConstraint(
            student_id, assignment_id,
        ),
    )
    
    def __init__(self, student_id, assignment_id, points):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.points = points

class Classroom(db.Model):
    __tablename__ = 'classroom'

    id = db.Column(db.Integer, primary_key = True)
    classroom_name = db.Column(db.Text)
    classroom_section = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', backref=backref("Classroom_JOIN_Teacher", cascade="all,delete")) # 
    
    def __init__(self, classroom_name, classroom_section, teacher_id):
        self.classroom_name = classroom_name
        self.classroom_section = classroom_section
        self.teacher_id = teacher_id


class Students_in_Classroom(db.Model):
    __tablename__ = 'students_in_classroom'

    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    classroom = db.relationship('Classroom', backref=backref("Students_in_Classroom_JOIN_Classroom", cascade="all,delete"))
    student = db.relationship('Student', backref="Students_in_Classroom_JOIN_Student")

    __table_args__ = (
        db.PrimaryKeyConstraint(
           classroom_id, student_id,
        ),
    )

    def __init__(self, classroom_id, student_id):
        self.classroom_id = classroom_id
        self.student_id = student_id


class Assignments_in_Classroom(db.Model):
    __tablename__ = 'assignments_in_classroom'

    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    deadline = db.Column(db.DateTime)
    classroom = db.relationship('Classroom', backref=backref("Assignments_in_Classroom_JOIN_Classroom", cascade="all,delete"))
    assignment = db.relationship('Assignments', backref=backref("Assignments_in_Classroom_JOIN_Assignments", cascade="all,delete"))

    __table_args__ = (
        db.PrimaryKeyConstraint(
           classroom_id, assignment_id,
        ),
    )

    def __init__(self, classroom_id, assignment_id, deadline):
        self.classroom_id = classroom_id
        self.assignment_id = assignment_id
        self.deadline = deadline 


class Solved_Classroom_Assignment(db.Model):
    __tablename__ = 'solved_classroom_assignments'

    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    points = db.Column(db.Integer)
                                        
    classroom = db.relationship('Classroom', backref=backref("Solved_Classroom_Assignment_JOIN_Classroom", cascade="all,delete"))
    student = db.relationship('Student', backref="Solved_Classroom_Assignment_JOIN_Student")
    assignment = db.relationship('Assignments' , backref=backref("Solved_Classroom_Assignment_JOIN_Assignments", cascade="all,delete"))
    
    __table_args__ = (
        db.PrimaryKeyConstraint(
           classroom_id, student_id, assignment_id,
        ),
    )
    def __init__(self, classroom_id, assignment_id, student_id, points):
        self.classroom_id = classroom_id
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.points = points