from myproject import db
from myproject.models import Student, Courses, Assignments,Assignment_Data, Assignment_Review, Solved_Assignemnts,Settings

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

# student = Student('Abdullah', 'Raheel', 'Ar', 'asd@asd', 'asd', 1, 1, 1, 1, '', True, 1)
# db.session.add(student)
# db.session.commit()

# review = Assignment_Review(1, 1, 'Mahad lund')
# db.session.add(review)
# db.session.commit()

# save = Saved_Assignemnts(1, 1)
# db.session.add(save)
# db.session.commit()

# check_save = Saved_Assignemnts.query.filter_by(assignment_id = 1).first()
# review_1 = Assignment_Review.query.filter_by(assignment_id = 1).first()
# # print(review_1.assignment_name)
# print(review_1.assignment.assignment_name)
# print(review_1.assignment.course_id)
# print(review_1.assignment.difficulty)
# print(review_1.assignment.assignment_rating)
# print('\n\n\n')
# print(check_save.assignment.assignment_name)
# print(check_save.student.student_fname)

# arr = [  ]

# if arr != []: # if not empty
#     review_no = arr[-1]["key2"] + 1 # add 1 to last review_id
# else:  
#     review_no = 1
# #endif

# print(review_no)


student = Student.query.filter_by(id = 2).first()
student.student_rank = 1
db.session.add(student)
student = Student.query.filter_by(id = 1).first()
student.student_rank = 2
db.session.add(student)
student = Student.query.filter_by(id = 3).first()
student.student_rank = 3
db.session.add(student)
db.session.commit()
# settig = Settings.query.filter_by(student_id = 3).first()
# solve = Solved_Assignemnts.query.filter_by(student_id = 3).first()
# db.session.delete(settig)
# db.session.delete(solve)
# db.session.delete(student)


# Updating the Leaderboard
# ========================
# old_rank_points = 200
# student = Student.query.filter_by(id =1).first()

# #student_new_position
# new_rank_points = (100 * student.student_solved) /student.student_attempted 

# #finding all the students who have attempted atleast one assignment, sorted by thier rank in asc order.
# all_students = Student.query.order_by(Student.student_rank.asc()).filter(Student.student_attempted > 0)

# # counting no of students in all_students
# no_of_students = 0
# for studs in all_students:
#     no_of_students += 1

# # check if there is only one student and his rank is 0 and he has passed the assignment.
# if no_of_students == 1:        
#     for stud in all_students:
#         stud.student_rank = 1
#         db.session.add(stud)
#     #endfor    
# # if more than one student (here there will always  be one student with rank = 1st)
# elif no_of_students > 1: 
#     print("no_of_students > 1")
#     found = False
#     less = False
#     temp = 1
#     for stud in all_students:
#         print(f"Stud.id:{stud.id}") 
#         if stud.id == student.id:
#             print(f"Stud.id:{stud.id} {student.id}:Student.id")
#             if stud.student_rank == 0:
#                 student.student_rank = no_of_students
#                 print('rank = 0')

#             if old_rank_points > new_rank_points:
#                 continue

#             break
#         #endif

#         position  = (stud.student_score * stud.student_solved) /stud.student_attempted
#         if new_rank_points > position and old_rank_points <= new_rank_points:
#             print(f"Greater  {new_rank_points} > {position}")
#             temp = student.student_rank
#             print(f"temp = {temp}")
#             new_rank = int(stud.student_rank)
#             print(f"student_rank: {student.student_rank}")
#             print(f"stud_rank: {stud.student_rank}")
#             # db.session.add(student)
#             found = True
#             break

#         elif old_rank_points > new_rank_points and stud.student_rank > student.student_rank:
#             new_rank = stud.student_rank
#             print(new_rank)
#             less = True
#         #endif    
#     #endfor
# #endif

# if found == True:
#     print(f"found = {found}")
#     for stud in all_students:
#         print(f"stud.id: {stud.id}")
#         if stud.student_rank == temp:
#             break
#         #endif
#         if stud.student_rank >= new_rank:
#             print(f"stud_before_rank: {stud.student_rank}")
#             stud.student_rank +=  1
#             print(f"stud_after_rank: {stud.student_rank}")
#             db.session.add(stud)
#         #endif
#     #endfor 
#     student.student_rank = new_rank
#     db.session.add(student)
# elif less == True:
#     print(f"less = {less}")
#     for stud in all_students:
#         print(f"stud.id: {stud.id}")
#         if stud.student_rank == new_rank + 1:
#             break
#         #endif
#         if stud.student_rank > student.student_rank:
#             print(f"stud_before_rank: {stud.student_rank}")
#             stud.student_rank -= 1
#             print(f"stud_after_rank: {stud.student_rank}")
#             db.session.add(stud)
#         #endif
#     #endfor 
#     student.student_rank = new_rank
#     db.session.add(student)
# #endif   

# db.session.commit()

