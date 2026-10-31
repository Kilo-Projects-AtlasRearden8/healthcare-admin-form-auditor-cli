# Healthcare Admin Form Auditor CLI

A small, local-first Python CLI that helps you check healthcare administrative
forms for missing required fields, deadline dates, and overall completeness.

It stores everything in local JSON files, can export your results to CSV, and
prints a plain-text audit report you can read or print.

Built by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana) as an education-only
accessibility tool for healthcare paperwork organization.

## Important: education only — not medical advice

This tool is for educational and administrative organization purposes only.

It is **not medical advice**, not a diagnosis or treatment tool, and not a
substitute for professional medical judgment. Always follow your facility's
policies, applicable law (such as HIPAA in the United States), and the guidance
of a qualified healthcare administrator, compliance officer, or attorney when
handling healthcare paperwork.

By using this tool you acknowledge that Asdale Dynamics, LLC provides it "as
is" for education only, with no warranties of any kind.

## Local-first — your data stays on your machine

Everything this tool does happens on your own computer:

* Form templates, submissions, and audits are saved as JSON files in a local
  data directory (default: `data/`).
* Nothing is sent over the network. No cloud accounts, no API keys, no
  telemetry, no third-party services.
* You own and control all of the data.

Please do not enter real patient identifiers or protected health information
unless your facility's policies permit it and you are managing the file
securely.

## What it checks

For each form submission, the auditor looks at:

* **Missing required fields** — fields your form template marks as required
  that are blank or not provided.
* **Deadline dates** — whether a deadline is met, approaching (within 7 days),
  overdue, missing, or not a valid date.
* **Completeness** — a percentage showing how many of the defined fields on the
  form have been filled in.

## Features

* Checks for missing required fields on a form template
* Checks deadline dates (met / approaching / overdue / no deadline / invalid)
* Computes a completeness percentage
* Local JSON storage for templates, submissions, and audit results
* CSV export of all audits
* Printable plain-text audit report
* Education-only disclaimer shown on every run

## Install

You'll need Python 3.9 or newer.

```bash
cd healthcare-admin-form-auditor-cli
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

This installs the `form-auditor` command so you can run it from anywhere.

## Usage, step by step

### 1. Create sample data

If you just want to see how the tool works, create some sample forms and a
sample submission:

```bash
form-auditor init
```

This makes a `data/` folder with one form template ("Patient Intake Form"),
one example submission, and one example audit result.

### 2. Audit a submission

A submission is a JSON file describing a filled-in form. Here's an example:

```json
{
  "submission_id": "SUB-1",
  "form_id": "patient-intake-001",
  "form_name": "Patient Intake Form",
  "deadline": "2026-12-01",
  "values": {
    "patient_reference": "PAT-9",
    "date_of_birth": "1975-03-04",
    "insurance_provider": "Blue Cross",
    "insurance_member_id": "X99",
    "emergency_contact_name": "J. Doe",
    "emergency_contact_phone": "555-0100",
    "allergies": "none"
  },
  "submitted_by": "clerk-example"
}
```

Save that to a file (for example `submission.json`), then run:

```bash
form-auditor check submission.json
```

The tool prints the education-only disclaimer, then a readable audit report
telling you what's missing, what the deadline status is, and the completeness
score.

To save the report to a file as well:

```bash
form-auditor check submission.json --out audit-report.txt
```

### 3. List your audits

See every audit you've run so far:

```bash
form-auditor list
```

### 4. Export to CSV

Save all audits to a CSV file you can open in a spreadsheet:

```bash
form-auditor export audits.csv
```

### 5. Reprint a past report

```bash
form-auditor report <audit-id>
```

Replace `<audit-id>` with an ID from `form-auditor list`.

### Data format notes

* `deadline` is optional. When included, use ISO format: `YYYY-MM-DD`.
* Empty strings count as missing required fields.
* A value of `0` or `false` counts as filled in (it's a deliberate answer).

## Run the tests

```bash
pytest
```

Tests cover missing required fields, empty optional fields, deadline
classification, and completeness scoring.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created and maintained by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana,
formed October 2026). Asdale Dynamics publishes beginner-friendly AI education,
open-source tools, and small-business / life-admin helpers. More at
dylanasdale.github.io and in *The Massive AI Manual*.

## About the author

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC. He explains things "like a friend would": plain English, step by
step, never condescending. The LLC's focus includes healthcare-worker AI aids
(education only, never medical advice), accessible life-admin helpers, and
practical open-source tools.
