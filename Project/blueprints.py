from flask import Blueprint, jsonify, request
from schemas import *
from models import *


blpr = Blueprint("courses", __name__)


@blpr.route("/user", methods=["POST"])
def create_user():
    try:
        user_data = CreateUser().load(request.json)
        user_obj = User(**user_data)

        session = Session()
        session.add(user_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "User data error"}))

    return jsonify(UserData().dump(user_obj)), 200


@blpr.route("/user/login", methods = ["GET"])
def user_login():
    try:
        user_data = UserLogIn().load(request.json)
    
    except Exception:
        return(jsonify({"code": 400 ,"error": "Invalid username or password"}))
    
    return jsonify({"Successful login": 200})
    
@blpr.route("/user/logout", methods = ["GET"])
def user_logout():
    return jsonify({"Successful logout": 200})


@blpr.route("/user/<id>", methods = ["DELETE"])
def del_user(id):
    try:
        session = Session()
        session.query(User).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong user id"}))

    return jsonify({"User deleted ": 200})  

@blpr.route("/course", methods=["POST"])
def create_course():
    try:
        course_data = CreateCourse().load(request.json)
        course_obj = Course(**course_data)

        session = Session()
        session.add(course_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Course data error"}))

    return jsonify(CourseData().dump(course_obj)), 200


@blpr.route("/course/<id>", methods = ["DELETE"])
def del_course(id):
    try:
        session = Session()
        session.query(Course).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong course id"}))

    return jsonify({"Course deleted ": 200})  

@blpr.route("/course/<id>", methods = ["PUT"])
def update_course(id):
    try:
        session = Session()
    
        course_data = CreateCourse().load(request.json)
        orig_course_data = session.query(Course).filter_by(id = id).one()

        for key, value in course_data.items():
            setattr(orig_course_data, key, value)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Course data error"}))

    return jsonify(CourseData().dump(orig_course_data)), 200


@blpr.route("/course/<id>", methods = ["GET"])
def get_course(id):
    try:
        session = Session()
    
        course_obj = session.query(Course).filter_by(id = id).one()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Invalid course id"}))

    return jsonify(CourseData().dump(course_obj)), 200

@blpr.route("/courses", methods = ["GET"])
def get_all_courses():
    try:
        session = Session()
        all_courses = session.query(Course).all()
    except Exception:
        return jsonify({"code":400,"error": "Eror"})

    return jsonify(CourseData(many = True).dump(all_courses)),200


