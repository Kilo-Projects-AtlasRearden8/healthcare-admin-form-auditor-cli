# Healthcare Admin Form Auditor CLI

A small, local-first Python CLI that checks healthcare administrative forms for
missing required fields, deadline dates, and overall completeness. Stores data
in local JSON files, exports to CSV, and prints a plain-text audit report.

Built by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana) as an education-only
accessibility tool for healthcare paperwork organization.

## Education-only - not medical advice

This tool is for educational and administrative organization purposes only.

It is **not medical advice**, not a diagnosis or treatment tool, and not a
substitute for professional medical judgment, your facility's policies, or
review by a qualified healthcare administrator, compliance officer, or
attorney. Always follow applicable law (such as HIPAA in the United States)
and your organization's procedures when handling healthcare paperwork.

## Local-first

Everything stays on your machine:

* Form templates, submissions, and audits are stored as JSON files in a local
  data directory (default: `data/`).
* Nothing is sent over the network. No cloud accounts, no API keys, no
  telemetry.
* You own and control all of the data.

Do not enter real patient identifiers or protected health information unless
your facility's policies permit it and you are managing the file securely.

## Features

* Checks for **missing required fields** on a form template
* Checks **deadline dates** (met / approaching / overdue / no deadline)
* Computes a **completeness percentage** (share of defined fields filled in)
* Local **JSON storage** for templates, submissions, and audit results
* **CSV export** of all audits
* Printable **plain-text audit report**
* Education-only disclaimer shown on every run

## Install

```bash
cd healthcare-admin-form-auditor-cli
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

Initialize sample data:

```bash
form-auditor init
```

Audit a submission (JSON file) against a stored template:

```bash
form-auditor check submissions/patient-intake-example.json
```

List stored audits:

```bash
form-auditor list
```

Export all audits to CSV:

```bash
form-auditor export audits.csv
```

Print a stored audit report:

```bash
form-auditor report AUD-...
```

Save a report to a file:

```bash
form-auditor check submissions/x.json --out report.txt
```

### Data file example (submission)

```json
{
  "submission_id": "SUB-1700000000",
  "form_id": "patient-intake-001",
  "form_name": "Patient Intake Form",
  "deadline": "2026-11-15",
  "values": {
    "patient_reference": "PAT-EXAMPLE",
    "date_of_birth": "1980-05-12",
    "insurance_provider": "Example Health",
    "insurance_member_id": "M123456",
    "emergency_contact_name": "",
    "emergency_contact_phone": ""
  },
  "submitted_by": "clerk-example"
}
```

`deadline` is optional and uses ISO format (`YYYY-MM-DD`). Empty strings count
as missing required fields.

## Tests

```bash
pytest
```

Tests cover field logic: missing required fields, empty optional fields,
deadline classification, and completeness scoring.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created and maintained by **Asdale Dynamics, LLC** (Dylan Asdale, Indiana,
formed October 2026). Asdale Dynamics publishes beginner-friendly AI education,
open-source tools, and small-business / life-admin helpers. More at
dylanasdale.github.io and in *The Massive AI Manual*.

## About the author

Dylan Asdale is a registered nurse turned AI author and founder of Asdale
Dynamics, LLC. He explains AI "like a friend would": plain English, step by
step, never condescending. The LLC's focus includes healthcare-worker AI aids
(education only, never medical advice), accessible life-admin helpers, and
practical open-source tools.
