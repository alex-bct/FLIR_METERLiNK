from __future__ import annotations

from flir_android.common import SmokeRunner


CASE_KEY = "mock-device-detail-disconnected"
CASE_ID = "MOCK-02"
DESCRIPTION = "Open a mock device detail page and verify disconnected-state UI."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_device_detail_disconnected")
    runner.device.screenshot("mock_device_detail_start")
    runner.tap_ocr_token("mock_device_detail_lookup", profile["device_name"])
    detail_image = runner.device.screenshot("mock_device_detail_open")
    required = list(profile.get("required_tokens", []))
    required.append(profile["device_name"])
    runner.assert_ocr_tokens_present(detail_image, required, "Mock device detail UI did not match expected disconnected state.")
    runner.record(CASE_ID, "PASS", "Verified mock disconnected-state device detail content.")
