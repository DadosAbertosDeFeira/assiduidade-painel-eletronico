import fitz


def from_xps_to_text(filepath):
    doc = fitz.open(filepath)
    return [page.get_text("text") for page in doc]


def extract_session_and_date(line):
    session, session_date = "", ""
    # raw format: `Reunião : 1ª SESSÃO ORDINÁRIA    Dia : 01/02/2021'`,
    begin_session_date = "Dia : "
    index_begin_session_date = line.find(begin_session_date)
    if index_begin_session_date != -1:
        session_date = line[len(begin_session_date)+index_begin_session_date:]
    begin_session = "Reunião : "
    index_begin_session = line.find(begin_session)
    if index_begin_session != -1:
        session = line[len(begin_session)+index_begin_session:index_begin_session_date]
    return session.strip(), session_date.strip()


def extract_attendance(lines):
    if not (lines[0].endswith("---") and lines[-1].endswith("---")):
        return {}
    attendance = {
        "city_councils": {
            "attending": [
                {"name": "", "party": ""},
            ],
            "absent": [
                {"name": "", "party": ""},
            ],
            "justified": [
                {"name": "", "party": ""},
            ],
        },
        "report_from_text": {
            "attending": "21",
            "absent": "0",
            "justified": "0",
        }
    }
    return attendance


def parse_attendance_report(text):
    lines = text.strip().splitlines()
    session, session_date = extract_session_and_date(lines[3].strip())
    attendance = {
        "agency": lines[0].strip(),
        "report": lines[2].strip(),
        "session": session,
        "date": session_date,
        "attendance": extract_attendance(lines[4:-4]),
        "president": lines[-3].strip(),
        "report_generated_at": lines[-2].strip()
    }
    return attendance


if __name__ == "__main__":
    text = from_xps_to_text("data/2021/SESSÕES ORDINÁRIA/1ª SESSÃO ORDINÁRIA.xps")
    attendance = parse_attendance_report(text)
