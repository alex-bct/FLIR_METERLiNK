from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, any_text_present


CASE_KEY = "oobe-deny"
CASE_ID = "SMK-03"
DESCRIPTION = "Deny OOBE permissions and verify the app stays recoverable."


def run(runner: SmokeRunner) -> None:
    root = runner.go_to_home_search("deny")
    if not any_text_present(
        root,
        "location permission",
        "welcome to flir meterlink",
        "searching for flir meterlink devices",
        "can't connect flir meterlink device?",
    ):
        raise AssertionFailure("Expected a visible post-deny state after rejecting permissions.")
    runner.record(CASE_ID, "PASS", "Denied OOBE permission flow and the app remained recoverable.")
