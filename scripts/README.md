# FLIR Android Smoke Scripts

CLI entrypoint: [flir_android_smoke.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android_smoke.py)

Case package: [flir_android](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android)

## Purpose

This automation now uses a shared runner plus one file per case. It currently focuses on the most annoying Android first-launch checks for FLIR MeterLiNK:

- app data reset
- launch/OOBE
- in-app permission explainer dialogs
- Android runtime permission dialogs
- tutorial progression
- scan page and `Can't connect?` help flow

## Requirements

- `adb` available in `PATH`
- Android device connected by USB
- FLIR MeterLiNK installed on device

## Run

```bash
python3 scripts/flir_android_smoke.py --case oobe-suite
```

If more than one Android device is connected:

```bash
python3 scripts/flir_android_smoke.py --serial <device-serial> --case oobe-suite
```

## Current Cases

- `oobe-allow` -> [oobe_allow.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/oobe_allow.py)
- `oobe-deny` -> [oobe_deny.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/oobe_deny.py)
- `search-no-device` -> [search_no_device.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/search_no_device.py)
- `cant-connect` -> [cant_connect.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/cant_connect.py)
- `mock-home-disconnected` -> [mock_home_disconnected.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/mock_home_disconnected.py)
- `mock-device-detail-disconnected` -> [mock_device_detail_disconnected.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/mock_device_detail_disconnected.py)
- `mock-gallery-empty` -> [mock_gallery_empty.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/mock_gallery_empty.py)
- `mock-add-device-default-name` -> [mock_add_device_default_name.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/mock_add_device_default_name.py)
- `mock-delete-device-card` -> [mock_delete_device_card.py](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/cases/mock_delete_device_card.py)

Run a single case:

```bash
python3 scripts/flir_android_smoke.py --case cant-connect
python3 scripts/flir_android_smoke.py --case oobe-allow
python3 scripts/flir_android_smoke.py --case oobe-deny
python3 scripts/flir_android_smoke.py --case search-no-device
```

Run the first mock cases after injecting data with dev tool:

```bash
cp scripts/flir_android/mock_profile.example.json scripts/flir_android/mock_profile.json
python3 scripts/flir_android_smoke.py --case mock-suite --mock-profile scripts/flir_android/mock_profile.json
```

Or run one mock case:

```bash
python3 scripts/flir_android_smoke.py --case mock-home-disconnected --mock-profile scripts/flir_android/mock_profile.json
```

## Artifacts

Default output directory:

```text
artifacts/android_smoke
```

Each run writes:

- screenshots
- UI dump XML files
- `results.json`

## Mock Expansion

Mock-friendly backlog: [mock_candidates.md](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/mock_candidates.md)

Mock profile template: [mock_profile.example.json](/Users/alex/Documents/Project/FLIR_METERLiNK/scripts/flir_android/mock_profile.example.json)

## Notes

- The script uses `pm clear` to recreate first-launch behavior.
- `Can't connect?` close is handled with a top-left tap fallback because some builds expose it as an icon without text.
- This suite is still intentionally limited to flows that do not require a physical meter.
- When mock data setup is ready, the next cases should also live one-per-file under `scripts/flir_android/cases/`.
- For mock Home cards, the preferred selector strategy is `device_name + serial suffix -> clickable container`, with manual tap coordinates only as a temporary fallback when the Home chart animation prevents reliable UI dumps.
