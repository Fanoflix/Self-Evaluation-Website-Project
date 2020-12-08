from myproject import db
from myproject.models import Student

# db.create_all()

searched = Student.query.filter_by(student_email = 'check1@gmail.com').first()
searched.student_rank = 151
print(searched.student_rank)