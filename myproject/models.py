from myproject import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer,primary_key= True)
    teacher_fname = db.Column(db.Text)
    teacher_lname = db.Column(db.Text)
    teacher_email = db.Column(db.Text)
    teacher_password = db.Column(db.Text)
    teacher_rating = db.Column(db.Float)
    teacher_no_Of_reviews = db.Column(db.Integer)

    def __init__(self, teacher_fname, teacher_lname, teacher_email, teacher_password, teacher_rating, teacher_no_Of_reviews):
        self.teacher_fname = teacher_fname
        self.teacher_lname = teacher_lname
        self.teacher_email = teacher_email
        self.teacher_password = teacher_password
        self.teacher_rating = teacher_rating
        self.teacher_no_Of_reviews = teacher_no_Of_reviews

    def __repr__(self):
        return f"Teacher Id: {self.teacher_id} First Name: {self.teacher_fname} Last Name: {self.teacher_lname}"

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key= True)
    student_fname = db.Column(db.Text)
    student_lname = db.Column(db.Text)
    student_email = db.Column(db.Text)
    student_password = db.Column(db.Text)
    student_attempted = db.Column(db.Integer)
    student_solved = db.Column(db.Integer)
    student_rank = db.Column(db.Integer)

    def __init__(self, student_fname, student_lname, student_email, student_password,student_attempted, student_solved, student_rank):
        self.student_fname = student_fname
        self.student_lname = student_lname
        self.student_email = student_email
        self.student_password = student_password
        self.student_attempted = student_attempted
        self.student_solved = student_solved
        self.student_rank = student_rank
    
    def __repr__(self):
       return f"Student Id: {self.student_id} First Name: {self.student_fname} Last Name: {self.student_lname}"
        



































# class Puppy(db.Model):

#     __tablename__ = 'puppies'
#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.Text)
#     owner = db.relationship('Owner',backref='puppy',uselist=False)

#     def __init__(self,name):
#         self.name = name

#     def __repr__(self):
#         if self.owner:
#             return f"Puppy name is {self.name} and owner is {self.owner.name}"
#         else:
#             return f"Puppy name is {self.name} and has no owner assigned yet."

# class Owner(db.Model):

#     __tablename__ = 'owners'

#     id = db.Column(db.Integer,primary_key= True)
#     name = db.Column(db.Text)
#     # We use puppies.id because __tablename__='puppies'
#     puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))

#     def __init__(self,name,puppy_id):
#         self.name = name
#         self.puppy_id = puppy_id

#     def __repr__(self):
#         return f"Owner Name: {self.name}"