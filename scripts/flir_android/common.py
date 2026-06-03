from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PACKAGE = "com.flir.METERLiNKAPP.beta"
ACTIVITY = "com.flir.METERLiNKAPP.MainActivity"
DEFAULT_SERIAL_ENV = "ANDROID_SERIAL"
DEFAULT_HOME_ADD_BUTTON = (990, 179)
DEFAULT_TOP_LEFT_BACK_BUTTON = (90, 168)


@dataclass
class Node:
    text: str
    desc: str
    resource_id: str
    clickable: bool
    bounds: tuple[int, int, int, int]

    @property
    def center(self) -> tuple[int, int]:
        x1, y1, x2, y2 = self.bounds
        return ((x1 + x2) // 2, (y1 + y2) // 2)


@dataclass(frozen=True)
class OCRBox:
    text: str
    left: int
    top: int
    width: int
    height: int
    confidence: float

    @property
    def center(self) -> tuple[int, int]:
        return (self.left + self.width // 2, self.top + self.height // 2)


@dataclass(frozen=True)
class CaseDefinition:
    key: str
    case_id: str
    description: str
    runner: str


@dataclass(frozen=True)
class MockProfile:
    path: Path
    data: dict

    def section(self, key: str) -> dict:
        value = self.data.get(key)
        if not isinstance(value, dict):
            raise AssertionFailure(f"Mock profile section '{key}' is missing.")
        return value


class AdbError(RuntimeError):
    pass


class AssertionFailure(RuntimeError):
    pass


class AdbDevice:
    def __init__(self, serial: str | None = None, work_dir: Path | None = None):
        self.serial = serial or os.environ.get(DEFAULT_SERIAL_ENV)
        self.work_dir = work_dir or Path(tempfile.mkdtemp(prefix="flir_smoke_"))
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.dump_counter = 0

    def _base_cmd(self) -> list[str]:
        cmd = ["adb"]
        if self.serial:
            cmd += ["-s", self.serial]
        return cmd

    def run(self, *args: str, check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess[str]:
        cmd = self._base_cmd() + list(args)
        proc = subprocess.run(cmd, text=True, capture_output=capture_output, check=False)
        if check and proc.returncode != 0:
            raise AdbError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr or proc.stdout}")
        return proc

    def launch(self) -> None:
        self.run("shell", "am", "start", "-W", "-n", f"{PACKAGE}/{ACTIVITY}")

    def clear_app(self) -> None:
        self.run("shell", "pm", "clear", PACKAGE)

    def force_stop(self) -> None:
        self.run("shell", "am", "force-stop", PACKAGE)

    def tap(self, x: int, y: int) -> None:
        self.run("shell", "input", "tap", str(x), str(y))

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 250) -> None:
        self.run("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms))

    def screenshot(self, name: str) -> Path:
        target = self.work_dir / f"{name}.png"
        last_error = "unknown screenshot failure"
        for attempt in range(3):
            try:
                with target.open("wb") as fh:
                    cmd = self._base_cmd() + ["exec-out", "screencap", "-p"]
                    proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, check=False, timeout=20)
                if proc.returncode == 0 and target.exists() and target.stat().st_size > 0:
                    return target
                last_error = proc.stderr.decode("utf-8", errors="ignore") or f"empty screenshot on attempt {attempt + 1}"
            except subprocess.TimeoutExpired:
                remote = f"/sdcard/{name}.png"
                self.run("shell", "rm", "-f", remote, check=False)
                self.run("shell", "screencap", "-p", remote, check=False)
                pull_proc = self.run("pull", remote, str(target), check=False)
                if pull_proc.returncode == 0 and target.exists() and target.stat().st_size > 0:
                    return target
                last_error = pull_proc.stderr or pull_proc.stdout or f"screenshot timeout on attempt {attempt + 1}"
            target.unlink(missing_ok=True)
            time.sleep(0.8)
        raise AdbError(last_error)

    def dump_ui(self, name: str | None = None) -> tuple[ET.Element, Path]:
        self.dump_counter += 1
        name = name or f"dump_{self.dump_counter:02d}"
        remote = f"/sdcard/{name}.xml"
        local = self.work_dir / f"{name}.xml"
        last_error = None
        for _ in range(3):
            self.run("shell", "rm", "-f", remote, check=False)
            self.run("shell", "uiautomator", "dump", remote, check=False)
            pull_proc = self.run("pull", remote, str(local), check=False)
            if pull_proc.returncode == 0 and local.exists():
                return ET.parse(local).getroot(), local
            last_error = pull_proc.stderr or pull_proc.stdout or "Unknown ui dump failure"
            time.sleep(0.8)
        cmd = self._base_cmd() + ["exec-out", "uiautomator", "dump", "/dev/tty"]
        proc = subprocess.run(cmd, capture_output=True, check=False)
        if proc.returncode == 0:
            raw = proc.stdout.decode("utf-8", errors="ignore")
            start = raw.find("<?xml")
            if start != -1:
                xml_text = raw[start:]
                local.write_text(xml_text, encoding="utf-8")
                return ET.parse(local).getroot(), local
            last_error = raw or last_error
        else:
            last_error = proc.stderr.decode("utf-8", errors="ignore") or last_error
        raise AdbError(f"Unable to capture UI dump after retries: {last_error}")


def parse_bounds(raw: str) -> tuple[int, int, int, int]:
    nums = list(map(int, re.findall(r"\d+", raw)))
    if len(nums) != 4:
        raise ValueError(f"Unexpected bounds: {raw}")
    return nums[0], nums[1], nums[2], nums[3]


def iter_nodes(root: ET.Element) -> Iterable[Node]:
    for elem in root.iter("node"):
        bounds_raw = elem.attrib.get("bounds")
        if not bounds_raw:
            continue
        yield Node(
            text=(elem.attrib.get("text") or "").strip(),
            desc=(elem.attrib.get("content-desc") or "").strip(),
            resource_id=(elem.attrib.get("resource-id") or "").strip(),
            clickable=elem.attrib.get("clickable") == "true",
            bounds=parse_bounds(bounds_raw),
        )


def normalize(value: str) -> str:
    return " ".join(value.lower().split())


def match_node(node: Node, token: str) -> bool:
    token = normalize(token)
    return token in normalize(node.text) or token in normalize(node.desc) or token == normalize(node.resource_id)


def find_node(root: ET.Element, *tokens: str, clickable_only: bool = False) -> Node | None:
    for node in iter_nodes(root):
        if clickable_only and not node.clickable:
            continue
        if any(match_node(node, token) for token in tokens):
            return node
    return None


def find_node_by_id(root: ET.Element, *resource_ids: str) -> Node | None:
    targets = set(resource_ids)
    for node in iter_nodes(root):
        if node.resource_id in targets:
            return node
    return None


def find_clickable_container(root: ET.Element, *tokens: str) -> Node | None:
    clickable_matches: list[Node] = []
    for node in iter_nodes(root):
        if not node.clickable:
            continue
        haystacks = [normalize(node.text), normalize(node.desc), normalize(node.resource_id)]
        if all(any(normalize(token) in hay for hay in haystacks) for token in tokens):
            clickable_matches.append(node)
    if clickable_matches:
        clickable_matches.sort(key=lambda n: (n.bounds[1], n.bounds[0]))
        return clickable_matches[0]
    return None


def any_text_present(root: ET.Element, *tokens: str) -> bool:
    return find_node(root, *tokens, clickable_only=False) is not None


def all_text_present(root: ET.Element, tokens: list[str]) -> bool:
    return all(any_text_present(root, token) for token in tokens)


def has_exact_label(root: ET.Element, label: str) -> bool:
    target = normalize(label)
    for node in iter_nodes(root):
        if normalize(node.text) == target or normalize(node.desc) == target:
            return True
    return False


def is_home_like_screen(root: ET.Element) -> bool:
    if any_text_present(root, "searching for flir meterlink devices", "can't connect flir meterlink device?"):
        return True
    return all(has_exact_label(root, label) for label in ("HOME", "FILES", "SETTINGS"))


def ocr_boxes(image_path: Path) -> list[OCRBox]:
    proc = subprocess.run(
        ["tesseract", str(image_path), "-", "tsv"],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise AdbError(proc.stderr or "tesseract failed")
    lines = proc.stdout.splitlines()
    if not lines:
        return []
    boxes: list[OCRBox] = []
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) != 12:
            continue
        text = parts[11].strip()
        if not text:
            continue
        try:
            conf = float(parts[10])
        except ValueError:
            conf = -1.0
        if conf < 0:
            continue
        boxes.append(
            OCRBox(
                text=text,
                left=int(parts[6]),
                top=int(parts[7]),
                width=int(parts[8]),
                height=int(parts[9]),
                confidence=conf,
            )
        )
    return boxes


def normalize_ocr_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def ocr_has_any_token(image_path: Path, *tokens: str) -> bool:
    boxes = ocr_boxes(image_path)
    flattened = "".join(normalize_ocr_token(box.text) for box in boxes)
    for token in tokens:
        if normalize_ocr_token(token) in flattened:
            return True
    return False


def ocr_has_all_tokens(image_path: Path, tokens: list[str]) -> bool:
    boxes = ocr_boxes(image_path)
    flattened = "".join(normalize_ocr_token(box.text) for box in boxes)
    return all(normalize_ocr_token(token) in flattened for token in tokens)


class SmokeRunner:
    def __init__(self, device: AdbDevice, pause: float = 1.0, mock_profile: MockProfile | None = None):
        self.device = device
        self.pause = pause
        self.mock_profile = mock_profile
        self.results: list[dict[str, str]] = []

    def log(self, message: str) -> None:
        print(message)

    def sleep(self, seconds: float | None = None) -> None:
        time.sleep(seconds if seconds is not None else self.pause)

    def snapshot(self, name: str) -> ET.Element:
        self.device.screenshot(name)
        root, _ = self.device.dump_ui(name)
        return root

    def wait_for(self, tokens: list[str], timeout: float = 12.0, name: str = "wait") -> ET.Element:
        deadline = time.time() + timeout
        while time.time() < deadline:
            root = self.snapshot(name)
            if any_text_present(root, *tokens):
                return root
            self.sleep(0.8)
        raise AssertionFailure(f"Timed out waiting for any of: {tokens}")

    def tap_token(self, root: ET.Element, *tokens: str) -> Node:
        node = find_node(root, *tokens, clickable_only=True) or find_node(root, *tokens, clickable_only=False)
        if node is None:
            raise AssertionFailure(f"Could not find tappable target for {tokens}")
        x, y = node.center
        self.device.tap(x, y)
        self.sleep()
        return node

    def tap_home_add(self, coords: tuple[int, int] = DEFAULT_HOME_ADD_BUTTON) -> None:
        self.device.tap(*coords)
        self.sleep(2.0)

    def tap_top_left_back(self, coords: tuple[int, int] = DEFAULT_TOP_LEFT_BACK_BUTTON) -> None:
        self.device.tap(*coords)
        self.sleep(1.5)

    def tap_container(self, root: ET.Element, *tokens: str) -> Node:
        node = find_clickable_container(root, *tokens)
        if node is None:
            raise AssertionFailure(f"Could not find clickable container for {tokens}")
        self.device.tap(*node.center)
        self.sleep()
        return node

    def snapshot_with_retries(self, name: str, attempts: int = 3, delay: float = 1.2) -> ET.Element:
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                return self.snapshot(name if attempt == 0 else f"{name}_{attempt+1}")
            except AdbError as exc:
                last_error = exc
                self.sleep(delay)
        raise AssertionFailure(f"Unable to capture UI snapshot for '{name}' after retries: {last_error}")

    def tap_home_device_by_label(self, device_name: str, sn_suffix: str | None = None) -> None:
        root = self.snapshot_with_retries("home_device_lookup")
        tokens = [device_name]
        if sn_suffix:
            tokens.append(sn_suffix)
        node = find_clickable_container(root, *tokens)
        if node is None:
            raise AssertionFailure(f"Could not locate a clickable Home card for {tokens}")
        self.device.tap(*node.center)
        self.sleep(2.0)

    def tap_home_device_by_ocr(self, device_name: str, sn_suffix: str | None = None) -> None:
        image_path = self.device.screenshot("home_device_ocr_lookup")
        boxes = ocr_boxes(image_path)

        def pick(token: str) -> OCRBox | None:
            target = normalize(token).replace("sn:", "").replace(" ", "")
            matches = []
            for box in boxes:
                text = normalize(box.text).replace("sn:", "").replace(" ", "")
                if target in text:
                    matches.append(box)
            if not matches:
                return None
            matches.sort(key=lambda b: (b.top, b.left))
            return matches[0]

        name_box = pick(device_name)
        if name_box is None:
            raise AssertionFailure(f"OCR could not find device name '{device_name}' on Home.")
        target_box = name_box
        if sn_suffix:
            sn_box = pick(sn_suffix)
            if sn_box is not None and abs(sn_box.top - name_box.top) < 200:
                target_box = OCRBox(
                    text=device_name,
                    left=min(name_box.left, sn_box.left),
                    top=min(name_box.top, sn_box.top),
                    width=max(name_box.left + name_box.width, sn_box.left + sn_box.width) - min(name_box.left, sn_box.left),
                    height=max(name_box.top + name_box.height, sn_box.top + sn_box.height) - min(name_box.top, sn_box.top),
                    confidence=min(name_box.confidence, sn_box.confidence),
                )

        tap_x = target_box.center[0]
        tap_y = target_box.center[1]
        self.device.tap(tap_x, tap_y)
        self.sleep(2.0)

    def tap_available_device_by_ocr(self, device_name: str) -> None:
        image_path = self.device.screenshot("available_device_ocr_lookup")
        boxes = ocr_boxes(image_path)
        target = normalize_ocr_token(device_name)
        matches = []
        for box in boxes:
            text = normalize_ocr_token(box.text)
            if target in text:
                matches.append(box)
        if not matches:
            raise AssertionFailure(f"OCR could not find available device '{device_name}'.")
        matches.sort(key=lambda b: (b.top, b.left))
        pick = matches[0]
        self.device.tap(*pick.center)
        self.sleep(2.0)

    def tap_ocr_token(self, screenshot_name: str, token: str) -> None:
        image_path = self.device.screenshot(screenshot_name)
        boxes = ocr_boxes(image_path)
        target = normalize_ocr_token(token)
        matches = []
        for box in boxes:
            text = normalize_ocr_token(box.text)
            if target in text:
                matches.append(box)
        if not matches:
            raise AssertionFailure(f"OCR could not find token '{token}'.")
        matches.sort(key=lambda b: (b.top, b.left))
        self.device.tap(*matches[0].center)
        self.sleep(1.5)

    def assert_ocr_tokens_present(self, image_path: Path, tokens: list[str], message: str) -> None:
        missing = [token for token in tokens if not ocr_has_any_token(image_path, token)]
        if missing:
            raise AssertionFailure(f"{message} Missing OCR tokens: {missing}")

    def ensure_home_before_mock_entry(self, profile: dict) -> Path:
        list_title = profile.get("list_title", "Available devices")

        probe = self.device.screenshot("mock_entry_probe")
        if ocr_has_any_token(probe, list_title):
            self.tap_top_left_back()
            self.sleep(1.0)
            probe = self.device.screenshot("mock_entry_home_probe")

        if ocr_has_any_token(probe, list_title):
            self.tap_top_left_back()
            self.sleep(1.0)
            probe = self.device.screenshot("mock_entry_home_probe_recovered")

        if ocr_has_any_token(probe, list_title):
            raise AssertionFailure("Expected to recover to HOME before enabling mock BLE.")
        return probe

    def enable_mock_ble_from_home(self, profile: dict, add_button: dict | None = None) -> Path:
        home_tab_token = profile.get("home_tab_token", "HOME")
        list_title = profile.get("list_title", "Available devices")
        mock_enable_taps = int(profile.get("mock_enable_taps", 10))
        mock_logo_tap = profile.get("mock_logo_tap")
        mock_ble_toggle_tap = profile.get("mock_ble_toggle_tap")
        mock_close_token = profile.get("mock_close_token", "Close")
        mock_close_tap = profile.get("mock_close_tap")
        close_after_mock_wait_seconds = float(profile.get("close_after_mock_wait_seconds", 4.0))

        self.ensure_home_before_mock_entry(profile)

        if not isinstance(mock_logo_tap, dict):
            raise AssertionFailure("Mock logo tap coordinates are required in the mock profile.")
        for _ in range(mock_enable_taps):
            self.device.tap(int(mock_logo_tap["x"]), int(mock_logo_tap["y"]))
            self.sleep(0.18)

        self.sleep(2.0)  # Wait for ripple effects or Toast to fade out before UI dump
        debug_root = self.snapshot_with_retries("mock_entry_debug")
        if isinstance(mock_ble_toggle_tap, dict):
            self.device.tap(int(mock_ble_toggle_tap["x"]), int(mock_ble_toggle_tap["y"]))
            self.sleep(0.5)
        else:
            self.tap_token(debug_root, "Mockup Ble")
        try:
            self.tap_token(debug_root, mock_close_token)
        except AssertionFailure:
            if isinstance(mock_close_tap, dict):
                self.device.tap(int(mock_close_tap["x"]), int(mock_close_tap["y"]))
                self.sleep(1.5)
            else:
                self.tap_ocr_token("mock_entry_close_lookup", mock_close_token)
        self.sleep(close_after_mock_wait_seconds)

        post_mock_probe = self.device.screenshot("mock_entry_post_mock")
        if ocr_has_any_token(post_mock_probe, list_title):
            return post_mock_probe
        if ocr_has_any_token(post_mock_probe, home_tab_token):
            if isinstance(add_button, dict):
                self.tap_home_add((int(add_button["x"]), int(add_button["y"])))
            else:
                self.tap_home_add()
            return self.device.screenshot("mock_entry_list_after_home")
        raise AssertionFailure("After enabling Mockup Ble, app was not on HOME or Available devices.")

    def ensure_mock_device_added(self, profile: dict) -> None:
        target_device = profile.get("available_device_name", profile["device_name"])
        required_home_tokens = list(profile.get("required_home_tokens", []))
        add_button = profile.get("add_button")
        device_card_tap = profile.get("device_card_tap")

        home_probe = self.ensure_home_before_mock_entry(profile)
        if required_home_tokens and ocr_has_all_tokens(home_probe, required_home_tokens):
            return
        home_tab_token = profile.get("home_tab_token", "HOME")

        if isinstance(add_button, dict):
            self.tap_home_add((int(add_button["x"]), int(add_button["y"])))
        else:
            self.tap_home_add()

        self.device.screenshot("mock_device_presence_list")
        try:
            self.tap_available_device_by_ocr(target_device)
        except AssertionFailure:
            self.tap_top_left_back()
            home_recovered_probe = self.ensure_home_before_mock_entry(profile)
            if ocr_has_any_token(home_recovered_probe, profile.get("list_title", "Available devices")):
                raise AssertionFailure("Expected to recover back to HOME before enabling mock BLE.")
            self.enable_mock_ble_from_home(profile, add_button if isinstance(add_button, dict) else None)
            try:
                self.tap_available_device_by_ocr(target_device)
            except AssertionFailure:
                if isinstance(device_card_tap, dict):
                    self.device.tap(int(device_card_tap["x"]), int(device_card_tap["y"]))
                    self.sleep(2.0)
                else:
                    raise

        rename_root = self.snapshot("mock_device_presence_rename")
        if not any_text_present(rename_root, "Rename", target_device):
            raise AssertionFailure(f"Expected Rename screen for {target_device} after tapping the mock device.")
        self.tap_token(rename_root, profile.get("skip_token", "Skip"))
        self.sleep(2.5)
        if required_home_tokens:
            home_probe = self.device.screenshot("mock_device_presence_home")
            if not ocr_has_all_tokens(home_probe, required_home_tokens):
                raise AssertionFailure("Mock device was not visible on HOME after add flow.")

    def record(self, case_id: str, status: str, detail: str) -> None:
        self.results.append({"case_id": case_id, "status": status, "detail": detail})

    def require_mock_profile(self) -> MockProfile:
        if self.mock_profile is None:
            raise AssertionFailure("This case requires --mock-profile.")
        return self.mock_profile

    def assert_tokens_present(self, root: ET.Element, tokens: list[str], message: str) -> None:
        missing = [token for token in tokens if not any_text_present(root, token)]
        if missing:
            raise AssertionFailure(f"{message} Missing tokens: {missing}")

    def write_results(self) -> Path:
        out = self.device.work_dir / "results.json"
        out.write_text(json.dumps(self.results, indent=2), encoding="utf-8")
        return out

    def launch_fresh(self) -> ET.Element:
        self.device.force_stop()
        self.device.clear_app()
        self.device.launch()
        self.sleep(2.0)
        return self.snapshot("fresh_launch")

    def continue_intro_permission(self, root: ET.Element, action: str) -> ET.Element:
        if any_text_present(root, "location permission"):
            self.tap_token(root, "continue" if action == "allow" else "decline")
            return self.snapshot(f"in_app_permission_{action}")
        return root

    def handle_system_permission(self, root: ET.Element, action: str) -> ET.Element:
        if not any("permissioncontroller" in node.resource_id for node in iter_nodes(root)):
            return root
        allow_id_order = [
            "com.android.permissioncontroller:id/permission_allow_all_button",
            "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            "com.android.permissioncontroller:id/permission_allow_button",
            "com.android.permissioncontroller:id/permission_allow_selected_button",
        ]
        deny_id_order = [
            "com.android.permissioncontroller:id/permission_deny_button",
            "com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button",
        ]
        node = None
        if action == "allow":
            for rid in allow_id_order:
                node = find_node_by_id(root, rid)
                if node:
                    break
            if node is None:
                node = find_node(root, "全部允許", "允許", "allow", "while using the app", clickable_only=True)
        else:
            for rid in deny_id_order:
                node = find_node_by_id(root, rid)
                if node:
                    break
            if node is None:
                node = find_node(root, "不允許", "don't allow", "deny", clickable_only=True)
        if node is None:
            raise AssertionFailure("Could not find a system permission action button.")
        x, y = node.center
        self.device.tap(x, y)
        self.sleep()
        return self.snapshot(f"system_permission_{action}")

    def dismiss_optional_dialogs(self, root: ET.Element) -> ET.Element:
        dismiss_tokens = ["close", "ok", "not now", "skip", "cancel", "稍後", "關閉", "確定"]
        for token in dismiss_tokens:
            node = find_node(root, token, clickable_only=True)
            if node:
                self.tap_token(root, token)
                return self.snapshot(f"dismiss_{normalize(token)}")
        return root

    def advance_tutorial_until_home(self, root: ET.Element, max_steps: int = 8) -> ET.Element:
        for _ in range(max_steps):
            if is_home_like_screen(root):
                return root
            next_node = find_node(root, "next", "get started", clickable_only=True)
            if next_node is None:
                return root
            self.tap_token(root, "next", "get started")
            root = self.snapshot("tutorial_step")
            root = self.dismiss_optional_dialogs(root)
        return root

    def go_to_home_search(self, permission_action: str) -> ET.Element:
        root = self.launch_fresh()
        for _ in range(6):
            before = ET.tostring(root, encoding="unicode")
            root = self.continue_intro_permission(root, permission_action)
            root = self.handle_system_permission(root, permission_action)
            root = self.dismiss_optional_dialogs(root)
            after = ET.tostring(root, encoding="unicode")
            if before == after:
                break
        root = self.dismiss_optional_dialogs(root)
        root = self.advance_tutorial_until_home(root)
        return root
