from flask import Flask, redirect

from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.faculty import faculty_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.get("/")
    def home():
        return redirect("/auth/login")

    return app
