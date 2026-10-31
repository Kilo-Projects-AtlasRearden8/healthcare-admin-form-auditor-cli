"""CSV export for audit results."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .models import AuditResult


def export_csv(audits: Iterable[AuditResult], output: str | Path) -> list[str]:
    """Write audits to a CSV file. Returns the header row written."""
    fieldnames = [
        "audit_id",
        "submission_id",
        "form_id",
        "form_name",
        "passed",
        "completeness",
        "deadline_status",
        "missing_required",
        "issue_count",
        "audited_at",
    ]
    rows = []
    for a in audits:
        rows.append(
            {
                "audit_id": a.audit_id,
                "submission_id": a.submission_id,
                "form_id": a.form_id,
                "form_name": a.form_name,
                "passed": "yes" if a.passed else "no",
                "completeness": f"{a.completeness:.2f}",
                "deadline_status": a.deadline_status,
                "missing_required": "; ".join(a.missing_required),
                "issue_count": len(a.issues),
                "audited_at": a.audited_at,
            }
        )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return fieldnames
