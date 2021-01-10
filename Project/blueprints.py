from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from schemas import *
from models import *


blpr = Blueprint("courses", __name__)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_passsword(username,password):
    session = Session()
    user = session.query(User).filter_by(email = username).one()
    if check_password_hash(user.password,password):
        return user

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


@blpr.route("/user/<id>", methods = ["PUT"])
@auth.login_required
def update_user(id):
    try:
        session = Session()
        user = auth.current_user()
        course_data = CreateUser().load(request.json)
        orig_course_data = session.query(User).filter_by(id = id).one()
        if user.id != orig_course_data.id:
            return (jsonify({"code": 400, "error": "You aren`t owner"}))

        for key, value in course_data.items():
            setattr(orig_course_data, key, value)
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "User data error"}))

    return jsonify(UserData().dump(orig_course_data)), 200

@blpr.route("/user/<int:id>", methods = ["DELETE"])
@auth.login_required
def del_user(id):
    
    session = Session()
    user = auth.current_user()
    if user.id != id:
        return (jsonify({"code": 400, "error": "You aren`t owner"}))
    for i in range(20):
        data = session.query(Course).filter_by(id = int(i)).first()
        if data != None:
            for d in data.students:
                if d == id:
                    uchni = data.students
                    uchni.pop(uchni.index(d))
                    setattr(data,"students",uchni)
                    session.query(Course).filter_by(id = int(i)).update({"students": uchni})
            data = None
    if user.status != 'student':
        object_t = session.query(Course).filter_by(owner_id = user.id).delete()
    
    session.query(User).filter_by(id=id).delete()
    session.commit()
    return jsonify({"User deleted ": 200})  



@blpr.route("/zapit", methods=["POST"])
@auth.login_required
def create_zapit():
    try:
        session = Session()
        user = auth.current_user()
        zapit_data = CreateZapit().load(request.json)
        zapit_obj = Zapit(**zapit_data)
        if user.status != 'student':
            return (jsonify({"code": 400, "error": "You aren`t student"}))

        if user.id != zapit_obj.owner_id:
            return (jsonify({"code": 400, "error": "You aren`t add another user"}))
        data = session.query(Course).filter_by(id = zapit_obj.id_course).first()
        if data == None:
            return (jsonify({"code": 400, "error": "NO id of course"}))

        session.add(zapit_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong user id"}))

    return jsonify(ZapitData().dump(zapit_obj)),200 

@blpr.route("/zapit/accept/<int:id>", methods=["GET"])
@auth.login_required
def accept_zapit(id):
    try:
        session = Session()
        user = auth.current_user()
        zapit_obj = session.query(Zapit).filter_by(id = id).one()
        course_obj = session.query(Course).filter_by(id = zapit_obj.id_course).one()
        if user.status != 'teacher':
            return (jsonify({"code": 400, "error": "You aren`t teacher"}))
        
        if user.id != course_obj.owner_id:
            return (jsonify({"code": 400, "error": "You aren`t owner"}))

        if len(course_obj.students) > 4:
            return (jsonify({"code": 400, "error": "NO SPACE ONLY 5 CAN BE"}))

        uchni = course_obj.students
        uchni.append(zapit_obj.owner_id)
        setattr(course_obj,"students",uchni)
        session.query(Zapit).filter_by(id=id).delete()
        session.query(Course).filter_by(id = zapit_obj.id_course).update({"students": uchni})
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong user id"}))

    return jsonify(CourseData().dump(course_obj)), 200

@blpr.route("/zapit/<id>", methods = ["DELETE"])
@auth.login_required
def delete_zapit(id):
    try:
        session = Session()
        user = auth.current_user()
        if user.status != 'teacher':
            return (jsonify({"code": 400, "error": "You aren`t teacher"}))
        session.query(Zapit).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong course id"}))

    return jsonify({"Zapit deleted ": 200})  


@blpr.route("/course", methods=["POST"])
@auth.login_required
def create_course():
    try:
        session = Session()
        user = auth.current_user()
        if user.status != 'teacher':
            return (jsonify({"code": 400, "error": "You aren`t teacher"}))
        course_data = CreateCourse().load(request.json)
        course_obj = Course(**course_data)
        for i in course_obj.students:
            data = session.query(User).filter_by(id = i).first()
            if data == None:
                return (jsonify({"code": 400, "error": "NO id"}))
                
        course_obj = Course(**course_data)

        session.add(course_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Course data error"}))

    return jsonify(CourseData().dump(course_obj)), 200


@blpr.route("/course/<id>", methods = ["DELETE"])
@auth.login_required
def del_course(id):
    try:
        session = Session()
        user = auth.current_user()
        data = session.query(Course).filter_by(id=id).one()
        if user.id != data.owner_id:
            return (jsonify({"code": 400, "error": "You aren`t owner"}))
        session.query(Course).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong course id"}))

    return jsonify({"Course deleted ": 200})  

@blpr.route("/course/<id>", methods = ["PUT"])
@auth.login_required
def update_course(id):
    try:
        session = Session()
        user = auth.current_user()
        data = session.query(Course).filter_by(id=id).one()
        if user.id != data.owner_id:
            return (jsonify({"code": 400, "error": "You aren`t owner"}))
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


