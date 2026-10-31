"""Printable plain-text audit report."""

from __future__ import annotations

from .models import AuditResult


def build_report(result: AuditResult) -> str:
    """Build a printable text report for one audit result."""
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("HEALTHCARE ADMIN FORM - AUDIT REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Audit ID:       {result.audit_id}")
    lines.append(f"Submission ID:  {result.submission_id}")
    lines.append(f"Form ID:        {result.form_id}")
    lines.append(f"Form name:      {result.form_name}")
    lines.append(f"Audited at:     {result.audited_at}")
    lines.append(f"Overall result: {'PASS' if result.passed else 'NEEDS ATTENTION'}")
    lines.append(f"Completeness:   {result.completeness:.2f}%")
    lines.append(f"Deadline:       {result.deadline_message or 'n/a'}")
    lines.append("")

    lines.append("-" * 70)
    lines.append("MISSING REQUIRED FIELDS")
    lines.append("-" * 70)
    if result.missing_required:
        for name in result.missing_required:
            lines.append(f"  - {name}")
    else:
        lines.append("  None.")
    lines.append("")

    lines.append("-" * 70)
    lines.append("ISSUES")
    lines.append("-" * 70)
    if result.issues:
        for issue in result.issues:
            tag = f"[{issue.severity.upper()}]"
            target = f" {issue.field}:" if issue.field else ":"
            lines.append(f"  {tag}{target} {issue.message}")
    else:
        lines.append("  None.")
    lines.append("")

    lines.append("-" * 70)
    lines.append("EDUCATION-ONLY REMINDER")
    lines.append("-" * 70)
    lines.append("  This report is for administrative organization only.")
    lines.append("  It is not medical advice and not a compliance determination.")
    lines.append("  Review with your facility's policies and qualified staff.")
    lines.append("")
    lines.append("=" * 70)
    lines.append("End of report.")
    lines.append("=" * 70)
    return "\n".join(lines) + "\n"
