from myproject import db
from myproject.models import  Courses

new_course = Courses('Software Development and Analysis', 0)
db.session.add(new_course)

new_course = Courses('Algorithms and Design', 0)
db.session.add(new_course)

new_course = Courses('Parallel and Distributed Computing', 0)
db.session.add(new_course)

new_course = Courses('Data Structures', 0)
db.session.add(new_course)

new_course = Courses('Object Oriented Programming', 0)
db.session.add(new_course)

new_course = Courses('Programmming Fundamentals', 0)
db.session.add(new_course)

new_course = Courses('Physics', 0)
db.session.add(new_course)

new_course = Courses('Chemistry', 0)
db.session.add(new_course)

new_course = Courses('Mathematics', 0)
db.session.add(new_course)

new_course = Courses('English', 0)
db.session.add(new_course)

new_course = Courses('Web Development', 0)
db.session.add(new_course)

new_course = Courses('Web Scrapping', 0)
db.session.add(new_course)


# will always be at the end.
new_course = Courses('Others', 0)
db.session.add(new_course)

db.session.commit()
