from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:147896325@localhost/lab", echo = True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User (Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    email = Column('email', String, unique = True)
    password = Column('password', String)
    status = Column('status', String)

class Course (Base):
    __tablename__ = "courses"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    title = Column('title', String)
    owner_id = Column('owner_id', Integer, ForeignKey(User.id))
    students = Column('students', ARRAY(Integer))

class Zapit (Base):
    __tablename__ = "zapitu"

    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey(User.id))
    id_course= Column('id_course', Integer, ForeignKey(Course.id))