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
    user = session.query(User).filter_by(email = username).first()
    user_puf = User("0","0","0","0")
    if user != None and check_password_hash(user.password,password):
        return user
    else:
        return user_puf



@blpr.route("/user", methods=["POST"])
def create_user():
    try:
        user_data = CreateUser().load(request.json)
        user_obj = User(**user_data)
    
        session = Session()
        session.add(user_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "User data error"})), 400

    return jsonify(UserData().dump(user_obj)), 200

@blpr.route("/user/login", methods = ["POST"])
def user_login():
    try:
        session = Session()
        user_data = UserLogIn().load(request.json)

        base_user_data = session.query(User).filter_by(email = user_data['email']).one()
    
    except Exception:
        return(jsonify({"code": 400 ,"error": "Invalid username or password"})), 400
    
    return jsonify(UserData().dump(base_user_data)), 200
    
@blpr.route("/user/logout", methods = ["GET"])
def user_logout():
    return jsonify({"Successful logout": 200}), 200


@blpr.route("/user/<id>", methods = ["PUT"])
@auth.login_required
def update_user(id):
    try:
        session = Session()
        user = auth.current_user()

        user_data = CreateUser().load(request.json)
        user_obj = User(**user_data)
        user_data = CreateUser().dump(user_obj)

        orig_user_data = session.query(User).filter_by(id = id).one()

        if user.id != orig_user_data.id:
            return (jsonify({"code": 403, "error": "You aren`t owner"})), 403


        for key, value in user_data.items():
            setattr(orig_user_data, key, value)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "User data error"})), 400

    return jsonify(UserData().dump(orig_user_data)), 200


@blpr.route("/user/<id>", methods = ["DELETE"])
@auth.login_required
def del_user(id):
    try:
        session = Session()
        user = auth.current_user()

        user_data = session.query(User).filter_by(id = id).one()

        for i in range(20):
            data = session.query(Course).filter_by(id = int(i)).first()
            if data != None:
                for d in data.students:
                    if d == int(id):
                        uchni = data.students
                        uchni.pop(uchni.index(d))
                        setattr(data,"students",uchni)
                        session.query(Course).filter_by(id = int(i)).update({"students": uchni})
                data = None

        if user.id != int(id):
            return (jsonify({"code": 403, "error": "You aren`t owner"})), 403

        if user.status != 'student':
            object_t = session.query(Course).filter_by(owner_id = user.id).delete()
    
        session.query(User).filter_by(id=id).delete()
        session.commit()
        return jsonify({"User deleted ": 200}), 200
    except Exception:
        return(jsonify({"code": 400 ,"error": "User data error"})), 400




