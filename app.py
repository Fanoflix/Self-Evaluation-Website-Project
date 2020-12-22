from myproject import app
from myproject import g
from myproject.search.form import Searching
from myproject.models import Assignments, Solved_Assignemnts
from sqlalchemy import desc,and_
from flask import render_template,redirect,url_for
from flask_login import current_user
import sys,copy

g.init()

@app.route('/' ,methods=['GET', 'POST'])
def index():
    all_assignments = []
    recomended_assignments_x = []
    recomended_assignments_y = []
    recomended_assignments_z = []
    top_pick = None
    
    
    # Finding his preferences
    if current_user.is_authenticated:
        x = [0,-sys.maxsize]
        y = [0, -sys.maxsize]
        z = [0, -sys.maxsize]

        # Displaying Random Assignments
        assignments = Assignments.query.order_by(Assignments.assignment_rating.desc()).filter(
                and_(
                    Assignments.course_id != x[0],
                    Assignments.course_id != y[0],
                    Assignments.course_id != z[0],
                )
        )
        
        for assignment in assignments:
            check = Solved_Assignemnts.query.filter(
                                            and_(
                                                    Solved_Assignemnts.assignment_id.like(assignment.id),
                                                    Solved_Assignemnts.student_id.like(current_user.id),
                                            )
                            ).first()
            if check == None:
                all_assignments.append(assignment)
                
            if len(all_assignments) == 8:
                break
        #endfor

        preffered_courses = []
        count_assignments = 0
        for assignment in Solved_Assignemnts.query.filter_by(student_id = current_user.id):
            preffered_courses.append(assignment.assignment.course.id)
            count_assignments += 1
        #endfor


        if count_assignments > 5:
            Hash = dict() 
            for i in range(len(preffered_courses)): 
                if preffered_courses[i] in Hash.keys(): 
                    Hash[preffered_courses[i]] += 1
                else: 
                    Hash[preffered_courses[i]] = 1
                #endif
            #endfor

            for cid in Hash:
                if Hash[cid] > 1 and Hash[cid] > x[1]:
                    z = copy.deepcopy(y)
                    y = copy.deepcopy(x)

                    x[0] = cid
                    x[1] = Hash[cid]
        
                elif Hash[cid] > 1 and Hash[cid] > y[1]:
                    z = copy.deepcopy(y)

                    y[0] = cid
                    y[1] = Hash[cid]

                elif Hash[cid] > 1 and Hash[cid] > z[1]:
                    z[0] = cid
                    z[1] = Hash[cid]
            #endfor

            if x[0] == 0:
                x = list(Hash.items())[-1]
                y = list(Hash.items())[-2]
                z = list(Hash.items())[-3]
            elif y[0] == 0:
                del Hash[x[0]]
                y = list(Hash.items())[-1]
                z = list(Hash.items())[-2]
            elif z[0] == 0:
                del Hash[x[0]]
                del Hash[y[0]]
                z = list(Hash.items())[-1]
            #endif


            #Student Course-wise Preferences
            for assignment in Assignments.query.order_by(Assignments.assignment_rating.desc()).filter_by(course_id = x[0]):
                
                check = Solved_Assignemnts.query.filter(
                                        and_(
                                                Solved_Assignemnts.assignment_id.like(assignment.id),
                                                Solved_Assignemnts.student_id.like(current_user.id),
                                        )
                        ).first()
                if check == None:
                    recomended_assignments_x.append(assignment)
                if len(recomended_assignments_x) == 4:
                    break

            for assignment in Assignments.query.order_by(Assignments.assignment_rating.desc()).filter_by(course_id = y[0]):
                check = Solved_Assignemnts.query.filter(
                                        and_(
                                                Solved_Assignemnts.assignment_id.like(assignment.id),
                                                Solved_Assignemnts.student_id.like(current_user.id),
                                        )
                        ).first()
                if check == None:
                    recomended_assignments_y.append(assignment)
                if len(recomended_assignments_y) == 4:
                    break

            for assignment in Assignments.query.order_by(Assignments.assignment_rating.desc()).filter_by(course_id = z[0]):
                check = Solved_Assignemnts.query.filter(
                                        and_(
                                                Solved_Assignemnts.assignment_id.like(assignment.id),
                                                Solved_Assignemnts.student_id.like(current_user.id),
                                        )
                        ).first()
                if check == None:
                    recomended_assignments_z.append(assignment)

                if len(recomended_assignments_z) == 4:
                    break
            
            # finding the TOP PICK
            for assignment in Assignments.query.filter_by(course_id = x[0]).order_by(Assignments.assignment_rating.desc(),
                                    Assignments.assignment_no_of_reviews.desc()):
                check = Solved_Assignemnts.query.filter(
                                        and_(
                                                Solved_Assignemnts.assignment_id.like(assignment.id),
                                                Solved_Assignemnts.student_id.like(current_user.id),
                                        )
                        ).first()
                if check == None and assignment.assignment_rating >= 4.0:
                    top_pick = assignment
                    break
                #endif
            #endfor

            if top_pick != None:
                for assignment in Assignments.query.filter_by(course_id = y[0]).order_by(Assignments.assignment_rating.desc(),
                                        Assignments.assignment_no_of_reviews.desc()):
                    check = Solved_Assignemnts.query.filter(
                                            and_(
                                                    Solved_Assignemnts.assignment_id.like(assignment.id),
                                                    Solved_Assignemnts.student_id.like(current_user.id),
                                            )
                            ).first()
                    if check == None:
                        if top_pick.assignment_rating < assignment.assignment_rating:
                            top_pick = assignment
                        
                        elif top_pick.assignment_rating == assignment.assignment_rating:
                            if top_pick.assignment_no_of_reviews < assignment.assignment_no_of_reviews:
                                top_pick = assignment
                        
                        break
                    #endif
                #endfor
                
                for assignment in Assignments.query.filter_by(course_id = z[0]).order_by(Assignments.assignment_rating.desc(),
                                        Assignments.assignment_no_of_reviews.desc()):
                    check = Solved_Assignemnts.query.filter(
                                            and_(
                                                    Solved_Assignemnts.assignment_id.like(assignment.id),
                                                    Solved_Assignemnts.student_id.like(current_user.id),
                                            )
                            ).first()
                    if check == None:
                        if top_pick.assignment_rating < assignment.assignment_rating:
                            top_pick = assignment
                        
                        elif top_pick.assignment_rating == assignment.assignment_rating:
                            if top_pick.assignment_no_of_reviews < assignment.assignment_no_of_reviews:
                                top_pick = assignment
                        
                        break
                    #endif
                #endfor
            #endif
    else:
        all_assignments = Assignments.query.order_by(Assignments.assignment_rating.desc()).limit(16)
    #endif
    
    searchForm = Searching()
    if searchForm.validate_on_submit():
        return redirect(url_for('search.searching', searched = searchForm.searched.data))
    #endif

    return render_template('home.html' , teacherLoggedIn = g.teacherLoggedIn, all_assignments = all_assignments, recomended_assignments_x = recomended_assignments_x, recomended_assignments_y = recomended_assignments_y, recomended_assignments_z = recomended_assignments_z, top_pick = top_pick,  searchForm =searchForm)

if __name__ == '__main__':
    app.run(debug=True)