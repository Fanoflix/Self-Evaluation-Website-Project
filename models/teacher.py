from db import db


class Teacher(): 
    def __init__(self, tid, username, password):
        self.tid = tid
        self.username = username
        self.password = password
    
    @classmethod
    def findbytid(cls, tid):
        cur = db.cursor()
        sql = "SELECT * FROM teachers WHERE id = %s"
        cur.execute(sql, (tid,)) # Sending only the tid here but in tuple form (tid, )
        result = cur.fetchall()
        if result:
            print(result)
            # teacher = Teacher(*result)
            # print(teacher)
        cur.close()

    def __repr__(self):
        print(f"{self.tid} {self.username} {self.password}")
