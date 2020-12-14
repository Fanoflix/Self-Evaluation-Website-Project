from myproject import db
from myproject.models import  Student, Teacher , Assignments, Assignment_Data, Settings, Courses, Preferences

new_course = Courses('database', 10)
db.session.add(new_course)

new_course = Courses('software development and analysis', 0)
db.session.add(new_course)

new_course = Courses('algorithms and design', 0)
db.session.add(new_course)

new_course = Courses('parallel and distributed computing', 1)
db.session.add(new_course)

new_course = Courses('data structures', 0)
db.session.add(new_course)

new_course = Courses('object oriented programming', 0)
db.session.add(new_course)

new_course = Courses('programmming fundamentals', 0)
db.session.add(new_course)

new_course = Courses('physics', 1)
db.session.add(new_course)

new_course = Courses('chemistry', 2)
db.session.add(new_course)

new_course = Courses('mathematics', 1)
db.session.add(new_course)

new_course = Courses('english', 1)
db.session.add(new_course)

new_course = Courses('web development', 9)
db.session.add(new_course)

new_course = Courses('web scrapping', 1)
db.session.add(new_course)

new_course = Courses('others', 0)
db.session.add(new_course)

new_teacher = Teacher('teach' , 'one' , 't1' , 'teach1@gmail.com' , '1234' , 1 , 10 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'two' , 't2' , 'teach2@gmail.com' , '1234' , 2 , 20 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'three' , 't3' , 'teach3@gmail.com' , '1234' , 3 , 30 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'four' , 't4' , 'teach4@gmail.com' , '1234' , 4 , 40 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'five' , 't5' , 'teach5@gmail.com' , '1234' , 5 , 50 , True , '')
db.session.add(new_teacher)

new_assignment = Assignments('Introduction to Physics' , 8 , 'expert' , 5 , 15750 , 1 , 1)
db.session.add(new_assignment)

new_assignment = Assignments('Electrochemistry' , 9 , 'expert' , 5 , 15750 , 1 , 2)
db.session.add(new_assignment)

new_assignment = Assignments('Organic Chemistry' , 9 , 'expert' , 5 , 15750 , 1 , 2)
db.session.add(new_assignment)

new_assignment = Assignments('Past,Present and Future Tense' , 11 , 'expert' , 5 , 15750 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('Test your Algebra Concepts' , 10 , 'expert' , 5 , 15750 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('OpenMP and MPI ' , 4 , 'expert' , 5 , 15750 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('Three Schema Architecture' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Normalization Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Serialization Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Transaction Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Key Constraints Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Integrity Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete MySql Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete MondoDB Practice' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('Introduction to ERD' , 1 , 'expert' , 5 , 15750 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Flask Practice' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('How to Nodejs' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('How to PHP' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('PHP and MySql' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('PHP and MongoDb' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('Intoduction to React' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('Scrapping using Scrappy' , 13 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Html5 Practice' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete CSS Practice' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete CSS Practice' , 12 , 'expert' , 5 , 15750 , 1 , 5)
db.session.add(new_assignment)

new_assignment_data = Assignment_Data(1,1,'How do you do when you cant do?','you do', 'you dont' ,'you cant' , 'you suck' ,'2')
db.session.add(new_assignment_data)

new_assignment_data = Assignment_Data(1,2,'What is your name?','I', 'you' ,'no' , 'yes' ,'4')
db.session.add(new_assignment_data)

new_assignment_data = Assignment_Data(1,3,'Is Abdullah a bot? Wrong answers only','yes', 'yes' ,'yes' , 'yes' ,'1')
db.session.add(new_assignment_data)

new_assignment_data = Assignment_Data(1,4,'You done fucked up','yes', 'no' ,'I am' , 'hahaha' ,'3')
db.session.add(new_assignment_data)

new_assignment_data = Assignment_Data(1,5,'How is testing going?','perfect', 'good' ,'not bad' , 'fucked' ,'4')
db.session.add(new_assignment_data)

db.session.commit()
