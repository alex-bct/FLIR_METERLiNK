from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner


CASE_KEY = "mock-device-detail-more-menu"
CASE_ID = "MOCK-08"
DESCRIPTION = "Open the More menu from a mock device detail page and verify its actions."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_device_detail_more_menu")
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

    more_tap = profile.get("more_tap")
    if isinstance(more_tap, dict):
        runner.device.tap(int(more_tap["x"]), int(more_tap["y"]))
        runner.sleep(2.0)
    else:
        runner.tap_ocr_token("mock_detail_more_lookup", profile.get("more_token", "More"))

    menu_image = runner.device.screenshot("mock_device_detail_more_menu")
    runner.assert_ocr_tokens_present(
        menu_image,
        list(profile.get("required_tokens", [])),
        "Mock device detail More menu did not match expected actions.",
    )
    runner.record(CASE_ID, "PASS", "Verified mock device detail More menu actions.")
