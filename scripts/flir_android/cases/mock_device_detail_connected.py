from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner


CASE_KEY = "mock-device-detail-connected"
CASE_ID = "MOCK-07"
DESCRIPTION = "Open a mock connected device detail page and verify connected-state UI."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_device_detail_connected")
    add_profile = runner.require_mock_profile().section("mock_add_device_default_name")

    runner.device.force_stop()
    runner.device.launch()
    runner.sleep(2.0)
    runner.ensure_mock_device_added(add_profile)
    try:
        runner.tap_home_device_by_ocr(profile.get("device_name", add_profile["device_name"]), profile.get("sn_suffix"))
    except AssertionFailure:
        home_card_tap = profile.get("home_card_tap")
        if not isinstance(home_card_tap, dict):
            raise
        runner.device.tap(int(home_card_tap["x"]), int(home_card_tap["y"]))
        runner.sleep(2.0)

    detail_image = runner.device.screenshot("mock_device_detail_connected")
    required = list(profile.get("required_tokens", []))
    required.append(profile.get("device_name", add_profile["device_name"]))
    runner.assert_ocr_tokens_present(detail_image, required, "Mock connected device detail UI did not match expected state.")
    runner.record(CASE_ID, "PASS", "Verified mock connected-state device detail content.")
