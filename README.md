# Smart Academic Management & Notification System

Mobile-first academic platform for students, faculty, and admin.

## Tech Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Flask (Python)
- Database: SQLite (default), MySQL (optional)
- Charts: Chart.js
- Mobile: Progressive Web App (PWA)

## Quick Start
1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy env: `cp .env.example .env`
4. Run app: `python run.py`

## Project Structure
- `app/models/`: ORM entities (Users, Students, Faculty, Timetable, Attendance, Exams, Events, Notifications)
- `app/routes/`: role-based and feature routes
- `app/services/`: business logic
- `app/templates/`: Jinja templates
- `app/static/`: CSS/JS/PWA assets
- `tests/`: test modules
- `docs/uml/`: OOSE diagrams
- `.vscode/`: editor and debug configuration
