from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.routes.student_routes import students_bp
from app.routes.teacher_routes import teachers_bp
from app.routes.discipline_routes import disciplines_bp
from app.routes.room_routes import rooms_bp
from app.routes.year_routes import years_bp
from app.routes.group_routes import groups_bp
from app.routes.class_session_routes import class_session_bp
from app.extension import db 


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'xxxxxxxxxxxxxxxxxxxx'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(disciplines_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(years_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(class_session_bp)
    
    with app.app_context():
        from app.models import Student, Teacher, Discipline, Room, TimeSlot, ClassSession, Group, Year, DisciplineTeacher
        db.create_all()

    return app

