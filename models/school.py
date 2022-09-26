from flask_wtf import FlaskForm
from wtforms import  IntegerField, StringField
from wtforms.validators import DataRequired
from utils.db import db

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('Enrollment',backref='school',lazy=True)

class SchoolForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired()])
    name = StringField("Nombre", validators=[DataRequired()])
    duration = IntegerField("Duratión (años)", validators=[DataRequired()])
