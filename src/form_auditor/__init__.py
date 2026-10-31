"""Healthcare admin form auditor CLI.

Education-only tool for checking healthcare administrative paperwork.
Never medical advice. All data stays local on your machine.
"""

from .models import FieldTemplate, FormSubmission, AuditResult, AuditIssue
from .auditor import audit_submission
from .storage import JsonStorage
from .export import export_csv
from .report import build_report

__all__ = [
    "FieldTemplate",
    "FormSubmission",
    "AuditResult",
    "AuditIssue",
    "audit_submission",
    "JsonStorage",
    "export_csv",
    "build_report",
]

__version__ = "1.0.0"
