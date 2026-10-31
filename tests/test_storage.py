"""Tests for storage round-trips."""

from __future__ import annotations

import tempfile
from pathlib import Path

from form_auditor.models import AuditResult, FormSubmission, FormTemplate
from form_auditor.storage import JsonStorage


def _storage():
    with tempfile.TemporaryDirectory() as tmp:
        yield JsonStorage(tmp)


def test_save_and_load_template():
    storage = JsonStorage.__new__(JsonStorage)
    with tempfile.TemporaryDirectory() as tmp:
        storage = JsonStorage(tmp)
        t = FormTemplate(form_id="t1", form_name="Template One")
        storage.save_template(t)
        loaded = storage.load_template("t1")
        assert loaded is not None
        assert loaded.form_name == "Template One"
        assert storage.list_templates()[0].form_id == "t1"


def test_save_and_load_submission_and_audit():
    with tempfile.TemporaryDirectory() as tmp:
        storage = JsonStorage(tmp)
        s = FormSubmission(
            submission_id="s1", form_id="t1", form_name="T", values={"a": "1"}
        )
        storage.save_submission(s)
        assert storage.load_submission("s1").values == {"a": "1"}

        a = AuditResult(
            audit_id="a1",
            submission_id="s1",
            form_id="t1",
            form_name="T",
            completeness=50.0,
        )
        storage.save_audit(a)
        loaded = storage.load_audit("a1")
        assert loaded is not None
        assert loaded.completeness == 50.0
        assert storage.latest_audit_for_submission("s1").audit_id == "a1"
        assert len(storage.list_audits()) == 1


def test_missing_keys_do_not_crash_list():
    with tempfile.TemporaryDirectory() as tmp:
        storage = JsonStorage(tmp)
        (storage.forms_dir / "bad.json").write_text("{not json")
        assert storage.list_templates() == []
