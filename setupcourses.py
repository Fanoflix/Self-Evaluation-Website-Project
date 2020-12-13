from myproject import db
from myproject.models import  Courses

# new_course = Courses('software development and analysis', 0)
# db.session.add(new_course)

# new_course = Courses('algorithms and design', 0)
# db.session.add(new_course)

# new_course = Courses('parallel and distributed computing', 0)
# db.session.add(new_course)

# new_course = Courses('data structures', 0)
# db.session.add(new_course)

# new_course = Courses('object oriented programming', 0)
# db.session.add(new_course)

# new_course = Courses('programmming fundamentals', 0)
# db.session.add(new_course)

# new_course = Courses('physics', 0)
# db.session.add(new_course)

# new_course = Courses('chemistry', 0)
# db.session.add(new_course)

# new_course = Courses('mathematics', 0)
# db.session.add(new_course)

# new_course = Courses('english', 0)
# db.session.add(new_course)

# new_course = Courses('web development', 0)
# db.session.add(new_course)

# new_course = Courses('web scrapping', 0)
# db.session.add(new_course)


# # will always be at the end.
new_course = Courses('others', 0)
db.session.add(new_course)

# searched = Courses.query.filter_by(course_name = "Others").first()
# db.session.delete(searched)
db.session.commit()
