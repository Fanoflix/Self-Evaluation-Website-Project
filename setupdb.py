from myproject import db
from myproject.models import Puppy,Owner,Student

# db.create_all()

Student.query.filter_by(student_email = "check1@gmail.com").delete()
db.session.commit()