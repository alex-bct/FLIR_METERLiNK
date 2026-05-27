from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, is_home_like_screen


CASE_KEY = "oobe-allow"
CASE_ID = "SMK-02"
DESCRIPTION = "Allow OOBE permissions and land on the scan page."


def run(runner: SmokeRunner) -> None:
    root = runner.go_to_home_search("allow")
    if not is_home_like_screen(root):
        raise AssertionFailure("Expected to land on the scan/help page after allowing permissions.")
    runner.record(CASE_ID, "PASS", "Allowed OOBE permission flow and reached the scan page.")
