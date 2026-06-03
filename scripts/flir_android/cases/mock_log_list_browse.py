from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner


CASE_KEY = "mock-log-list-browse"
CASE_ID = "MOCK-09"
DESCRIPTION = "Verify the logs list in Files can be opened and browsed using mock data."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_log_list_browse")

    runner.device.screenshot("mock_log_list_start")
    home_tab_token = profile.get("home_tab_token", "HOME")
    try:
        runner.tap_ocr_token("mock_log_list_home_lookup", home_tab_token)
    except AssertionFailure:
        runner.tap_top_left_back()
        try:
            runner.tap_ocr_token("mock_log_list_home_retry", home_tab_token)
        except AssertionFailure:
            runner.tap_top_left_back()
            runner.tap_ocr_token("mock_log_list_home_retry_2", home_tab_token)

    try:
        runner.tap_ocr_token("mock_log_list_files_lookup", profile.get("files_tab_token", "FILES"))
    except AssertionFailure:
        runner.tap_ocr_token("mock_log_list_files_retry", profile.get("files_tab_token", "FILES"))

    log_tab_token = profile.get("log_tab_token", "Logs")
    runner.tap_ocr_token("mock_log_list_logs_lookup", log_tab_token)
    log_image = runner.device.screenshot("mock_log_list_browse")
    runner.assert_ocr_tokens_present(log_image, list(profile.get("required_tokens", [])), "Mock log list UI did not match expected tokens.")
    runner.record(CASE_ID, "PASS", "Verified mock log list browse page.")
