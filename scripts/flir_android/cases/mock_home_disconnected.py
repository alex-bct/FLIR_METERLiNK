from __future__ import annotations

from flir_android.common import SmokeRunner


CASE_KEY = "mock-home-disconnected"
CASE_ID = "MOCK-01"
DESCRIPTION = "Verify a mock disconnected device card is rendered on Home."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_home_disconnected")
    image_path = runner.device.screenshot("mock_home_disconnected")
    required = list(profile.get("required_tokens", []))
    if "device_name" in profile:
        required.append(profile["device_name"])
    runner.assert_ocr_tokens_present(image_path, required, "Disconnected Home device UI did not match mock profile.")
    runner.record(CASE_ID, "PASS", "Verified mock disconnected device card content on Home.")
