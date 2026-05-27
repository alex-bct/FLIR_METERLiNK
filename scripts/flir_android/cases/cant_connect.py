from __future__ import annotations

from flir_android.common import AssertionFailure, SmokeRunner, any_text_present, find_node


CASE_KEY = "cant-connect"
CASE_ID = "SMK-07"
DESCRIPTION = "Open and exit the Can't connect help page."


def run(runner: SmokeRunner) -> None:
    root = runner.go_to_home_search("allow")
    if not any_text_present(root, "can't connect flir meterlink device?"):
        raise AssertionFailure("Search page does not show the help link.")
    runner.tap_token(root, "can't connect flir meterlink device?")
    help_root = runner.wait_for(["connecting your flir meterlink device"], name="cant_connect_help")
    close_node = find_node(help_root, "close", clickable_only=True)
    if close_node is not None:
        runner.tap_token(help_root, "close")
    else:
        runner.device.tap(60, 165)
        runner.sleep()
    root = runner.snapshot("cant_connect_exit")
    if not any_text_present(root, "can't connect flir meterlink device?"):
        raise AssertionFailure("Expected to return from help page to the scan page.")
    runner.record(CASE_ID, "PASS", "Opened and exited the Can't connect help page.")
