from myproject import db
from myproject.models import  Student, Teacher , Assignments, Assignment_Data, Settings, Courses

new_course = Courses('Database', 10)
db.session.add(new_course)

new_course = Courses('Software Development And Analysis', 0)
db.session.add(new_course)

new_course = Courses('Algorithms And Design', 0)
db.session.add(new_course)

new_course = Courses('Parallel And Distributed Computing', 1)
db.session.add(new_course)

new_course = Courses('Data Structures', 0)
db.session.add(new_course)

new_course = Courses('Object Oriented Programming', 0)
db.session.add(new_course)

new_course = Courses('Programmming Fundamentals', 0)
db.session.add(new_course)

new_course = Courses('Physics', 1)
db.session.add(new_course)

new_course = Courses('Chemistry', 2)
db.session.add(new_course)

new_course = Courses('Mathematics', 1)
db.session.add(new_course)

new_course = Courses('English', 1)
db.session.add(new_course)

new_course = Courses('Web Development', 9)
db.session.add(new_course)

new_course = Courses('Web Scrapping', 1)
db.session.add(new_course)

new_course = Courses('Others', 0)
db.session.add(new_course)

new_teacher = Teacher('teach' , 'one' , 't1' , 'teach1@gmail.com' , '1234' , 1 , 10 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'two' , 't2' , 'teach2@gmail.com' , '1234' , 2 , 20 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'three' , 't3' , 'teach3@gmail.com' , '1234' , 3 , 30 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'four' , 't4' , 'teach4@gmail.com' , '1234' , 4 , 40 , True , '')
db.session.add(new_teacher)

new_teacher = Teacher('teach' , 'five' , 't5' , 'teach5@gmail.com' , '1234' , 5 , 50 , True , '')
db.session.add(new_teacher)

new_assignment = Assignments('Introduction to Physics' , 8 , 'Expert' , 0 , 0 , 0 , 1 , 1)
db.session.add(new_assignment)

new_assignment = Assignments('Electrochemistry' , 9 , 'Expert' , 0 , 0 , 0 , 1 , 2)
db.session.add(new_assignment)

new_assignment = Assignments('Organic Chemistry' , 9 , 'Expert' , 0 , 0 , 0 , 1 , 2)
db.session.add(new_assignment)

new_assignment = Assignments('Past,Present and Future Tense' , 11 , 'Expert' , 0 , 0 , 0 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('Test your Algebra Concepts' , 10 , 'Expert' , 0 , 0 , 0 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('OpenMP and MPI ' , 4 , 'Expert' , 0 , 0 , 0 , 1 , 3)
db.session.add(new_assignment)

new_assignment = Assignments('Three Schema Architecture' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Normalization Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Serialization Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Transaction Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Key Constraints Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Integrity Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete MySql Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete MondoDB Practice' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('Introduction to ERD' , 1 , 'Expert' , 0 , 0 , 0 , 1 , 4)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Flask Practice' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('How to Nodejs' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('How to PHP' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('PHP and MySql' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('PHP and MongoDb' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('Intoduction to React' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('Scrapping using Scrappy' , 13 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete Html5 Practice' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete CSS Practice' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

new_assignment = Assignments('The Complete CSS Practice' , 12 , 'Expert' , 0 , 0 , 0 , 1 , 5)
db.session.add(new_assignment)

for x in range(1, 11):
    new_assignment_data = Assignment_Data(x,1,'The function f(x) = x^3 - 6x^2 + 9x + 25 has', 'a maxima at x= 1 and a minima at x = 3', 'a maxima at x = 3 and a minima at x = 1' ,'no maxima, but a minima at x = 1', 'a maxima at x = 1, but no minima', '1')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,2,'The interval in which the Lagranges theorem is applicable for the function f(x) = 1/x is', '[-3, 3]', '[-2, 2]', '[2, 3]', '[-1, 1]', '3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,3,'If f(x) = | x | , then for interval [-1, 1] ,f(x)', 'satisied all the conditions of Rolles Theorem', 'satisfied all the conditions of Mean Value Theorem' ,'does not satisied the conditions of Mean Value Theorem' , 'None of these' ,'3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,4,'The minimum value of | x2 _ 5x + 21 | is', '-5', '0', '-1', '-2' ,'2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,5,'f(x) =  | x | at x = 0', '1', '-1', '0', 'Does Not Exists', '4')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,6,'Minimum point of the function f(x) = (x^3)/x', 'x = 1', 'x = -1', 'x = 0', 'x = 1/√3', '3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,7,'If f (0) = 2 and f (x) = 1/(5-x2), then lower and upper bound of f(1) estimated by the mean value theorem are', '1.9, 2.2', '2.2, 2.25', '2.25, 2.5', 'None of these', '2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,8,'The unit normal to the plane 2x +y + 2z = 6 can be expressed in the vector form as', 'i3 + j2 + k2', '2i/3 + j/3 + 2k/3', 'i/3 + j/2 + k/2', '2i/3 + j/3 + 2k/3', '2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,9,'Maxima and Minima occur', 'simultaneously', 'once', 'alternately', 'rarely', '3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,10, 'If x + y = k, x > 0, y > 0, then xy is maximum when', 'x = ky', 'kx = y', 'x = y', 'None of these', '3')
    db.session.add(new_assignment_data)

    db.session.commit()


for x in range(11, 26):
    new_assignment_data = Assignment_Data(x,1,'The walls of a particle in a box are supposed to be', 'Small but infinitely hard', 'Infinitely large but soft', 'Soft and Small', 'Infinitely hard and infinitely large', '4')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,2,'The wave function of the particle lies in which region?', 'x > 0', 'x < 0', '0 < x < L', 'x > L', '3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,3,'The particle loses energy when it collides with the wall', 'True', 'False' ,'Neither', 'Both' ,'2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,4,'The Energy of the particle is proportional to', 'n', 'n^-1', 'n^2', 'n^-2' ,'3')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,5,'For a particle inside a box, the potential is maximum at x =', 'L', '2L', 'L/2', '3L', '1')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,6,'The Eigen value of a particle in a box is', 'L/2', '2/L', '√L/2', '√2/L', '4')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,7,'Particle in a box can never be at rest', 'True', 'False' ,'Neither', 'Both', '1')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,8,'What is the minimum Energy possessed by the particle in a box', '0', 'π^2 * h^2/2mL^2', 'π^2 * h^2/2mL', 'π^2 * h/2mL', '2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,9,'What is the quantum state which has a wave function similar to the sin(x) wave function', '1', '2', '3', '4', '2')
    db.session.add(new_assignment_data)

    new_assignment_data = Assignment_Data(x,10, 'Calculate the Zero-point energy for a particle in an infinite potential well for an electron confined to a 1 nm atom', '3.9 X 10^-29 J', '4.9 X 10^-29 J', '5.9 X 10^-29 J', '6.9 X 10^-29 J', '3')
    db.session.add(new_assignment_data)

    db.session.commit()

