from flask import Blueprint, render_template
from models.enrollment import Enrollment
from models.school import School,SchoolForm
from utils.db import db
from flask import Blueprint, redirect, render_template, flash, url_for

SchoolRoute =  Blueprint("school",__name__,url_prefix="/school")

@SchoolRoute.route('/',methods=['GET'])
def index():
    schools = School.query.order_by(School.id)
    return render_template('school/index.html',schools = schools)

@SchoolRoute.route('/insert',methods=['POST'])
def insert():
    form = SchoolForm()
    if form.validate_on_submit():
        school = School.query.filter_by(codigo=form.codigo.data).first()
        if school is None:
            school = School(name = form.name.data, codigo = form.codigo.data,duration = form.duration.data)
            db.session.add(school)
            db.session.commit()
            flash("Escuela registrada con exito")
        else: flash(f"La escuela con codigo {school.codigo} ya existe")
    return redirect(url_for('school.index'))

@SchoolRoute.route('/create',methods=['GET'])
def create():
    form = SchoolForm()
    return render_template("school/create.html", form = form)

@SchoolRoute.route('/edit/<id>',methods=['GET'])
def edit(id):
    form = SchoolForm()
    school = School.query.filter_by(id = id).first()
    form.name.data = school.name;
    form.codigo.data = school.codigo;
    form.duration.data = school.duration;
    return render_template('school/edit.html', form=form , id = school.id)


@SchoolRoute.route('/update/<id>',methods=['POST'])
def update(id):
    form = SchoolForm()
    if form.validate_on_submit():
        school = School.query.filter_by(id = id).first()
        school.name = form.name.data;
        school.codigo = form.codigo.data;
        school.duration = form.duration.data;
        db.session.commit()
        flash("Se modificaron los datos de la escuela con exito")
    return redirect(url_for('school.index'))

@SchoolRoute.route('/delete/<id>',methods=['POST'])
def delete(id):
    school = School.query.filter_by(id = id).first()
    for enrollment in school.enrollments:
        db.session.delete(enrollment)
    db.session.delete(school)
    db.session.commit();
    flash(f"Se elimino a la escuela {school.name}")
    return redirect(url_for('school.index'))



