import csv
import hashlib
import json
from pathlib import Path


class AuthError(Exception):
    pass


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _users_path() -> Path:
    path = _root() / 'instance' / 'users.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text('[]', encoding='utf-8')
    return path


def _students_seed_path() -> Path:
    return _root() / 'data' / 'seed' / 'students_cse3y_s2.csv'


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _load_users() -> list:
    path = _users_path()
    return json.loads(path.read_text(encoding='utf-8') or '[]')


def _save_users(users: list) -> None:
    _users_path().write_text(json.dumps(users, indent=2), encoding='utf-8')


def _load_student_index() -> dict:
    path = _students_seed_path()
    if not path.exists():
        return {}
    with path.open(newline='', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))
    return {row['roll_no']: row for row in rows if row.get('roll_no')}


def register_user(role: str, name: str, identifier: str, password: str):
    role = (role or '').strip().lower()
    name = (name or '').strip()
    identifier = (identifier or '').strip()
    password = (password or '').strip()

    if role not in {'student', 'faculty'}:
        raise AuthError('Invalid role selected.')
    if not name:
        raise AuthError('Name is required.')
    if not identifier:
        raise AuthError('Roll number / ID is required.')
    if len(password) < 6:
        raise AuthError('Password must be at least 6 characters.')

    users = _load_users()
    if any((u.get('identifier', '').lower() == identifier.lower() and u.get('role') == role) for u in users):
        raise AuthError('Account already exists. Please login.')

    section_code = ''
    semester = ''

    if role == 'student':
        student_index = _load_student_index()
        student_row = student_index.get(identifier)
        if not student_row:
            raise AuthError('Roll number is not in approved section list.')
        section_code = student_row.get('section_code', '')
        semester = student_row.get('semester', '')

    user = {
        'role': role,
        'name': name,
        'identifier': identifier,
        'password_hash': _hash_password(password),
        'section_code': section_code,
        'semester': semester,
    }
    users.append(user)
    _save_users(users)
    return user


def authenticate(role: str, identifier: str, password: str):
    role = (role or '').strip().lower()
    identifier = (identifier or '').strip()
    password = (password or '').strip()

    users = _load_users()
    hashed = _hash_password(password)
    for user in users:
        if (
            user.get('role') == role
            and user.get('identifier', '').lower() == identifier.lower()
            and user.get('password_hash') == hashed
        ):
            return user
    raise AuthError('Invalid credentials. Please check role, ID, and password.')
