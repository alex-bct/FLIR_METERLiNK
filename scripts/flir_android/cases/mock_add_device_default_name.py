from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, any_text_present


CASE_KEY = "mock-add-device-default-name"
CASE_ID = "MOCK-04"
DESCRIPTION = "Add a mock device from Available devices and keep the default name."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_add_device_default_name")
    
    # Ensure we start from a clean state (HOME screen)
    runner.device.force_stop()
    runner.device.launch()
    runner.sleep(2.0)
    
    runner.device.screenshot("mock_add_device_start")
    runner.ensure_mock_device_added(profile)
    runner.device.screenshot("mock_add_device_home")
    runner.record(CASE_ID, "PASS", "Added mock device with default name and captured the resulting Home card screenshot.")
