import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class Solve():
    def __init__(self, student_id, assignment_id):
        self.student_id = student_id
        self.assignment_id = assignment_id
    
    def __repr__(self):
        return f"Student {self.student_id} solves the assignment {self.assignment_id}"