@blpr.route("/course", methods=["POST"])
@auth.login_required
def create_course():
    try:
        session = Session()
        user = auth.current_user()
        
        course_data = CreateCourse().load(request.json)
        course_obj = Course(**course_data)

        if course_obj.owner_id != user.id:
            return (jsonify({"code": 403, "error": "Not your id"})), 403

        if user.status != 'teacher':
            return (jsonify({"code": 403, "error": "You aren`t teacher"})), 403

        for i in course_obj.students:
            data = session.query(User).filter_by(id = i).first()
            if data == None:
                return (jsonify({"code": 400, "error": "NO such user id"})), 400
                
        course_obj = Course(**course_data)

        session.add(course_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Course data error"})), 400

    return jsonify(CourseData().dump(course_obj)), 200


@blpr.route("/course/<id>", methods = ["DELETE"])
@auth.login_required
def del_course(id):
    try:
        session = Session()
        user = auth.current_user()
        data = session.query(Course).filter_by(id=id).one()
        if user.id != data.owner_id:
            return (jsonify({"code": 403, "error": "You aren`t owner"})), 403
        session.query(Course).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong course id"})),400

    return jsonify({"Course deleted ": 200}), 200  

@blpr.route("/course/<id>", methods = ["PUT"])
@auth.login_required
def update_course(id):
    try:
        session = Session()
        user = auth.current_user()
        data = session.query(Course).filter_by(id=id).one()

        if user.id != data.owner_id:
            return (jsonify({"code": 403, "error": "You aren`t owner"})), 403

        course_data = CreateCourse().load(request.json)
        course_obj = Course(**course_data)
        orig_course_data = session.query(Course).filter_by(id = id).one()

        for i in course_obj.students:
            data = session.query(User).filter_by(id = i).first()
            if data == None:
                return (jsonify({"code": 400, "error": "NO such user id"})), 400

        for key, value in course_data.items():
            setattr(orig_course_data, key, value)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Course data error"})), 400

    return jsonify(CourseData().dump(orig_course_data)), 200

@blpr.route("/course/<id>", methods = ["GET"])
def get_course(id):
    try:
        session = Session()
    
        course_obj = session.query(Course).filter_by(id = id).one()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Invalid course id"})), 400

    return jsonify(CourseData().dump(course_obj)), 200

@blpr.route("/courses", methods = ["GET"])
def get_all_courses():
    session = Session()
    all_courses = session.query(Course).all()

    return jsonify(CourseData(many = True).dump(all_courses)),200





@blpr.route("/zapit", methods=["POST"])
@auth.login_required
def create_zapit():
    try:
        session = Session()
        user = auth.current_user()
        zapit_data = CreateZapit().load(request.json)
        zapit_obj = Zapit(**zapit_data)
        if user.status != 'student':
            return (jsonify({"code": 403, "error": "You aren`t student"})), 403

        if user.id != zapit_obj.owner_id:
            return (jsonify({"code": 403, "error": "You can`t add another user"})), 403

        data = session.query(Course).filter_by(id = zapit_obj.id_course).first()

        if data == None:
            return (jsonify({"code": 404, "error": "NO id of course"})), 404

        if zapit_obj.owner_id in data.students:
            return (jsonify({"code": 403, "error": "You already in course"})), 403

        session.add(zapit_obj)
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong user id"})), 400

    return jsonify(ZapitData().dump(zapit_obj)),200 

@blpr.route("/zapit/accept/<id>", methods=["GET"])
@auth.login_required
def accept_zapit(id):
    try:
        session = Session()
        user = auth.current_user()

        zapit_obj = session.query(Zapit).filter_by(id = id).one()
        course_obj = session.query(Course).filter_by(id = zapit_obj.id_course).one()
        if user.status != 'teacher':
            return (jsonify({"code": 403, "error": "You aren`t teacher"})), 403
        
        if user.id != course_obj.owner_id:
            return (jsonify({"code": 403, "error": "You aren`t owner"})), 403

        if len(course_obj.students) > 4:
            return (jsonify({"code": 409, "error": "NO SPACE ONLY 5 CAN BE"})), 409

        uchni = course_obj.students
        uchni.append(zapit_obj.owner_id)
        setattr(course_obj,"students",uchni)
        session.query(Zapit).filter_by(id=id).delete()
        session.query(Course).filter_by(id = zapit_obj.id_course).update({"students": uchni})
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong user id"})), 400

    return jsonify(CourseData().dump(course_obj)), 200

@blpr.route("/zapit/<id>", methods = ["DELETE"])
@auth.login_required
def delete_zapit(id):
    try:
        session = Session()
        user = auth.current_user()

        zapit_obj = session.query(Zapit).filter_by(id = id).one()
        course_obj = session.query(Course).filter_by(id = zapit_obj.id_course).one()

        if user.status != 'teacher':
            return (jsonify({"code": 400, "error": "You aren`t teacher"})), 403

        if user.id != course_obj.owner_id:
            return (jsonify({"code": 400, "error": "You aren`t course owner"})), 403

        session.query(Zapit).filter_by(id=id).delete()
        session.commit()

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong course id"})), 400

    return jsonify({"Zapit deleted ": 200}), 200
