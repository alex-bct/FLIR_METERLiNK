from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, any_text_present


CASE_KEY = "mock-delete-device-card"
CASE_ID = "MOCK-05"
DESCRIPTION = "Open a mock device card and remove it from the Home list."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_delete_device_card")
    add_profile = runner.require_mock_profile().section("mock_add_device_default_name")
    runner.device.force_stop()
    runner.device.launch()
    runner.sleep(2.0)
    runner.device.screenshot("mock_delete_start")
    runner.ensure_mock_device_added(add_profile)
    runner.device.screenshot("mock_delete_ready")
    sn_suffix = profile.get("sn_suffix")
    home_card_tap = profile.get("home_card_tap")
    try:
        runner.tap_home_device_by_ocr(profile["device_name"], sn_suffix)
    except AssertionFailure:
        if isinstance(home_card_tap, dict):
            runner.device.tap(int(home_card_tap["x"]), int(home_card_tap["y"]))
            runner.sleep(2.0)
        else:
            raise

    more_token = profile.get("more_token", "More")
    runner.device.screenshot("mock_delete_detail")
    more_tap = profile.get("more_tap")
    if isinstance(more_tap, dict):
        runner.device.tap(int(more_tap["x"]), int(more_tap["y"]))
        runner.sleep(2.0)
    else:
        # Default for current Device Details layout: the three-dot icon above the More label.
        runner.device.tap(926, 620)
        runner.sleep(2.0)

    more_root = runner.snapshot("mock_delete_more")
    remove_token = profile.get("remove_token", "Remove Device")
    runner.tap_token(more_root, remove_token)

    confirm_root = runner.snapshot("mock_delete_confirm")
    confirm_token = profile.get("confirm_token", "Remove")
    confirm_tap = profile.get("confirm_tap")
    if isinstance(confirm_tap, dict):
        runner.device.tap(int(confirm_tap["x"]), int(confirm_tap["y"]))
        runner.sleep(2.0)
    elif any_text_present(confirm_root, confirm_token):
        runner.tap_token(confirm_root, confirm_token)
        runner.sleep(2.0)
    else:
        # Some builds keep the first remove action as the final delete action.
        runner.sleep(1.5)

    final_png = runner.device.screenshot("mock_delete_home")
    runner.record(CASE_ID, "PASS", f"Triggered mock device removal flow and captured final Home screenshot at {final_png.name}.")
