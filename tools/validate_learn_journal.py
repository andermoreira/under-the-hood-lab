#!/usr/bin/env python3
"""Conservative LEARN journal checker. Never certifies actual understanding."""
import argparse
import json
import re
from pathlib import Path

DIMENSIONS = ("Prever", "Construir", "Explicar", "Refutar", "Transferir")
PLACEHOLDER = re.compile(r"<[^>]+>|\bNOT_RUN\b|\bUNVERIFIED\b", re.I)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def section(text, number):
    match = re.search(r"^## " + str(number) + r"\. .*?$", text, re.M)
    if not match:
        return ""
    end = re.search(r"^## \d+\. ", text[match.end():], re.M)
    return text[match.end():match.end() + end.start()] if end else text[match.end():]

def check(text):
    findings = []
    prediction = section(text, 3)
    observation = section(text, 4)
    if not prediction.strip() or PLACEHOLDER.search(prediction):
        findings.append("prediction_missing_or_placeholder")
    if not observation.strip() or PLACEHOLDER.search(observation) or "$ <comando>" in observation:
        findings.append("observation_missing_or_placeholder")
    if "Commit em que foi observado: <hash>" in observation:
        findings.append("observed_commit_missing")
    for number in (1, 2, 5, 6, 7, 10):
        body = section(text, number)
        if not body.strip() or PLACEHOLDER.search(body):
            findings.append(f"section_{number}_missing_or_placeholder")
    for token in ("Estudante: <nome>", "Data de início: <AAAA-MM-DD>", "Commit base: <hash"):
        if token in text:
            findings.append("identity_or_provenance_missing")
            break
    rubric = section(text, 8)
    for dimension in DIMENSIONS:
        line = next((line for line in rubric.splitlines() if re.match(r"^\|\s*" + dimension + r"\s*\|", line)), "")
        cells = [x.strip() for x in line.strip("|").split("|")]
        if len(cells) < 3 or cells[1] not in ("0", "1", "2", "3") or PLACEHOLDER.search(cells[2]):
            findings.append("rubric_incomplete_" + dimension.lower())
        elif int(cells[1]) < 2:
            findings.append("rubric_below_threshold_" + dimension.lower())
    review = section(text, 9)
    rows = [line for line in review.splitlines() if re.match(r"^\|\s*\+(1|7|30) dias?\s*\|", line)]
    if len(rows) != 3:
        findings.append("review_rows_missing")
    for line in rows:
        cells = [x.strip() for x in line.strip("|").split("|")]
        if len(cells) < 4 or not DATE.fullmatch(cells[2]) or cells[3] in ("—", "-", "") or PLACEHOLDER.search(cells[3]):
            findings.append("review_incomplete_" + cells[0].replace(" ", "_"))
    return {"status": "INCOMPLETE" if findings else "READY_FOR_HUMAN_REVIEW",
            "findings": findings,
            "note": "Static completeness only; not proof of learning, timing, authorship or execution."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("journal", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.journal.is_file():
        parser.error("journal not found")
    report = check(args.journal.read_text(encoding="utf-8"))
    result = json.dumps(report, indent=2, ensure_ascii=False)
    print(result)
    if args.output:
        args.output.write_text(result + "\n", encoding="utf-8")
    return 0 if report["status"] == "READY_FOR_HUMAN_REVIEW" else 1

if __name__ == "__main__":
    raise SystemExit(main())
