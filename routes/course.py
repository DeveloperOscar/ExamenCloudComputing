from flask import Blueprint, render_template
from models.course import Course, CourseForm
from models.enrollment import Enrollment
from utils.db import db
from flask import Blueprint, redirect, render_template, flash, url_for

CourseRoute =  Blueprint("course",__name__,url_prefix="/course")

@CourseRoute.route('/',methods=['GET'])
def index():
    courses = Course.query.order_by(Course.id)
    return render_template('courses/index.html',courses = courses)

@CourseRoute.route('/insert',methods=['POST'])
def insert():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(codigo=form.codigo.data).first()
        if course is None:
            course = Course(name = form.name.data, codigo = form.codigo.data,credits = form.credits.data)
            db.session.add(course)
            db.session.commit()
            flash("Curso registrado con exito")
        else: flash(f"El curso con codigo {course.codigo} ya existe")
    return redirect(url_for('course.index'))

@CourseRoute.route('/create',methods=['GET'])
def create():
    form = CourseForm()
    return render_template("courses/create.html", form = form)

@CourseRoute.route('/edit/<id>',methods=['GET'])
def edit(id):
    form = CourseForm()
    course = Course.query.filter_by(id = id).first()
    form.name.data = course.name;
    form.codigo.data = course.codigo;
    form.credits.data = course.credits;
    return render_template('courses/edit.html', form=form , id = course.id)


@CourseRoute.route('/update/<id>',methods=['POST'])
def update(id):
    form = CourseForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id = id).first()
        course.name = form.name.data;
        course.codigo = form.codigo.data;
        course.credits = form.credits.data;
        db.session.commit()
        flash("Se modificaron los datos del curso con exito")
    return redirect(url_for('course.index'))

@CourseRoute.route('/delete/<id>',methods=['POST'])
def delete(id):
    course = Course.query.filter_by(id = id).first()
    for enrollment in course.enrollments:
        db.session.delete(enrollment)
    db.session.delete(course)
    db.session.commit();
    flash(f"Se elimino el curso {course.name}")
    return redirect(url_for('course.index'))
