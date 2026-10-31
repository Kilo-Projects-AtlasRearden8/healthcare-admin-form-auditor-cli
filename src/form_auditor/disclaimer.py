"""Education-only disclaimer. Displayed on every run."""

DISCLAIMER = """
================================================================================
HEALTHCARE ADMIN FORM AUDITOR - EDUCATION ONLY
================================================================================

This tool is for educational and administrative organization purposes only.
It is NOT medical advice, NOT a substitute for professional medical judgment,
and NOT a substitute for compliance review by a qualified healthcare
administrator, compliance officer, or attorney.

Always follow your facility's policies, applicable laws (such as HIPAA in the
United States), and the guidance of qualified professionals when handling
healthcare paperwork or patient information.

This tool runs entirely on your local machine. It does not send any data over
the network, and it does not store anything in the cloud. You are responsible
for the data you enter into it.

By using this tool you acknowledge that Asdale Dynamics, LLC provides it
"as is" for education only, with no warranties of any kind.
================================================================================
"""


def show_disclaimer() -> str:
    """Return the education-only disclaimer text."""
    return DISCLAIMER.strip()


def print_disclaimer() -> None:
    """Print the education-only disclaimer to stdout."""
    print(show_disclaimer())
