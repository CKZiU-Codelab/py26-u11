# Project – CV Page

**Individual Project Brief – Week 6 · u11**

Start: Monday, 16 November 2026. Show the working page on Monday, 23 November 2026.

## The Idea

You build a program that writes your CV. The data lives in `cv.csv` — a section, a label and a value in every row — and the program turns that file into two documents: a plain text version with aligned columns, and a real HTML page with a heading, sections and a list, styled with the CSS you write yourself.

This is the honest version of "making a website": the content is data, the page is generated from the data, and the same source produces two outputs. When your skills change, you edit one line in the CSV file and both documents change with it.

## Why This Project Is Yours

You use Autodesk, you are interested in how things are made, and you said you want to learn to build pages and to have a CV that works. This project is exactly that, and it does not need a framework, a server or a fast computer — a text file, a browser and the terminal are enough. You also asked about philosophy and metaphysics: a CV is a small exercise in the same discipline, because every line must be true and every claim must be defensible.

## What You Already Have

- Python variables, strings, lists, `for` loops and conditions from the first weeks.
- `%s` formatting and `len()`.
- Reading files line by line, `strip()`, `split(",")`, and writing files inside `with`.
- Terminal work and `git` from the Linux weeks.

## The New Thing

HTML is text, and that is the whole discovery of this week. Find out how to:

1. Which characters in a text break an HTML page, and what `html.escape()` does with `&` and `<`.
2. Where `<!DOCTYPE html>`, `<head>`, `<style>` and `<body>` go, and what each one is responsible for.
3. Which element belongs to a section heading, a paragraph and a list item.
4. How CSS finds an element by tag, by class and by id, and which of the three you want here.
5. Why the page must be written with `encoding="utf-8"`, and what a Polish browser shows without it.
6. How to open a local HTML file in a browser, and what `file://` means in the address bar.

**Write it down:** Create `notes.md` with `## The New Thing – HTML is text`. Write four sentences: what a tag is, what an attribute is, which two characters must be escaped, and why the encoding matters for Polish letters. Then add one line of HTML you wrote from memory and one sentence about what the browser did with it.

## The Plan

### Milestone 1 – The data

Create `cv.csv` by hand.

1. Three columns: `section,label,value`.
2. Sections: `header`, `education`, `skills`, `projects`, `contact`.
3. At least twelve rows. In `header` put your name and your class; in `skills` put one skill per row.
4. Leave one value empty on purpose, so that the validator has something to find.

### Milestone 2 – Read and check

Create `make_cv.py`.

1. Read the file with the `csv` module and print every row with its line number.
2. Reject a row with a missing value, an unknown section or more than three columns.
3. Print a numbered list of problems and count the valid rows.
4. Write the problems to `cv_check.txt`, one per line.

At the end of this step the program reports exactly one problem and eleven or twelve valid rows.

### Milestone 3 – The text version

1. Group the rows by section, keeping the order of the file.
2. Write `cv.txt` with the name at the top, a line under it, and one block per section.
3. Align the labels with a field width, and print the value after the label.
4. Print the same text on the screen.

At the end of this step `cv.txt` is a CV you could send as an attachment, without HTML at all.

### Milestone 4 – The HTML version

1. Write `cv.html` with the mandatory skeleton and the title in `<title>`.
2. Write one section for every section of the CSV, with an `<h2>` heading and a `<ul>` list.
3. Put the name in an `<h1>` and a short line about you in a `<p>`.
4. Pass every value through `html.escape()` before it reaches the file, and test with a value containing `&` and `<`.
5. Open the file in a browser and compare it with `cv.txt` — same content, different clothes.

### Milestone 5 – The stylesheet

1. Move the styles into a `<style>` block at the top of the file, not into the tags.
2. Set a readable font size, a maximum width, a colour for headings and a border between sections.
3. Use one class for a label and one for a value, and style them from the class, not from the tag.
4. Check the page after every change and keep only what you would show to an employer.

### Milestone 6 – One command, two files

1. Make one run produce both `cv.txt` and `cv.html` and print the number of sections and rows written.
2. Add a rule: if a section is empty, it does not appear in either file.
3. Read `cv.html` back and count the `<li>` elements; compare the count with the number of valid skill rows.
4. Print the length of the file and one sentence about what a browser needs in order to display it.

## Example

```text
Reading cv.csv
 1  header     name       Jan Kowalski          OK
 2  header     class      3a                      OK
 3  education  school     CKZiU Zbąszynek         OK
 4  skills     cad        Autodesk Fusion 360     OK
 5  skills     printing   3D printing, FDM        OK
 6  projects   chess      Chess openings notebook OK
 7  contact    email                              invalid: empty value
 ...

12 valid rows, 1 problem

cv.html
<section>
  <h2>Skills</h2>
  <ul>
    <li><span class="label">cad</span> Autodesk Fusion 360</li>
  </ul>
</section>

Saved cv.txt (18 lines)
Saved cv.html (64 lines, 9 list items)
```

## Requirements

- One program, `make_cv.py`, started from the terminal with `python3 make_cv.py`.
- Both files are generated from `cv.csv`; no name, school or skill is typed into the HTML code.
- Every value passes through `html.escape()` before it is written.
- The page has the full skeleton, a `<style>` block, one `<h1>` and one `<h2>` per section.
- An empty section is left out of both outputs.
- Both files are written with `encoding="utf-8"`.
- Invalid rows are reported in `cv_check.txt` with their line numbers and never appear in the page.

## Files

```text
cv_page/
├── cv.csv
├── make_cv.py
├── cv.txt
├── cv.html
├── cv_check.txt
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- The number of list items in `cv.html` equals the number of valid rows in `cv.csv`.
- The content of `cv.txt` and `cv.html` is the same; only the markup differs.
- A value with `&` and `<` appears correctly in the browser instead of breaking the page.
- Polish letters display correctly in the browser.
- An empty section disappears from both files when its rows are removed.
- You can explain what `html.escape()` protects you from.

**Hint:** Build the page as a list of lines and write the list at the end, or write the file in one `with` block and append line after line. Do not try to build one giant string with `%` — a missing `%s` in a long template is the hardest bug to find in this project.

**Additional challenge:** Add a second stylesheet for print, with `@media print`, so that the page prints as a one-page CV, and add a command that opens the page in the browser after generating it. Then generate a third output, `cv.md`, in Markdown, and say in `notes.md` which of the three formats you would send to an employer.

## Suggested Learning Resources

- [The `html` module – escaping text](https://docs.python.org/3/library/html.html)
- [The `csv` module – reading and writing tabular data](https://docs.python.org/3/library/csv.html)
- [MDN – HTML basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics)
- [MDN – CSS first steps](https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps)

**Final goal:** By the end of this project, you should have a program that turns a data file into a plain text document and a styled HTML page, validates the data before it is published, and escapes what a browser must not interpret — using loops, conditions, lists and files from the first five weeks.
