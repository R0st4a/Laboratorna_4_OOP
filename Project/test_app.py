from app import *
from models import *

from flask_testing import TestCase
import unittest
import requests
import json
import base64
from sqlalchemy.orm import close_all_sessions


class TestingUser(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        close_all_sessions()
        Base.metadata.create_all(engine)

    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(engine)

    def test_login_user(self):
        with app.test_client() as cl:
            user_data = {
                "name" : "user1",
                "email" : "user1@gmail.com",
                "password" : "pass",
                "status" : "teacher"
            }
            json_data= json.dumps(user_data).encode('utf-8')

            r = cl.open(path = '/courses/user', method = 'POST', data = json_data, headers={'Content-Type': 'application/json'})
            self.assertEqual(r.status_code, 200)

            login_data = {
                "email" : "user1@gmail.com",
                "password" : "pass"
            }
            json_data= json.dumps(login_data).encode('utf-8')

            r1 = cl.open(path = '/courses/user/login', method = 'POST', data = json_data, headers={'Content-Type': 'application/json'})
            self.assertEqual(r1.status_code, 200)

            login_data = {
                "email" : "user111@gmail.com",
                "password" : "passxxxx",
            }
            json_data= json.dumps(login_data).encode('utf-8')
            r2 = cl.open(path = '/courses/user/login', method = 'POST', data = json_data, headers={'Content-Type': 'application/json'})
            self.assertEqual(r2.status_code, 400)

    def test_logout_user(self):
        with app.test_client() as cl:
            r = cl.open(path = '/courses/user/logout', method = 'GET')
            self.assertEqual(r.status_code, 200)

    def test_add_user(self):
        with app.test_client() as cl:
            user_data1 = {
                "name" : "user1",
                "email" : "user1@gmail.com",
                "password" : "pass",
                "status" : "teacher"
            }
            user_data2 = {
                "name" : "user2",
                "email" : "user2@gmail.com",
                "password" : "pass",
                "status" : "student"
            }

            json_data1= json.dumps(user_data1).encode('utf-8')
            json_data2= json.dumps(user_data2).encode('utf-8')

            r1 = cl.open(path = '/courses/user', method = 'POST', headers={'Content-Type': 'application/json'})
            r2 = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
            r3 = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
            r4 = cl.open(path = '/courses/user', method = 'POST', data = json_data2, headers={'Content-Type': 'application/json'})

            self.assertEqual(r1.status_code, 400)
            self.assertEqual(r2.status_code, 200)
            self.assertEqual(r3.status_code, 400)
            self.assertEqual(r4.status_code, 200)


    def test_update_user(self):
        with app.test_client() as cl:
            user_data1 = {
                "name" : "user1",
                "email" : "user1@gmail.com",
                "password" : "pass",
                "status" : "teacher"
            }
            user_data2 = {
                "name" : "user2",
                "email" : "user2@gmail.com",
                "password" : "pass",
                "status" : "student"
            }

            json_data1= json.dumps(user_data1).encode('utf-8')
            json_data2= json.dumps(user_data2).encode('utf-8')

            rr = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
            rr = cl.open(path = '/courses/user', method = 'POST', data = json_data2, headers={'Content-Type': 'application/json'})


            new_user_data = {
                "name" : "userchanged",
                "email" : "userchanged@gmail.com",
                "password" : "pass",
                "status" : "teacher"
            }

            new_json_data = json.dumps(new_user_data).encode('utf-8')

            r1 = cl.open(path = '/courses/user/1', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1x@gmail.com:pass'.encode()).decode()})
            
            r2 = cl.open(path = '/courses/user/1', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r3 = cl.open(path = '/courses/user/1', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r4 = cl.open(path = '/courses/user/111', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r5 = cl.open(path = '/courses/user/xxx', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})


            self.assertEqual(r1.status_code, 403)
            self.assertEqual(r2.status_code, 200)
            self.assertEqual(r3.status_code, 403)
            self.assertEqual(r4.status_code, 400)
            self.assertEqual(r5.status_code, 400)


    def test_delete_user(self):
        with app.test_client() as cl:
            user_data1 = {
                "name" : "user1",
                "email" : "user1@gmail.com",
                "password" : "pass",
                "status" : "teacher"
            }
            user_data2 = {
                "name" : "user2",
                "email" : "user2@gmail.com",
                "password" : "pass",
                "status" : "student"
            }

            json_data1= json.dumps(user_data1).encode('utf-8')
            json_data2= json.dumps(user_data2).encode('utf-8')

            rr = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
            rr = cl.open(path = '/courses/user', method = 'POST', data = json_data2, headers={'Content-Type': 'application/json'})

            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : [2]
            }
            json_data3 = json.dumps(course_data).encode('utf-8')

            rr = cl.open(path = '/courses/course', method = 'POST', data = json_data3, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r1 = cl.open(path = '/courses/user/1', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            r5 = cl.open(path = '/courses/user/2', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            r2 = cl.open(path = '/courses/user/xxx', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            
            r3 = cl.open(path = '/courses/user/11', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r4 = cl.open(path = '/courses/user/1', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

        
        self.assertEqual(r1.status_code, 403)
        self.assertEqual(r2.status_code, 400)
        self.assertEqual(r3.status_code, 400)
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(r5.status_code, 200)
        

class TestingCourse(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        close_all_sessions()
        Base.metadata.create_all(engine)
        cl = app.test_client()

        user_data1 = {
            "name" : "user1",
            "email" : "user1@gmail.com",
            "password" : "pass",
            "status" : "teacher"
        }
        user_data2 = {
            "name" : "user2",
            "email" : "user2@gmail.com",
            "password" : "pass",
            "status" : "student"
        }
        user_data3 = {
            "name" : "user3",
            "email" : "user3@gmail.com",
            "password" : "pass",
            "status" : "student"
        }

        json_data1= json.dumps(user_data1).encode('utf-8')
        json_data2= json.dumps(user_data2).encode('utf-8')
        json_data3= json.dumps(user_data3).encode('utf-8')

        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data2, headers={'Content-Type': 'application/json'})
        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data3, headers={'Content-Type': 'application/json'})


    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(engine)



    def test_add_course(self):
        with app.test_client() as cl:
            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : [2,3]
            }
            json_data = json.dumps(course_data).encode('utf-8')

            r1 = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 2,
                "students" : [2,3]
            }
            json_data = json.dumps(course_data).encode('utf-8')

            r2 = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})
            
            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r2.status_code, 403)

            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : [2,3,4]
            }
            json_data = json.dumps(course_data).encode('utf-8')

            r1 = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 400)

            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 2,
                "students" : []
            }
            json_data = json.dumps(course_data).encode('utf-8')

            r1 = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 403)


    def test_update_course(self):
        with app.test_client() as cl:
            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : [2]
            }

            json_data = json.dumps(course_data).encode('utf-8')

            rr = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            new_course_data = {
                "name" : "Meth changed",
                "title" : "Intense course222",
                "owner_id" : 1,
                "students" : [2]
            }

            new_json_data = json.dumps(course_data).encode('utf-8')

            r1 = cl.open(path = '/courses/course/1', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            r2 = cl.open(path = '/courses/course/222', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            r3 = cl.open(path = '/courses/course/1', method = 'PUT', data = new_json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r2.status_code, 400)
            self.assertEqual(r3.status_code, 403)
            

    def test_delete_course(self):
        with app.test_client() as cl:
            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : [2]
            }

            json_data = json.dumps(course_data).encode('utf-8')

            rr = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})


            r1 = cl.open(path = '/courses/course/111', method = 'DELETE',
            headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            r2 = cl.open(path = '/courses/course/1', method = 'DELETE',
            headers={'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})
            r3 = cl.open(path = '/courses/course/1', method = 'DELETE',
            headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            
            self.assertEqual(r1.status_code, 400)
            self.assertEqual(r2.status_code, 403)
            self.assertEqual(r3.status_code, 200)


    def test_get_course_by_id(self):
        with app.test_client() as cl:

            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : []
            }

            json_data = json.dumps(course_data).encode('utf-8')

            rr = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r1 = cl.open(path = '/courses/course/1', method = 'GET')
            r2= cl.open(path = '/courses/course/222', method = 'GET')
            r3 = cl.open(path = '/courses/course/xxx', method = 'GET')

            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r2.status_code, 400)
            self.assertEqual(r3.status_code, 400)

    def test_get_courses(self):
        with app.test_client() as cl:
            course_data = {
                "name" : "Meth",
                "title" : "Intense course",
                "owner_id" : 1,
                "students" : []
            }

            json_data = json.dumps(course_data).encode('utf-8')

            rr = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            r = cl.open(path = '/courses/courses', method = 'GET')
            self.assertEqual(r.status_code, 200)

class TestingZapit(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        close_all_sessions()
        Base.metadata.create_all(engine)

        cl = app.test_client()

        user_data1 = {
            "name" : "user1",
            "email" : "user1@gmail.com",
            "password" : "pass",
            "status" : "teacher"
        }
        user_data2 = {
            "name" : "user2",
            "email" : "user2@gmail.com",
            "password" : "pass",
            "status" : "student"
        }
        user_data3 = {
            "name" : "user3",
            "email" : "user3@gmail.com",
            "password" : "pass",
            "status" : "student"
        }

        json_data1= json.dumps(user_data1).encode('utf-8')
        json_data2= json.dumps(user_data2).encode('utf-8')
        json_data3= json.dumps(user_data3).encode('utf-8')

        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data1, headers={'Content-Type': 'application/json'})
        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data2, headers={'Content-Type': 'application/json'})
        rr = cl.open(path = '/courses/user', method = 'POST', data = json_data3, headers={'Content-Type': 'application/json'})

        course_data = {
            "name" : "Meth",
            "title" : "Intense course",
            "owner_id" : 1,
            "students" : []
        }
        json_data = json.dumps(course_data).encode('utf-8')

        rr = cl.open(path = '/courses/course', method = 'POST', data = json_data, 
        headers={'Content-Type': 'application/json', 
        'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

    def tearDown(self):
        close_all_sessions()
        Base.metadata.drop_all(engine)

    def test_add_zapit(self):
        with app.test_client() as cl:
            zapit_data = {
                "owner_id" : 2,
                "id_course" : 1
            }
            json_data = json.dumps(zapit_data).encode('utf-8')

            r1 = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})
            r2 = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 200)
            self.assertEqual(r2.status_code, 403)

            zapit_data = {
                "owner_id" : 1,
                "id_course" : 1
            }
            json_data = json.dumps(zapit_data).encode('utf-8')

            r1 = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 403)

            zapit_data = {
                "owner_id" : 2,
                "id_course" : 40040440
            }
            json_data = json.dumps(zapit_data).encode('utf-8')

            r1 = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 404)


    def test_accept_zapit(self):
        with app.test_client() as cl:
            zapit_data = {
                "owner_id" : 2,
                "id_course" : 1
            }
            json_data = json.dumps(zapit_data).encode('utf-8')

            rr = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            self.assertEqual(rr.status_code, 200)


            r1 = cl.open(path = '/courses/zapit/accept/1', method = 'GET',
            headers={'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})
            r2 = cl.open(path = '/courses/zapit/accept/1', method = 'GET',
            headers={'Authorization': 'Basic ' + base64.b64encode('user3@gmail.com:pass'.encode()).decode()})
            r3 = cl.open(path = '/courses/zapit/accept/fdgf', method = 'GET',
            headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            r4 = cl.open(path = '/courses/zapit/accept/1', method = 'GET',
            headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 403)
            self.assertEqual(r2.status_code, 403)
            self.assertEqual(r3.status_code, 400)
            self.assertEqual(r4.status_code, 200)


    def test_delete_zapit(self):
        with app.test_client() as cl:
            zapit_data = {
                "owner_id" : 2,
                "id_course" : 1
            }
            json_data = json.dumps(zapit_data).encode('utf-8')

            rr = cl.open(path = '/courses/zapit', method = 'POST', data = json_data, 
            headers={'Content-Type': 'application/json', 
            'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})

            self.assertEqual(rr.status_code, 200)

            r1 = cl.open(path = '/courses/zapit/1', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user2@gmail.com:pass'.encode()).decode()})
            r2 = cl.open(path = '/courses/zapit/1', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user3@gmail.com:pass'.encode()).decode()})
            r3 = cl.open(path = '/courses/zapit/fdgf', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})
            r4 = cl.open(path = '/courses/zapit/1', method = 'DELETE',
                headers={'Authorization': 'Basic ' + base64.b64encode('user1@gmail.com:pass'.encode()).decode()})

            self.assertEqual(r1.status_code, 403)
            self.assertEqual(r2.status_code, 403)
            self.assertEqual(r3.status_code, 400)
            self.assertEqual(r4.status_code, 200)


if __name__ == '__main__':
    unittest.main()    