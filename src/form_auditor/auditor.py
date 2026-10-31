"""Core auditing logic: missing required fields, deadlines, completeness."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from .models import (
    AuditIssue,
    AuditResult,
    FieldTemplate,
    FormSubmission,
)

APPROACHING_DAYS = 7


def _is_empty(value: Any) -> bool:
    """Return True if a field value counts as empty/not provided."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, dict):
        return len(value) == 0
    if isinstance(value, bool):
        return False  # False is a deliberate boolean answer
    if isinstance(value, (int, float)):
        return False  # 0 is a deliberate numeric answer
    return False


def _deadline_status(deadline: str | None) -> tuple[str, str]:
    """Classify an optional ISO deadline date relative to today."""
    if not deadline:
        return "no_deadline", "No deadline recorded."
    try:
        due = date.fromisoformat(deadline)
    except ValueError:
        return "invalid_deadline", f"Deadline '{deadline}' is not a valid ISO date (YYYY-MM-DD)."
    today = date.today()
    delta = (due - today).days
    if delta < 0:
        return "overdue", f"Deadline {due} is overdue by {-delta} day(s)."
    if delta <= APPROACHING_DAYS:
        return "approaching", f"Deadline {due} is in {delta} day(s)."
    return "met", f"Deadline {due} is met ({delta} day(s) away)."


def audit_submission(submission: FormSubmission, template: FormTemplate) -> AuditResult:
    """Audit one submission against its template.

    Checks for missing required fields, deadline status, and overall
    completeness (share of defined fields with a non-empty value).
    """
    missing_required: list[str] = []
    issues: list[AuditIssue] = []

    # Missing required fields.
    for field in template.required_fields():
        value = submission.values.get(field.name)
        if _is_empty(value):
            missing_required.append(field.name)
            issues.append(
                AuditIssue(
                    field=field.name,
                    code="missing_required",
                    message=f"Required field '{field.name}' is missing or empty.",
                    severity="error",
                )
            )

    # Empty non-required fields are informational only.
    for field in template.fields:
        if field.required:
            continue
        value = submission.values.get(field.name)
        if _is_empty(value):
            issues.append(
                AuditIssue(
                    field=field.name,
                    code="empty_value",
                    message=f"Optional field '{field.name}' is empty.",
                    severity="info",
                )
            )

    # Deadline check.
    deadline_status, deadline_message = _deadline_status(submission.deadline)
    if deadline_status == "overdue":
        issues.append(
            AuditIssue(
                field=None,
                code="deadline_overdue",
                message=deadline_message,
                severity="error",
            )
        )
    elif deadline_status == "approaching":
        issues.append(
            AuditIssue(
                field=None,
                code="deadline_approaching",
                message=deadline_message,
                severity="warning",
            )
        )
    elif deadline_status == "invalid_deadline":
        issues.append(
            AuditIssue(
                field="deadline",
                code="deadline_invalid",
                message=deadline_message,
                severity="error",
            )
        )

    # Completeness: share of defined fields carrying a non-empty value.
    defined = [f.name for f in template.fields]
    if defined:
        filled = sum(1 for name in defined if not _is_empty(submission.values.get(name)))
        completeness = round((filled / len(defined)) * 100, 2)
    else:
        completeness = 100.0

    audit_id = f"AUD-{submission.submission_id}-{int(datetime.now(timezone.utc).timestamp())}"
    return AuditResult(
        audit_id=audit_id,
        submission_id=submission.submission_id,
        form_id=submission.form_id,
        form_name=submission.form_name,
        missing_required=missing_required,
        deadline_status=deadline_status,
        deadline_message=deadline_message,
        completeness=completeness,
        issues=issues,
    )
