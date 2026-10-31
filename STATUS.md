# STATUS

Healthcare Admin Form Auditor CLI — Asdale Dynamics, LLC

## What was built

A local-first, education-only Python CLI that audits healthcare administrative
forms against form templates for:

* missing required fields
* deadline dates (met / approaching / overdue / no deadline / invalid date)
  with a 7-day "approaching" window
* completeness percentage (share of defined fields filled in)

Components:

* `src/form_auditor/auditor.py` — core audit logic
* `src/form_auditor/storage.py` — local JSON storage (templates, submissions, audits)
* `src/form_auditor/export.py` — CSV export of audits
* `src/form_auditor/report.py` — printable plain-text audit report
* `src/form_auditor/cli.py` — argparse CLI: `init`, `check`, `list`, `export`, `report`
* `src/form_auditor/disclaimer.py` — education-only disclaimer printed once per run
* `src/form_auditor/models.py` — data models (templates, submissions, audits, issues)
* `tests/` — 16 tests covering field logic, storage round-trips, and CSV export
* `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
* `README.md` — beginner-friendly usage docs crediting Asdale Dynamics, LLC
* `STATUS.md` — this file

Git initialized locally with two plain-message commits. No remote, no push, no
GitHub workflows, no secrets, no API keys, no personal data.

## How to run

```bash
cd healthcare-admin-form-auditor-cli
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create sample data:

```bash
form-auditor init
```

Audit a submission JSON file:

```bash
form-auditor check path/to/submission.json --out audit-report.txt
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
form-auditor report <audit-id>
```

Run tests:

```bash
pytest
```

Data stays in the local `data/` directory (configurable with `--data-dir`).
Nothing leaves the machine.

## Verification results

* `pip install -e .` succeeds; `form-auditor` console script installed.
* `form-auditor init`, `check`, `list`, `export`, `report` all ran successfully
  against sample data in a temp directory; CSV output and report file verified.
* Education-only disclaimer prints exactly once per run (no duplication).
* `pytest`: 16 passed, 0 failed, no deprecation warnings.
* No `datetime.utcnow()` references remain in source (timezone-aware UTC used).
* LICENSE copyright line verified exactly:
  `Copyright (c) 2026 Asdale Dynamics, LLC`
* README credits Asdale Dynamics, LLC and is written in a warm, beginner-friendly,
  step-by-step tone.

## Known gaps

* Deadline "approaching" window is hard-coded at 7 days (no CLI flag yet).
* Completeness counts all defined fields; there is no required-only completeness mode.
* No config file; data directory passed via `--data-dir` on every call.
* Reports are plain text only (no HTML/PDF).
* No authentication or encryption — files are local; protect the data directory per
  facility policy. Do not enter real patient identifiers unless your policies permit it.
* Python 3.9+ targeted; developed and tested on Python 3.13.
