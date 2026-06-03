from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, is_home_like_screen


CASE_KEY = "search-no-device"
CASE_ID = "SMK-06"
DESCRIPTION = "Reach the scan page without requiring a physical device."


def run(runner: SmokeRunner) -> None:
    root = runner.go_to_home_search("allow")
    if not is_home_like_screen(root):
        raise AssertionFailure("Search/empty state was not visible.")
    runner.record(CASE_ID, "PASS", "Reached the scan page without requiring a physical device.")
