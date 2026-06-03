from __future__ import annotations

from flir_android.common import SmokeRunner


CASE_KEY = "mock-home-connected"
CASE_ID = "MOCK-06"
DESCRIPTION = "Verify a mock connected device card is rendered on Home."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_home_connected")
    add_profile = runner.require_mock_profile().section("mock_add_device_default_name")

    runner.device.force_stop()
    runner.device.launch()
    runner.sleep(2.0)
    runner.ensure_mock_device_added(add_profile)

    image_path = runner.device.screenshot("mock_home_connected")
    required = list(profile.get("required_tokens", []))
    required.append(profile.get("device_name", add_profile["device_name"]))
    runner.assert_ocr_tokens_present(image_path, required, "Connected Home device UI did not match mock profile.")
    runner.record(CASE_ID, "PASS", "Verified mock connected device card content on Home.")
