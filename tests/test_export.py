"""Tests for CSV export."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from form_auditor.models import AuditIssue, AuditResult
from form_auditor.export import export_csv


def _audit(audit_id: str, completeness: float, passed: bool) -> AuditResult:
    issues = [] if passed else [AuditIssue(field=None, code="x", message="y")]
    return AuditResult(
        audit_id=audit_id,
        submission_id="sub",
        form_id="f1",
        form_name="Form One",
        completeness=completeness,
        issues=issues,
    )


def test_export_csv_writes_header_and_rows():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "audits.csv"
        header = export_csv(
            [_audit("a1", 100.0, True), _audit("a2", 50.0, False)], out
        )
        assert "audit_id" in header
        rows = list(csv.DictReader(out.open()))
        assert len(rows) == 2
        assert rows[0]["audit_id"] == "a1"
        assert rows[0]["completeness"] == "100.00"
        assert rows[0]["passed"] == "yes"
        assert rows[1]["passed"] == "no"
