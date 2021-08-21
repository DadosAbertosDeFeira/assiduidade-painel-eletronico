import re
from pprint import pprint

import fitz


def from_xps_to_text(filepath):
    doc = fitz.open(filepath)
    return "".join(page.get_text("text") for page in doc)


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
    attendance = {}
    if not (lines[0].endswith("___") and lines[-1].endswith("___")):
        return attendance
    lines.pop(0)
    lines.pop()

    key = "attending"
    attendance[key] = []
    for line in lines:
        if "Nome Parlamentar" in line:
            continue
        elif "Ausências" in line:
            key = "absent"
            attendance[key] = []
            continue
        elif "Justificados" in line:
            key = "justified"
            attendance[key] = []
            continue
        elif "Totalização" in line:
            key = "report_from_text"
            continue

        if key != "report_from_text":
            info = {}
            elements = line.split()
            elements.pop(0)  # remove código
            if key == "justified":
                info["text"] = elements.pop()
            info["party"] = elements.pop()
            info["name"] = " ".join(elements)
            attendance[key].append(info)
        else:
            matches = re.findall(r'(\w+)\s:\s(\d+)', line.strip())
            attendance[key] = {
                "attending": matches[0][1],
                "absent": matches[1][1],
                "justified": matches[2][1],
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
        "report_generated_by": lines[-3].strip(),
        "report_generated_at": lines[-2].strip()
    }
    return attendance


if __name__ == "__main__":
    raw_text = from_xps_to_text("data/example-2021-1ª SESSÃO ORDINÁRIA.xps")
    attendance = parse_attendance_report(raw_text)
    pprint(attendance)
