from flask import Flask

class Assignment():
    def __init__(self, assignment_id, course_id, assignment_tag, tutor_id, difficulty, stars):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.assignment_tag = assignment_tag
        self.tutor_id = tutor_id
        self.difficulty = difficulty
        self.stars = stars
    
    def __repr__(self):
        print("---------------------------------------------------------")
        print(f"Assignment ID: {self.assignment_id} Course: {self.course_id}")
        print(f"Tutor ID: {self.tutor_id} Difficulty Level: {self.difficulty}")
        print(f"Stars: {self.stars} ")
        return "---------------------------------------------------------"

