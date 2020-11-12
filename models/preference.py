from flask import Flask

class Preferences():
    def __init__(self, student_id , course_name):
        self.student_id = student_id
        self course_name = course_name
    
    def __repr__(self)
    return f"student_id: {self.student_id} is doing assignment related to course: {self.course}"