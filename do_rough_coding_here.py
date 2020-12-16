from myproject import db
from myproject.models import Student, Courses, Assignments,Assignment_Data, Assignment_Review, Saved_Assignemnts

# # db.create_all()

# searched = Student.query.filter_by(student_fname = 'check').all()
# print(searched)



# count = 1
# for q in range(5):
#     print('choice'+ str(count))
#     count = count + 1

# a sample 
# questions = [ 
#               ['1','1','How do you do when you cant do?','you do', 'you dont' ,'you cant' , 'you suck' ,'2'] ,
#               ['1','2','What is your name?','I', 'you' ,'no' , 'yes' ,'4'] ,
#               ['1','3','Is Abdullah a bot? Wrong answers only','yes', 'yes' ,'yes' , 'yes' ,'1'] ,
#               ['1','4','You done fucked up','yes', 'no' ,'I am' , 'hahaha' ,'3'] ,
#               ['1','5','How is testing going?','perfect', 'good' ,'not bad' , 'fucked' ,'4'] 
#             ]
    

# records = []
# row = []

# for record in Student.query.filter_by(student_fname = 'check').all():
# for record in questions:
#     for x in range(2,8):
#         row.append(record[x])
#     # row.append(record.student_fname)
#     # row.append(record.student_lname)
#     records.append(row)
#     row = []


# for i in range(len(records)):
#     print(records[i])
#     print("\n")


# print(len(Student.query.filter_by(student_fname = 'check').all()))

# new_course = Courses('Software Development and Analysis', 0)
# db.session.add(new_course)
# db.session.commit()


# new_course = Courses('Algorithms and Design', 0)
# db.session.add(new_course)
# db.session.commit()

# new_course = Courses('Parallel and Distributed Computing', 0)
# db.session.add(new_course)
# db.session.commit()


# for x in range(10):
#     print(x+1)


# print(len(Courses.query.all()))

# searched = Assignments.query.filter_by(assignment_name = 'a1').first()

# Courses.__table__.drop(db.engine)
# Assignments.__table__.drop(db.engine)
# Assignment_Data.__table__.drop(db.engine)

student = Student('Abdullah', 'Raheel', 'Ar', 'asd@asd', 'asd', 1, 1, 1, 1, '', True, 1)
db.session.add(student)
db.session.commit()

review = Assignment_Review(1, 1, 'Mahad lund')
db.session.add(review)
db.session.commit()

save = Saved_Assignemnts(1, 1)
db.session.add(save)
db.session.commit()

check_save = Saved_Assignemnts.query.filter_by(assignment_id = 1).first()
review_1 = Assignment_Review.query.filter_by(assignment_id = 1).first()
# print(review_1.assignment_name)
print(review_1.assignment.assignment_name)
print(review_1.assignment.course_id)
print(review_1.assignment.difficulty)
print(review_1.assignment.assignment_rating)
print('\n\n\n')
print(check_save.assignment.assignment_name)
print(check_save.student.student_fname)


