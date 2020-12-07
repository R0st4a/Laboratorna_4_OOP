from models import Session, User, Course

session1 = Session()

user1 = User(id = 1, name = 'Bob', email = 'bobbobson@gmail.com', password = 'passwodr', status = 'teacher')
course1 = Course(id = 3, name = 'mafth3', title = 'lectures about bonk3', owner_id = 1, students = [])

# session1.add(user1)
session1.add(course1)

session1.commit()

session1.close()