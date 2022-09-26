from datetime import datetime
from utils.db import db
from flask_wtf import FlaskForm
from wtforms import StringField,DateField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    dni = StringField("DNI", validators=[DataRequired()])
    name = StringField("Nombre(s)", validators=[DataRequired()])
    surname = StringField("Apellidos", validators=[DataRequired()])
    birth_date = DateField("Fecha Nacimiento", validators=[DataRequired()])
    sexo = StringField("Sexo", validators=[DataRequired()])

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(8), nullable=False, unique=True)
    surname = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(10))
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment',backref='student',lazy=True)

