from flask import Blueprint

admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/dashboard")
def dashboard():
    return {"route": "admin/dashboard"}
