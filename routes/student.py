from flask import Blueprint, render_template
from models.enrollment import Enrollment
from models.student import Student,StudentForm
from utils.db import db
from flask import Blueprint, redirect, render_template, flash, url_for

StudentRoute =  Blueprint("student",__name__,url_prefix="/student")

@StudentRoute.route('/',methods=['GET'])
def index():
    students = Student.query.order_by(Student.data_added)
    return render_template('students/index.html',students = students)

@StudentRoute.route('/insert',methods=['POST'])
def insert():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(dni=form.dni.data).first()
        if student is None:
            student = Student(name=form.name.data, surname=form.surname.data,birth_date = form.birth_date.data, sexo = form.sexo.data,dni = form.dni.data)
            db.session.add(student)
            db.session.commit()
            flash("Estudiante añadido con exito")
        else: flash(f"El estudiante con el DNI {student.dni} ya existe")
    return redirect(url_for('student.index'))

@StudentRoute.route('/create',methods=['GET'])
def create():
    form = StudentForm()
    return render_template("students/create.html", form = form)

@StudentRoute.route('/edit/<id>',methods=['GET'])
def edit(id):
    form = StudentForm()
    student = Student.query.filter_by(id = id).first()
    form.name.data = student.name;
    form.surname.data = student.surname;
    form.birth_date.data = student.birth_date;
    form.sexo.data = student.sexo;
    form.dni.data = student.dni;
    return render_template('students/edit.html', form=form , id = student.id)


@StudentRoute.route('/update/<id>',methods=['POST'])
def update(id):
    form = StudentForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(id = id).first()
        user.name = form.name.data
        user.surname = form.surname.data
        user.dni = form.dni.data
        user.sexo = form.sexo.data
        user.birth_date = form.birth_date.data
        db.session.commit()
        flash("Se modificaron los datos del estudiante con exito")
    return redirect(url_for('student.index'))

@StudentRoute.route('/delete/<id>',methods=['POST'])
def delete(id):
    student = Student.query.filter_by(id = id).first()
    for enrollment in student.enrollments:
        db.session.delete(enrollment)
    db.session.delete(student)
    db.session.commit();
    flash(f"Se elimino al estudiante {student.name}")
    return redirect(url_for('student.index'))
