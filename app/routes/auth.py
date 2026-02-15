from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthError, authenticate, register_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.get('/login')
def login_page():
    return render_template('auth/login.html')


@auth_bp.post('/register')
def register():
    role = request.form.get('role', 'student')
    name = request.form.get('name', '')
    identifier = request.form.get('identifier', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if password != confirm_password:
        flash('Password and confirm password do not match.', 'error')
        return redirect(url_for('auth.login_page'))

    try:
        user = register_user(role=role, name=name, identifier=identifier, password=password)
    except AuthError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('auth.login_page'))

    session['user'] = {
        'role': user.get('role'),
        'name': user.get('name'),
        'identifier': user.get('identifier'),
        'section_code': user.get('section_code', ''),
        'semester': user.get('semester', ''),
    }

    if user.get('role') == 'student':
        flash(f"Account created for {user.get('identifier')}.", 'success')
        return redirect(url_for('student.dashboard', section=user.get('section_code', '')))

    flash('Faculty account created successfully.', 'success')
    return redirect(url_for('faculty.dashboard'))


@auth_bp.post('/signin')
def signin():
    role = request.form.get('role', 'student')
    identifier = request.form.get('identifier', '')
    password = request.form.get('password', '')

    try:
        user = authenticate(role=role, identifier=identifier, password=password)
    except AuthError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('auth.login_page'))

    session['user'] = {
        'role': user.get('role'),
        'name': user.get('name'),
        'identifier': user.get('identifier'),
        'section_code': user.get('section_code', ''),
        'semester': user.get('semester', ''),
    }

    if user.get('role') == 'student':
        return redirect(url_for('student.dashboard', section=user.get('section_code', '')))
    return redirect(url_for('faculty.dashboard'))


@auth_bp.get('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login_page'))
