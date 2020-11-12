from flask import Flask

class Preference():
    def __init__(self, student_id , course_name):
        self.student_id = student_id
        self.course_name = course_name
    
    def __repr__(self):
        return f"Student ID: {self.student_id} Course Name: {self.course_name}"