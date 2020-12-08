from models import Session, User, Course

session1 = Session()

user1 = User(id = 1, name = 'Bob', email = 'bobbobson@gmail.com', password = 'passwodr', status = 'teacher')
user2 = User(id = 2, name = 'John', email = 'bobbobsondsfsfd@gmail.com', password = 'passwodr', status = 'student')


course1 = Course(id = 1, name = 'math', title = 'lectures about bonk3', owner_id = 1, students = [])
course2 = Course(id = 2, name = 'pfysics', title = 'lectures about bonk3', owner_id = 1, students = [2])
course3 = Course(id = 3, name = 'literature', title = 'lectures about bonk3', owner_id = 2, students = [1,2])

session1.add(user1)
session1.add(user2)

session1.commit()

session1.add(course1)
session1.add(course2)
session1.add(course3)

session1.commit()

session1.close()