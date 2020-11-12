from flask import Flask

class Student():
    def __init__(self, student_id, student_name, student_email, no_attempts, no_solved, rank):
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.no_attempts = no_attempts
        self.no_solved = no_solved
        self.rank = rank

    def __repr__(self, student_id, student_name, student_email, no_attempts, no_solved, rank):
        print("---------------------------------------------------------")
        print(f"ID: {self.student_id} Name: {self.student_name}")
        print(f"Email: {self.student_email} Attempts: {self.no_attempts} Solved: {self.no_solved} Rank: self{self.rank}")
        print("---------------------------------------------------------")
