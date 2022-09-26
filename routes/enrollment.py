from flask import Blueprint, flash, redirect, render_template, url_for
from models.course import Course
from models.enrollment import Enrollment, EnrollmentForm
from models.school import School
from models.student import Student
from utils.db import db

EnrollmentRoute =  Blueprint("enrollment",__name__,url_prefix="/enrollment")

@EnrollmentRoute.route('/',methods=['GET'])
def index():
    enrollments = Enrollment.query.order_by(Enrollment.id)
    form = EnrollmentForm()
    form.school_group.choices = list(map(lambda tupla:tupla[0],School.query.with_entities(School.name)))
    form.course_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Course.name)))
    form.dni_student_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Student.dni)))
    listOfEnrollment = []
    for enrollment in enrollments:
        school = School.query.filter_by(id = enrollment.school_id).first()
        course = Course.query.filter_by(id = enrollment.course_id).first()
        student = Student.query.filter_by(id = enrollment.student_id).first()
        listOfEnrollment.append({'school': school.name,'course': course.name,'student': student.surname + " " + student.name,'id': enrollment.id})
    return render_template('enrollment/index.html', enrollments = listOfEnrollment,form = form)

@EnrollmentRoute.route('/create',methods=['GET'])
def create():
    form = EnrollmentForm()
    form.school_group.choices = list(map(lambda tupla:tupla[0],School.query.with_entities(School.name)))
    form.course_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Course.name)))
    form.dni_student_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Student.dni)))
    return render_template('enrollment/create.html',form = form)


@EnrollmentRoute.route('/insert',methods=['POST'])
def insert():
    form = EnrollmentForm()
    course =  Course.query.filter_by(name = form.course_group.data).first()
    course_id = course.id
    school_id = School.query.filter_by(name = form.school_group.data).first().id
    student = Student.query.filter_by(dni = form.dni_student_group.data).first()
    student_id = student.id
    db.session.add(Enrollment(course_id = course_id,school_id = school_id, student_id = student_id))
    db.session.commit();
    flash(f"Alumno {student.name + ' ' + student.surname } se matriculo en el curso de {course.name} con exito.")
    form.school_group.choices = list(map(lambda tupla:tupla[0],School.query.with_entities(School.name)))
    form.course_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Course.name)))
    form.dni_student_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Student.dni)))
    return render_template('enrollment/create.html',form = form) 

@EnrollmentRoute.route('/delete<id>',methods=['POST'])
def delete(id):
    enrollment = Enrollment.query.filter_by(id = id).first()
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('enrollment.index'))

@EnrollmentRoute.route('/search',methods=['POST'])
def search():
    form = EnrollmentForm()
    form.school_group.choices = list(map(lambda tupla:tupla[0],School.query.with_entities(School.name)))
    form.course_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Course.name)))
    form.dni_student_group.choices = list(map(lambda tupla:tupla[0],Course.query.with_entities(Student.dni)))
    form.dni_student_group.choices.append("TODOS")
    school_id = School.query.filter_by(name = form.school_group.data).first().id
    course_id = Course.query.filter_by(name = form.course_group.data).first().id
    if form.dni_student_group.data == 'TODOS':
        enrollments = Enrollment.query.filter_by(school_id = school_id,course_id = course_id).all()
    else:
        student_id = Student.query.filter_by(dni = form.dni_student_group.data).first().id
        enrollments = Enrollment.query.filter_by(school_id = school_id,course_id = course_id,student_id = student_id).all()
    listOfEnrollment = []
    for enrollment in enrollments:
        school = School.query.filter_by(id = enrollment.school_id).first()
        course = Course.query.filter_by(id = enrollment.course_id).first()
        student = Student.query.filter_by(id = enrollment.student_id).first()
        listOfEnrollment.append({'school': school.name,'course': course.name,'student': student.surname + " " + student.name,'id': enrollment.id})
    return render_template('enrollment/index.html', enrollments = listOfEnrollment,form = form)


