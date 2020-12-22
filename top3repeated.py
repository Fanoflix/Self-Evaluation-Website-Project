from myproject.models import Solved_Assignemnts,Courses, Solved_Assignemnts
import sys,copy
  
display_assignments = []
preffered_courses = []
        
for assignment in Solved_Assignemnts.query.filter_by(student_id = 2):
    preffered_courses.append(assignment.assignment.course.id)


Hash = dict() 
for i in range(len(preffered_courses)): 
    if preffered_courses[i] in Hash.keys(): 
        Hash[preffered_courses[i]] += 1
    else: 
        Hash[preffered_courses[i]] = 1

x = [0,-sys.maxsize]
y = [0, -sys.maxsize]
z = [0, -sys.maxsize]

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

print(x,y,z )




# max(Hash.items(),key = operator.itemgetter(1))
