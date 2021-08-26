import json
import re
from pathlib import Path

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
        session_date = line[len(begin_session_date) + index_begin_session_date :]
    begin_session = "Reunião : "
    index_begin_session = line.find(begin_session)
    if index_begin_session != -1:
        session = line[
            len(begin_session) + index_begin_session : index_begin_session_date
        ]
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
        elif "Recomposição" in line:
            key = "rearrangement"
            attendance[key] = []
            continue
        elif "Totalização" in line:
            key = "report_from_text"
            continue

        if key != "report_from_text":
            line = line.strip()
            info = {"name": line[:31].strip(), "party": line[31:42].strip(), "text": line[42:].strip()}
            if key in {"attending", "rearrangement"}:
                info["name"] = info["name"][3:]  # remove código

            attendance[key].append(info)
        else:
            matches = re.findall(r"(\w+)\s:\s(\d+)", line.strip())
            if matches:
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
        "report_generated_at": lines[-2].strip(),
    }
    return attendance


if __name__ == "__main__":
    root = "data/2021-05-01"  # ou "data/examples"
    result_folder = Path(f"{root}/results")
    result_folder.mkdir(exist_ok=True)
    write = True
    for path in Path(root).resolve().glob("**/*.xps"):
        year = path.parts[-3]
        session_type = path.parts[-2]
        title = path.parts[-1].replace(".xps", "")
        attendance = {}
        try:
            raw_text = from_xps_to_text(path)
        except Exception as e:
            print(f"Erro ao extrair texto ({e}): {path}")
        try:
            attendance = parse_attendance_report(raw_text)
        except Exception as e:
            print(f"Erro ao parsear texto ({e}): {path}")

        text_path = result_folder / year
        text_path.mkdir(parents=True, exist_ok=True)
        if write:
            (text_path / f"{session_type}-{title}.txt").write_text(raw_text)
            (text_path / f"{session_type}-{title}.json").write_text(
                json.dumps(attendance, indent=4)
            )
