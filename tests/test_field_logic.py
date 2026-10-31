"""Tests for field-logic: missing required fields, deadlines, completeness."""

from __future__ import annotations

import datetime as dt

import pytest

from form_auditor.auditor import audit_submission, _deadline_status, _is_empty
from form_auditor.models import FieldTemplate, FormSubmission, FormTemplate


def _template() -> FormTemplate:
    return FormTemplate(
        form_id="intake-001",
        form_name="Patient Intake",
        fields=[
            FieldTemplate(name="patient_reference", required=True, field_type="text"),
            FieldTemplate(name="date_of_birth", required=True, field_type="date"),
            FieldTemplate(name="insurance_provider", required=True, field_type="text"),
            FieldTemplate(name="allergies", required=False, field_type="text"),
            FieldTemplate(name="consent", required=True, field_type="boolean"),
        ],
    )


def _submission(values=None, deadline=None) -> FormSubmission:
    return FormSubmission(
        submission_id="SUB-TEST",
        form_id="intake-001",
        form_name="Patient Intake",
        deadline=deadline,
        values=values or {},
    )


def test_missing_required_fields_detected():
    result = audit_submission(_submission(), _template())
    assert result.missing_required == [
        "patient_reference",
        "date_of_birth",
        "insurance_provider",
        "consent",
    ]
    assert not result.passed
    missing_codes = [i.code for i in result.issues if i.code == "missing_required"]
    assert len(missing_codes) == 4


def test_optional_field_not_reported_as_missing():
    result = audit_submission(
        _submission(
            {
                "patient_reference": "PAT-1",
                "date_of_birth": "1980-01-01",
                "insurance_provider": "Example Health",
                "consent": True,
            }
        ),
        _template(),
    )
    assert result.missing_required == []
    assert "allergies" not in result.missing_required
    codes = [i.code for i in result.issues]
    assert "missing_required" not in codes
    # Optional empty field surfaces as info only, not a failure.
    assert not any(i.severity == "error" for i in result.issues)


def test_filled_required_fields_pass():
    result = audit_submission(
        _submission(
            {
                "patient_reference": "PAT-1",
                "date_of_birth": "1980-01-01",
                "insurance_provider": "Example Health",
                "consent": True,
            }
        ),
        _template(),
    )
    assert result.missing_required == []
    assert not any(i.code == "missing_required" for i in result.issues)
    assert result.completeness == 80.0  # 4 of 5 fields filled


def test_completeness_partial():
    result = audit_submission(
        _submission(
            {
                "patient_reference": "PAT-1",
                "date_of_birth": "",
                "insurance_provider": "Example Health",
                "consent": False,
            }
        ),
        _template(),
    )
    assert result.completeness == 60.0  # 3 of 5 fields filled


def test_completeness_no_fields_is_100():
    empty = FormTemplate(form_id="e", form_name="E", fields=[])
    result = audit_submission(_submission(), empty)
    assert result.completeness == 100.0


def test_is_empty_recognizes_various_empties():
    assert _is_empty(None)
    assert _is_empty("")
    assert _is_empty("   ")
    assert _is_empty([])
    assert _is_empty({})
    assert not _is_empty(0)  # zero is a deliberate number
    assert not _is_empty(False)  # False is a deliberate boolean
    assert not _is_empty("0")
    assert not _is_empty("  x  ")


def test_deadline_overdue():
    yesterday = (dt.date.today() - dt.timedelta(days=3)).isoformat()
    status, message = _deadline_status(yesterday)
    assert status == "overdue"
    assert "overdue" in message


def test_deadline_approaching():
    soon = (dt.date.today() + dt.timedelta(days=3)).isoformat()
    status, _ = _deadline_status(soon)
    assert status == "approaching"


def test_deadline_met():
    later = (dt.date.today() + dt.timedelta(days=20)).isoformat()
    status, _ = _deadline_status(later)
    assert status == "met"


def test_deadline_none():
    status, _ = _deadline_status(None)
    assert status == "no_deadline"


def test_deadline_invalid():
    status, message = _deadline_status("not-a-date")
    assert status == "invalid_deadline"
    assert "not-a-date" in message


def test_audit_result_to_and_from_dict():
    template = _template()
    result = audit_submission(_submission(), template)
    restored = type(result).from_dict(result.to_dict())
    assert restored.audit_id == result.audit_id
    assert restored.missing_required == result.missing_required
    assert restored.deadline_status == result.deadline_status
    assert restored.completeness == result.completeness
    assert restored.passed == result.passed
