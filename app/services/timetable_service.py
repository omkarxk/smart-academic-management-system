import csv
from pathlib import Path
from typing import Optional

DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
DAY_LABELS = {
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
    "SAT": "Saturday",
}


def _seed_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "seed"


def _read_csv(filename: str):
    path = _seed_dir() / filename
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_sections():
    rows = _read_csv("sections.csv")
    return sorted(rows, key=lambda row: row.get("section_code", ""))


def get_section(section_code: str) -> Optional[dict]:
    for section in get_sections():
        if section.get("section_code") == section_code:
            return section
    return None


def get_subject_map():
    rows = _read_csv("subjects.csv")
    return {row["subject_code"]: row for row in rows if row.get("subject_code")}


def get_section_faculty(section_code: str):
    subjects = get_subject_map()
    rows = [
        row
        for row in _read_csv("section_subject_faculty.csv")
        if row.get("section_code") == section_code
    ]
    for row in rows:
        subject = subjects.get(row.get("subject_code", ""), {})
        row["subject_short"] = subject.get("subject_short", row.get("subject_code", ""))
        row["subject_name"] = subject.get("subject_name", row.get("subject_code", ""))
    return rows


def get_section_timetable(section_code: str):
    rows = [
        row
        for row in _read_csv("timetable_3rd_year_cse.csv")
        if row.get("section_code") == section_code
    ]

    def sort_key(row: dict) -> tuple[int, int]:
        day = row.get("day", "")
        day_idx = DAY_ORDER.index(day) if day in DAY_ORDER else 99
        period_no = int(row.get("period_no", "0") or 0)
        return day_idx, period_no

    rows.sort(key=sort_key)
    return rows


def get_week_matrix(section_code: str):
    rows = get_section_timetable(section_code)
    matrix = {day: {} for day in DAY_ORDER}
    for row in rows:
        day = row.get("day", "")
        period = int(row.get("period_no", "0") or 0)
        if day in matrix and period:
            matrix[day][period] = row
    return matrix


def get_section_summary(section_code: str):
    section = get_section(section_code) or {}
    faculty_rows = get_section_faculty(section_code)
    timetable_rows = get_section_timetable(section_code)

    unique_faculty = sorted(
        {row.get("faculty_name", "") for row in faculty_rows if row.get("faculty_name")}
    )
    unique_subject_codes = sorted(
        {
            code
            for row in timetable_rows
            for code in (row.get("subject_codes", "").split("|") if row.get("subject_codes") else [])
            if code and not code.startswith("ACT_")
        }
    )

    return {
        "section": section,
        "faculty_count": len(unique_faculty),
        "subject_count": len(unique_subject_codes),
        "slot_count": len(timetable_rows),
    }


def get_faculty_view(section_code: str, faculty_name: Optional[str] = None):
    faculty_rows = get_section_faculty(section_code)
    names = sorted({row.get("faculty_name", "") for row in faculty_rows if row.get("faculty_name")})
    selected_name = faculty_name if faculty_name in names else (names[0] if names else "")

    assigned_rows = [row for row in faculty_rows if row.get("faculty_name") == selected_name]
    assigned_codes = {row.get("subject_code", "") for row in assigned_rows}

    slots = []
    for row in get_section_timetable(section_code):
        codes = set((row.get("subject_codes", "").split("|") if row.get("subject_codes") else []))
        if assigned_codes.intersection(codes):
            slots.append(row)

    return {
        "faculty_names": names,
        "selected_name": selected_name,
        "assigned_subjects": assigned_rows,
        "teaching_slots": slots,
    }
