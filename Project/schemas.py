from marshmallow import Schema, fields, post_load, validates

class CreateUser(Schema):
    name = fields.String(required = True)
    email = fields.Email(required = True)
    password = fields.String()
    status = fields.String(required = True)

    @validates('status')
    def validate_status(self, status):
        if status != 'teacher' and status != 'student':
            raise ValidationError('invalid status')


class UserLogIn(Schema):
    email = fields.Email(required = True)
    password = fields.String(required = True)

 
class UserData(Schema):
    id = fields.Integer(required = True)
    name = fields.String(required = True)
    email = fields.Email(required = True)
    status = fields.String(required = True)


class CreateCourse(Schema):
    name = fields.String(required = True)
    title = fields.String(required = True)
    owner_id = fields.Integer(required = True)
    students = fields.List(fields.Integer())
    @validates('students')
    def validate_status(self, students):
        if len(students)>5:
            raise ValidationError('invalid student')


class CourseData(Schema):
    id = fields.Integer(required = True)
    name = fields.String(required = True)
    title = fields.String(required = True)
    owner_id = fields.Integer(required = True)
    students = fields.List(fields.Integer())
    @validates('students')
    def validate_status(self, students):
        if len(students)>5:
            raise ValidationError('invalid student')

class CreateZapit(Schema):
    owner_id = fields.Integer(required = True)
    id_course = fields.Integer(required = True)

class ZapitData(Schema):
    owner_id = fields.Integer(required = True)
    id_course = fields.Integer(required = True)
