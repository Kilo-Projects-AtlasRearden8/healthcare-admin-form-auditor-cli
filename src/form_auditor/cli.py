"""Command-line interface for the healthcare admin form auditor."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .auditor import audit_submission
from .disclaimer import print_disclaimer
from .export import export_csv
from .models import (
    AuditResult,
    FieldTemplate,
    FormSubmission,
    FormTemplate,
)
from .report import build_report
from .storage import JsonStorage, DEFAULT_DIR


def _load_json(path: str | Path) -> Any:
    with Path(path).open() as fh:
        return json.load(fh)


def _save_json(data: Any, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2))


def _new_id(prefix: str) -> str:
    return f"{prefix}-{int(datetime.now(timezone.utc).timestamp())}"


def cmd_init(args: argparse.Namespace) -> int:
    storage = JsonStorage(args.data_dir)
    sample = FormTemplate(
        form_id="patient-intake-001",
        form_name="Patient Intake Form",
        fields=[
            FieldTemplate(name="patient_reference", required=True, field_type="text"),
            FieldTemplate(name="date_of_birth", required=True, field_type="date"),
            FieldTemplate(name="insurance_provider", required=True, field_type="text"),
            FieldTemplate(name="insurance_member_id", required=True, field_type="text"),
            FieldTemplate(name="emergency_contact_name", required=True, field_type="text"),
            FieldTemplate(name="emergency_contact_phone", required=True, field_type="text"),
            FieldTemplate(name="allergies", required=False, field_type="text"),
            FieldTemplate(name="current_medications", required=False, field_type="text"),
        ],
    )
    storage.save_template(sample)
    sample_sub = FormSubmission(
        submission_id=_new_id("SUB"),
        form_id=sample.form_id,
        form_name=sample.form_name,
        deadline=str(date.today()),
        values={
            "patient_reference": "PAT-EXAMPLE",
            "date_of_birth": "",
            "insurance_provider": "",
            "insurance_member_id": "M123456",
            "emergency_contact_name": "",
            "emergency_contact_phone": "",
        },
        submitted_by="clerk-example",
    )
    storage.save_submission(sample_sub)
    result = audit_submission(sample_sub, sample)
    storage.save_audit(result)
    print(f"Initialized sample data in {storage.base_dir}")
    print(f"Template: {sample.form_id} ({sample.form_name})")
    print(f"Submission: {sample_sub.submission_id}")
    print(f"Audit: {result.audit_id} (completeness {result.completeness:.2f}%)")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    storage = JsonStorage(args.data_dir)
    submission = FormSubmission.from_dict(_load_json(args.submission))
    template = storage.load_template(submission.form_id)
    if template is None:
        # Allow a template file to be supplied instead.
        if not args.template:
            print(
                f"Error: no template for form '{submission.form_id}' in storage. "
                "Use --template to supply one.",
                file=sys.stderr,
            )
            return 2
        template = FormTemplate.from_dict(_load_json(args.template))
    result = audit_submission(submission, template)
    storage.save_submission(submission)
    storage.save_audit(result)
    print(build_report(result))
    if args.out:
        Path(args.out).write_text(build_report(result))
        print(f"Report written to {args.out}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    storage = JsonStorage(args.data_dir)
    audits = storage.list_audits()
    if not audits:
        print("No audits stored yet. Run 'form-auditor check ...' first.")
        return 0
    print(f"{'AUDIT ID':<32} {'SUBMISSION':<20} {'FORM':<24} {'COMPLETE':<10} {'STATUS'}")
    print("-" * 100)
    for a in audits:
        status = "PASS" if a.passed else "ATTENTION"
        print(
            f"{a.audit_id:<32} {a.submission_id:<20} {a.form_id:<24} "
            f"{a.completeness:>6.2f}%    {status} ({a.deadline_status})"
        )
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    storage = JsonStorage(args.data_dir)
    audits = storage.list_audits()
    header = export_csv(audits, args.output)
    print(f"Exported {len(audits)} audit(s) to {args.output}")
    print("Columns: " + ", ".join(header))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    storage = JsonStorage(args.data_dir)
    result = storage.load_audit(args.audit_id)
    if result is None:
        print(f"Error: audit '{args.audit_id}' not found.", file=sys.stderr)
        return 2
    text = build_report(result)
    print(text)
    if args.out:
        Path(args.out).write_text(text)
        print(f"Report written to {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="form-auditor",
        description=(
            "Healthcare admin form auditor - education only, never medical "
            "advice, local-only JSON storage."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--data-dir",
        default=str(DEFAULT_DIR),
        help=f"Local data directory (default: {DEFAULT_DIR})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create sample form data in the data directory")
    p_init.add_argument("--data-dir", default=str(DEFAULT_DIR))
    p_init.set_defaults(func=cmd_init)

    p_check = sub.add_parser("check", help="Audit a form submission JSON file")
    p_check.add_argument("submission", help="Path to form submission JSON file")
    p_check.add_argument("--template", help="Path to form template JSON (optional if in storage)")
    p_check.add_argument("--out", help="Write printable report to this file as well")
    p_check.add_argument("--data-dir", default=str(DEFAULT_DIR))
    p_check.set_defaults(func=cmd_check)

    p_list = sub.add_parser("list", help="List stored audits")
    p_list.add_argument("--data-dir", default=str(DEFAULT_DIR))
    p_list.set_defaults(func=cmd_list)

    p_export = sub.add_parser("export", help="Export audits to CSV")
    p_export.add_argument("output", help="Output CSV path")
    p_export.add_argument("--data-dir", default=str(DEFAULT_DIR))
    p_export.set_defaults(func=cmd_export)

    p_report = sub.add_parser("report", help="Print a stored audit report")
    p_report.add_argument("audit_id", help="Audit ID to report on")
    p_report.add_argument("--out", help="Write report to this file as well")
    p_report.add_argument("--data-dir", default=str(DEFAULT_DIR))
    p_report.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    print_disclaimer()
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
