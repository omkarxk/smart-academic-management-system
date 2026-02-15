from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.timetable_service import DAY_LABELS, DAY_ORDER
from app.services.timetable_service import get_section_summary, get_sections
from app.services.timetable_service import get_section_faculty, get_week_matrix

student_bp = Blueprint('student', __name__)


@student_bp.get('/dashboard')
def dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'student':
        return redirect(url_for('auth.login_page'))

    sections = get_sections()
    preferred_section = user.get('section_code')
    selected_section = request.args.get('section') or preferred_section or (sections[0]['section_code'] if sections else '')

    summary = get_section_summary(selected_section)
    faculty_rows = get_section_faculty(selected_section)
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
        'student/dashboard.html',
        role='Student',
        sections=sections,
        selected_section=selected_section,
        summary=summary,
        faculty_rows=faculty_rows,
        week_matrix=week_matrix,
        day_order=DAY_ORDER,
        day_labels=DAY_LABELS,
        period_labels=period_labels,
        user=user,
    )
