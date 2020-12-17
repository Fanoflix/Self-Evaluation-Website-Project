def init():
    global studentLoggedIn
    global teacherLoggedIn
    global whichStudent
    global whichTeacher
    global total_reviews

    studentLoggedIn = False
    teacherLoggedIn = False
    whichStudent = False
    whichTeacher = False
    total_reviews = False

# Auto increments only works on primary keys (looked it up and tried) so had to make a gobal Variable -Abdullah