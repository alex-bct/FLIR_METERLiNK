from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import shutil

from flir_android.common import AdbDevice, AdbError, AssertionFailure, CaseDefinition, MockProfile, SmokeRunner


CASE_MODULES = {
    "oobe-allow": "flir_android.cases.oobe_allow",
    "oobe-deny": "flir_android.cases.oobe_deny",
    "search-no-device": "flir_android.cases.search_no_device",
    "cant-connect": "flir_android.cases.cant_connect",
    "mock-add-device-default-name": "flir_android.cases.mock_add_device_default_name",
    "mock-delete-device-card": "flir_android.cases.mock_delete_device_card",
    "mock-home-disconnected": "flir_android.cases.mock_home_disconnected",
    "mock-device-detail-disconnected": "flir_android.cases.mock_device_detail_disconnected",
    "mock-gallery-empty": "flir_android.cases.mock_gallery_empty",
}

SUITES = {
    "oobe-suite": ["oobe-allow", "oobe-deny", "search-no-device", "cant-connect"],
    "mock-suite": [
        "mock-add-device-default-name",
        "mock-home-disconnected",
        "mock-device-detail-disconnected",
        "mock-gallery-empty",
    ],
}


def load_mock_profile(path_value: str | None) -> MockProfile | None:
    if not path_value:
        return None
    path = Path(path_value).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    return MockProfile(path=path, data=data)


def load_case(key: str) -> CaseDefinition:
    module = importlib.import_module(CASE_MODULES[key])
    return CaseDefinition(
        key=module.CASE_KEY,
        case_id=module.CASE_ID,
        description=module.DESCRIPTION,
        runner=CASE_MODULES[key],
    )


def run_case(runner: SmokeRunner, key: str) -> None:
    module = importlib.import_module(CASE_MODULES[key])
    module.run(runner)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run FLIR MeterLiNK Android smoke checks with adb.")
    parser.add_argument(
        "--case",
        choices=sorted(list(CASE_MODULES.keys()) + list(SUITES.keys())),
        default="oobe-suite",
        help="Smoke case or suite to run.",
    )
    parser.add_argument("--serial", help="ADB device serial. Defaults to $ANDROID_SERIAL when set.")
    parser.add_argument(
        "--artifacts-dir",
        default="artifacts/android_smoke",
        help="Directory for screenshots, UI dumps, and results.",
    )
    parser.add_argument(
        "--mock-profile",
        help="JSON file with expected mock-device labels and screen tokens for mock-driven cases.",
    )
    return parser


def expand_case_selection(case_key: str) -> list[str]:
    return SUITES.get(case_key, [case_key])


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    work_dir = Path(args.artifacts_dir).resolve()
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    device = AdbDevice(serial=args.serial, work_dir=work_dir)
    runner = SmokeRunner(device, mock_profile=load_mock_profile(args.mock_profile))

    failures = 0
    for case_key in expand_case_selection(args.case):
        case_def = load_case(case_key)
        try:
            runner.log(f"Running {case_def.key} ({case_def.case_id}) ...")
            run_case(runner, case_key)
        except (AdbError, AssertionFailure) as exc:
            failures += 1
            runner.record(case_def.case_id, "FAIL", str(exc))
            runner.log(f"FAIL [{case_def.case_id}]: {exc}")

    results_path = runner.write_results()
    runner.log(f"Artifacts: {work_dir}")
    runner.log(f"Results: {results_path}")
    return 1 if failures else 0
