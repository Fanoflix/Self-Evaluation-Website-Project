from flask import Flask

class Student():
    def __init__(self, student_id, student_name, student_email, no_attempts, no_solved, rank):
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.no_attempts = no_attempts
        self.no_solved = no_solved
        self.rank = rank
