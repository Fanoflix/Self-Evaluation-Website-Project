from flask import Flask

class Assignment():
    def __init__(self, assignment_id, course_id, assignment_tag, tutor_id, diff, stars, review):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.assignment_tag = assignment_tag
        self.tutor_id = tutor_id
        self.diff = diff
        self.stars = stars
    
    def __repr__(self)
    return f"Assignment id: {self.assignment_id} belongs to course {self.course_id}" 
