#!/usr/bin/env python3
"""Self-check for the project "CV Page" (u11).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



def cv_rows():
    rows = read_csv("cv.csv")
    header = [cell.strip().lower() for cell in rows[0]]
    if header != ["section", "label", "value"]:
        raise Fail("cv.csv header is %s; expected section,label,value" % ",".join(header))
    if len(rows) - 1 < 12:
        raise Fail("cv.csv has %d data rows; at least twelve were asked for" % (len(rows) - 1))
    data = []
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != 3:
            raise Fail("line %d has %d cells, three expected" % (number, len(row)))
        data.append((number, row[0].strip(), row[1].strip(), row[2].strip()))
    return data


@check("the files named in the brief exist")
def files():
    require_files("cv.csv", "make_cv.py", "cv.txt", "cv.html", "cv_check.txt", "notes.md")


@check("cv.csv has the three columns and at least twelve rows")
def cv():
    cv_rows()


@check("cv.html has the skeleton, the styles and every value from cv.csv")
def page():
    rows = cv_rows()
    text = read_text("cv.html")
    low = text.lower()
    for token in ("<!doctype html", "<style", "<h1", "<h2", "<li"):
        if token not in low:
            raise Fail("cv.html has no %s" % token)
    missing = []
    for number, section, label, value in rows:
        if not value:
            continue
        if value not in text and html_lib.escape(value) not in text:
            missing.append(value)
    if missing:
        raise Fail("these values from cv.csv are not in cv.html: %s"
                   % ", ".join(missing[:4]))


@check("cv.txt has every value from cv.csv")
def plain():
    rows = cv_rows()
    text = read_text("cv.txt")
    missing = []
    for number, section, label, value in rows:
        if value and value not in text:
            missing.append(value)
    if missing:
        raise Fail("these values from cv.csv are not in cv.txt: %s"
                   % ", ".join(missing[:4]))


@check("cv_check.txt names the line of every empty value")
def validation():
    rows = cv_rows()
    text = read_text("cv_check.txt")
    problems = [number for number, section, label, value in rows if not value]
    for number in problems:
        if str(number) not in text and str(number - 1) not in text:
            raise Fail("cv_check.txt does not name line %d, where a value is empty" % number)
    if not problems:
        warn("cv.csv has no empty value, so the validator was never tested. "
             "Remove one value, run the program again, and check that cv_check.txt "
             "names that line.")


@check("notes.md has the research note")
def notes():
    require_notes("## The New Thing – HTML is text")


def check_escaping_sample():
    try:
        rows = cv_rows()
    except Fail:
        return
    for number, section, label, value in rows:
        if "&" in value or "<" in value:
            return
    warn("no value in cv.csv contains & or <, so the page never tests escaping. "
         "Add such a value and open the page again.")


check_escaping_sample()

if __name__ == "__main__":
    sys.exit(main())
