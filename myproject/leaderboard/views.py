from re import search
from flask import Blueprint, render_template, redirect, url_for
from myproject import db
from myproject.models import Student
from sqlalchemy import desc
from myproject.search.form import Searching

leaderboard_blueprint = Blueprint('leaderboard', __name__, template_folder='templates/leaderboard')

@leaderboard_blueprint.route('/')
def display_leaderboard():
    searchForm = Searching()
    if searchForm.searched.data != '' and  searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))

    # leaderboard contains all the students with score > 0 in descending order
    leaderboard = Student.query.order_by(Student.student_score.desc()).filter(Student.student_score > 0)

    return render_template('leaderboard.html', leaderboard=leaderboard, searchForm = searchForm)