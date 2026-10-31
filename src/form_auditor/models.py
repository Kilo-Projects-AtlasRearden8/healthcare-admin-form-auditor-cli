"""Data models for form auditing."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any


@dataclass
class FieldTemplate:
    """Definition of one expected field on a form template."""

    name: str
    required: bool = True
    field_type: str = "text"  # text, date, number, boolean, choice
    choices: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "required": self.required,
            "field_type": self.field_type,
            "choices": self.choices,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FieldTemplate":
        return FieldTemplate(
            name=data["name"],
            required=bool(data.get("required", True)),
            field_type=str(data.get("field_type", "text")),
            choices=data.get("choices"),
        )


@dataclass
class FormTemplate:
    """A form template: the fields a form is expected to have."""

    form_id: str
    form_name: str
    fields: list[FieldTemplate] = field(default_factory=list)

    def field_by_name(self, name: str) -> FieldTemplate | None:
        for f in self.fields:
            if f.name == name:
                return f
        return None

    def required_fields(self) -> list[FieldTemplate]:
        return [f for f in self.fields if f.required]

    def to_dict(self) -> dict[str, Any]:
        return {
            "form_id": self.form_id,
            "form_name": self.form_name,
            "fields": [f.to_dict() for f in self.fields],
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FormTemplate":
        return FormTemplate(
            form_id=data["form_id"],
            form_name=data.get("form_name", data["form_id"]),
            fields=[FieldTemplate.from_dict(f) for f in data.get("fields", [])],
        )


@dataclass
class FormSubmission:
    """One filled-in instance of a form."""

    submission_id: str
    form_id: str
    form_name: str
    deadline: str | None = None  # ISO date string, optional
    values: dict[str, Any] = field(default_factory=dict)
    submitted_by: str = ""
    submitted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "submission_id": self.submission_id,
            "form_id": self.form_id,
            "form_name": self.form_name,
            "deadline": self.deadline,
            "values": self.values,
            "submitted_by": self.submitted_by,
            "submitted_at": self.submitted_at,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FormSubmission":
        return FormSubmission(
            submission_id=data["submission_id"],
            form_id=data["form_id"],
            form_name=data.get("form_name", ""),
            deadline=data.get("deadline"),
            values=data.get("values", {}),
            submitted_by=data.get("submitted_by", ""),
            submitted_at=data.get("submitted_at", datetime.now(timezone.utc).isoformat()),
        )


@dataclass
class AuditIssue:
    """A single problem found during an audit."""

    field: str | None
    code: str  # missing_required, deadline_overdue, deadline_approaching, empty_value
    message: str
    severity: str = "error"  # error, warning, info

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass
class AuditResult:
    """Result of auditing one form submission."""

    audit_id: str
    submission_id: str
    form_id: str
    form_name: str
    missing_required: list[str] = field(default_factory=list)
    deadline_status: str = "no_deadline"  # no_deadline, met, approaching, overdue
    deadline_message: str = ""
    completeness: float = 0.0  # 0.0 to 100.0
    issues: list[AuditIssue] = field(default_factory=list)
    audited_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def passed(self) -> bool:
        return len(self.issues) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "submission_id": self.submission_id,
            "form_id": self.form_id,
            "form_name": self.form_name,
            "missing_required": self.missing_required,
            "deadline_status": self.deadline_status,
            "deadline_message": self.deadline_message,
            "completeness": self.completeness,
            "issues": [i.to_dict() for i in self.issues],
            "passed": self.passed,
            "audited_at": self.audited_at,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "AuditResult":
        return AuditResult(
            audit_id=data["audit_id"],
            submission_id=data["submission_id"],
            form_id=data["form_id"],
            form_name=data.get("form_name", ""),
            missing_required=data.get("missing_required", []),
            deadline_status=data.get("deadline_status", "no_deadline"),
            deadline_message=data.get("deadline_message", ""),
            completeness=float(data.get("completeness", 0.0)),
            issues=[AuditIssue(**i) for i in data.get("issues", [])],
            audited_at=data.get("audited_at", datetime.now(timezone.utc).isoformat()),
        )
