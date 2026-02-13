from flask import Blueprint

student_bp = Blueprint("student", __name__)


@student_bp.get("/dashboard")
def dashboard():
    return {"route": "student/dashboard"}
