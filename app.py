from myproject import app
from myproject import g
from myproject.search.form import Searching
from flask import render_template,redirect,url_for

g.init()

@app.route('/' ,methods=['GET', 'POST'])
def index():
    
   
    g.searchForm = Searching()
    studentLoggedIn = g.studentLoggedIn
    teacherLoggedIn = g.teacherLoggedIn
    
    if g.searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = g.searchForm.searched.data))

    return render_template('home.html' , studentLoggedIn = studentLoggedIn , teacherLoggedIn = teacherLoggedIn, searchForm =g.searchForm)

if __name__ == '__main__':
    app.run(debug=True)
