from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, ocr_has_any_token


CASE_KEY = "mock-settings-version"
CASE_ID = "MOCK-10"
DESCRIPTION = "Open Settings and verify the app version information is visible."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_settings_version")
    settings_markers = list(profile.get("settings_screen_tokens", ["NOTIFICATION", "APP SETTING", "SUPPORT"]))
    start_image = runner.device.screenshot("mock_settings_start")
    if not any(ocr_has_any_token(start_image, marker) for marker in settings_markers):
        try:
            runner.tap_ocr_token("mock_settings_tab_lookup", profile.get("settings_tab_token", "SETTINGS"))
        except AssertionFailure:
            runner.tap_top_left_back()
            runner.tap_ocr_token("mock_settings_tab_retry", profile.get("settings_tab_token", "SETTINGS"))

    required_tokens = list(profile.get("required_tokens", []))
    swipe = profile.get("scroll_up_swipe")
    attempts = int(profile.get("scroll_attempts", 3))
    last_error: AssertionFailure | None = None
    for attempt in range(attempts):
        shot_name = "mock_settings_version" if attempt == 0 else f"mock_settings_version_scrolled_{attempt}"
        settings_image = runner.device.screenshot(shot_name)
        try:
            runner.assert_ocr_tokens_present(
                settings_image,
                required_tokens,
                "Settings version UI did not match expected tokens.",
            )
            runner.record(CASE_ID, "PASS", "Verified app version information on Settings.")
            return
        except AssertionFailure as exc:
            last_error = exc
            if isinstance(swipe, dict):
                runner.device.swipe(
                    int(swipe["x1"]),
                    int(swipe["y1"]),
                    int(swipe["x2"]),
                    int(swipe["y2"]),
                    int(swipe.get("duration_ms", 250)),
                )
            else:
                runner.device.swipe(540, 1750, 540, 650, 300)
            runner.sleep(1.5)

    if last_error is not None:
        raise last_error
    runner.record(CASE_ID, "PASS", "Verified app version information on Settings.")
