from myproject import app
from myproject import g 
from flask import render_template

g.init()

@app.route('/')
def index():
    studentLoggedIn = g.studentLoggedIn
    teacherLoggedIn = g.teacherLoggedIn
    return render_template('home.html' , studentLoggedIn = studentLoggedIn , teacherLoggedIn = teacherLoggedIn )

if __name__ == '__main__':
    app.run(debug=True)
