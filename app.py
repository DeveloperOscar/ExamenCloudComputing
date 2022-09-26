from flask import Flask

from routes.enrollment import EnrollmentRoute

def create_app():
    app = Flask(__name__)
    #app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root@127.0.0.1/ExamenDB"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://oscar:Mysql123#@54.89.251.68/ExamenDB"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    from routes.student import StudentRoute
    from routes.school import SchoolRoute
    from routes.course import CourseRoute
    app.register_blueprint(StudentRoute)
    app.register_blueprint(SchoolRoute)
    app.register_blueprint(CourseRoute)
    app.register_blueprint(EnrollmentRoute)
    from utils.db import db
    db.init_app(app)
    return app
