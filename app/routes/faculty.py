from flask import Blueprint

faculty_bp = Blueprint("faculty", __name__)


@faculty_bp.get("/dashboard")
def dashboard():
    return {"route": "faculty/dashboard"}
