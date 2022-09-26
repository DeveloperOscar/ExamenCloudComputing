from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from utils.db import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('Enrollment',backref='course',lazy=True)


class CourseForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired()])
    name = StringField("Curso", validators=[DataRequired()])
    credits = StringField("Creditos", validators=[DataRequired()])
