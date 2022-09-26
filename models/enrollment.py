from flask_wtf import FlaskForm
from wtforms import SelectField
from utils.db import db

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable=False)
    school_id = db.Column(db.Integer,db.ForeignKey('school.id'),nullable=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)

class EnrollmentForm(FlaskForm):
    dni_student_group = SelectField(u'DNI ESTUDIANTE',coerce=str)
    school_group = SelectField(u'ESCUELA',coerce=str)
    course_group = SelectField(u'CURSO',coerce=str)

