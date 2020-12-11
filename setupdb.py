from myproject import db
from myproject.models import Student, Courses

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

new_course = Courses('Web-Dev', 0)
db.session.add(new_course)
db.session.commit()


new_course = Courses('Physics', 0)
db.session.add(new_course)
db.session.commit()

new_course = Courses('Web-Scraping', 0)
db.session.add(new_course)
db.session.commit()