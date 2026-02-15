from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.timetable_service import DAY_LABELS, DAY_ORDER
from app.services.timetable_service import get_faculty_view, get_section_summary
from app.services.timetable_service import get_sections, get_week_matrix

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.get('/dashboard')
def dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'faculty':
        return redirect(url_for('auth.login_page'))

    sections = get_sections()
    selected_section = request.args.get('section') or (sections[0]['section_code'] if sections else '')
    selected_faculty = request.args.get('faculty') or user.get('name')

    summary = get_section_summary(selected_section)
    faculty_view = get_faculty_view(selected_section, selected_faculty)
    week_matrix = get_week_matrix(selected_section)

    period_labels = {
        1: '09:00-09:50',
        2: '09:50-10:40',
        3: '10:40-11:30',
        4: '11:30-12:20',
        5: '01:30-02:20',
        6: '02:20-03:10',
        7: '03:10-04:00',
    }

    return render_template(
        'faculty/dashboard.html',
        role='Faculty',
        sections=sections,
        selected_section=selected_section,
        summary=summary,
        faculty_view=faculty_view,
        week_matrix=week_matrix,
        day_order=DAY_ORDER,
        day_labels=DAY_LABELS,
        period_labels=period_labels,
        user=user,
    )
