from __future__ import annotations

from flir_android.common import SmokeRunner


CASE_KEY = "mock-gallery-empty"
CASE_ID = "MOCK-03"
DESCRIPTION = "Verify the gallery/files area empty state using mock data."


def run(runner: SmokeRunner) -> None:
    profile = runner.require_mock_profile().section("mock_gallery_empty")
    runner.device.screenshot("mock_gallery_start")
    
    # If we are in Device Details or somewhere else, go back to ensure bottom tabs are visible
    runner.tap_top_left_back() 
    runner.sleep(1.0)
    
    runner.tap_ocr_token("mock_gallery_files_lookup", profile.get("files_tab_token", "FILES"))
    files_image = runner.device.screenshot("mock_gallery_files")
    if "gallery_tab_token" in profile:
        runner.tap_ocr_token("mock_gallery_tab_lookup", profile["gallery_tab_token"])
        files_image = runner.device.screenshot("mock_gallery_tab")
    runner.assert_ocr_tokens_present(files_image, list(profile.get("required_tokens", [])), "Mock gallery empty-state UI did not match expected tokens.")
    
    # Navigate back to HOME after verification
    runner.tap_ocr_token("mock_gallery_back_home", "HOME")
    
    runner.record(CASE_ID, "PASS", "Verified mock gallery empty-state UI and returned to HOME.")
