"""Local JSON storage for forms, submissions, and audit results."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .models import AuditResult, FormSubmission, FormTemplate

DEFAULT_DIR = Path("data")


class JsonStorage:
    """File-backed JSON store. Everything stays on the local machine."""

    def __init__(self, base_dir: str | Path | None = None) -> None:
        self.base_dir = Path(base_dir or DEFAULT_DIR)
        self.forms_dir = self.base_dir / "forms"
        self.submissions_dir = self.base_dir / "submissions"
        self.audits_dir = self.base_dir / "audits"
        for d in (self.base_dir, self.forms_dir, self.submissions_dir, self.audits_dir):
            d.mkdir(parents=True, exist_ok=True)

    # -- templates -----------------------------------------------------
    def save_template(self, template: FormTemplate) -> None:
        path = self.forms_dir / f"{template.form_id}.json"
        path.write_text(json.dumps(template.to_dict(), indent=2))

    def load_template(self, form_id: str) -> FormTemplate | None:
        path = self.forms_dir / f"{form_id}.json"
        if not path.exists():
            return None
        return FormTemplate.from_dict(json.loads(path.read_text()))

    def list_templates(self) -> list[FormTemplate]:
        templates: list[FormTemplate] = []
        for path in sorted(self.forms_dir.glob("*.json")):
            try:
                templates.append(FormTemplate.from_dict(json.loads(path.read_text())))
            except (json.JSONDecodeError, KeyError):
                continue
        return templates

    # -- submissions ---------------------------------------------------
    def save_submission(self, submission: FormSubmission) -> None:
        path = self.submissions_dir / f"{submission.submission_id}.json"
        path.write_text(json.dumps(submission.to_dict(), indent=2))

    def load_submission(self, submission_id: str) -> FormSubmission | None:
        path = self.submissions_dir / f"{submission_id}.json"
        if not path.exists():
            return None
        return FormSubmission.from_dict(json.loads(path.read_text()))

    def list_submissions(self) -> list[FormSubmission]:
        submissions: list[FormSubmission] = []
        for path in sorted(self.submissions_dir.glob("*.json")):
            try:
                submissions.append(FormSubmission.from_dict(json.loads(path.read_text())))
            except (json.JSONDecodeError, KeyError):
                continue
        return submissions

    # -- audits --------------------------------------------------------
    def save_audit(self, result: AuditResult) -> None:
        path = self.audits_dir / f"{result.audit_id}.json"
        path.write_text(json.dumps(result.to_dict(), indent=2))

    def load_audit(self, audit_id: str) -> AuditResult | None:
        path = self.audits_dir / f"{audit_id}.json"
        if not path.exists():
            return None
        return AuditResult.from_dict(json.loads(path.read_text()))

    def list_audits(self) -> list[AuditResult]:
        audits: list[AuditResult] = []
        for path in sorted(self.audits_dir.glob("*.json")):
            try:
                audits.append(AuditResult.from_dict(json.loads(path.read_text())))
            except (json.JSONDecodeError, KeyError):
                continue
        return audits

    def latest_audit_for_submission(self, submission_id: str) -> AuditResult | None:
        audits = [
            a
            for a in self.list_audits()
            if a.submission_id == submission_id
        ]
        if not audits:
            return None
        return sorted(audits, key=lambda a: a.audited_at)[-1]
