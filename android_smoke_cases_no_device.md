# FLIR MeterLiNK Android Smoke Cases Without Physical BT Device

Source: `FLIR_QA_TCs_METERLiNK.xlsx` -> `Test Case`

This suite keeps only Android smoke cases that can be executed without pairing to a real FLIR/Extech Bluetooth meter. It is intended for fast launch validation, permission behavior, basic navigation, and support/settings checks.

## Scope

- Target app: `com.flir.METERLiNKAPP.beta`
- Device class: Android phone
- Excluded: cases that require a connected meter, live Bluetooth data, file transfer from device, or alarm/notification events triggered by hardware state

## Recommended Smoke Suite

| Smoke ID | Source Row | Priority | Area | Title | Needs Fresh Install | Needs External Device | Suggested Mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SMK-01` | 2 | P1 | OOBE | Splash screen on Phone | Yes | No | Auto |
| `SMK-02` | 9 | P1 | OOBE | Allow Android location permission | Yes | No | Semi-auto |
| `SMK-03` | 10 | P2 | OOBE | Denying Android location permission | Yes | No | Semi-auto |
| `SMK-04` | 11 | Unset | OOBE | Tutorial progress in OOBE | Yes | No | Auto |
| `SMK-05` | 12 | Unset | OOBE | Interruption when in tutorial progress | Yes | No | Semi-auto |
| `SMK-06` | 14 | P2 | Home - Device Connection | Start to search devices but no device found | No | No | Auto |
| `SMK-07` | 15 | P1 | Home - Device Connection | Can't connect? | No | No | Auto |
| `SMK-08` | 20 | P2 | Home | Add device when bluetooth is disable | No | No | Semi-auto |
| `SMK-09` | 110 | P1 | Settings | Dark mode | No | No | Auto |
| `SMK-10` | 111 | P1 | Settings | Light mode | No | No | Auto |
| `SMK-11` | 112 | P1 | Settings | Support - Manual | No | No | Semi-auto |
| `SMK-12` | 113 | P1 | Settings | Support - FLIR support | No | No | Semi-auto |
| `SMK-13` | 114 | P1 | Settings | Support - FLIR | No | No | Semi-auto |
| `SMK-14` | 115 | P1 | Settings | App version information | No | No | Auto |
| `SMK-15` | 118 | P2 | General | App language is English | No | No | Auto |

## Case Details

### `SMK-01` Splash screen on Phone

- Source row: `2`
- Precondition: brand-new install or cold launch
- Steps:
  1. Launch FLIR MeterLiNK
  2. Observe splash screen
- Expected:
  1. FLIR splash screen displays correctly
  2. App transitions into the next app flow without crash

### `SMK-02` Allow Android location permission

- Source row: `9`
- Precondition: fresh install on Android
- Steps:
  1. Launch app
  2. Allow Android location permission
  3. Change permission to `Allow all the time` if app routes user to settings
- Expected:
  1. App informs user if background location is still needed
  2. User can continue toward the scan/home flow after permission is handled

### `SMK-03` Denying Android location permission

- Source row: `10`
- Precondition: fresh install on Android
- Steps:
  1. Launch app
  2. Deny location permission
  3. Relaunch app
  4. Open settings from the prompt and enable permission
- Expected:
  1. Home/scan page shows a clear permission guidance message
  2. App recovers after permission is enabled

### `SMK-04` Tutorial progress in OOBE

- Source row: `11`
- Precondition: fresh install
- Steps:
  1. Launch app
  2. Tap `Next` until OOBE completes
- Expected:
  1. Tutorial finishes successfully
  2. App lands on Home

### `SMK-05` Interruption when in tutorial progress

- Source row: `12`
- Precondition: fresh install
- Steps:
  1. Launch app
  2. Advance tutorial to `Get started`
  3. Send app to background
  4. Return app to foreground
- Expected:
  1. Tutorial stays on the same step
  2. User can continue and finish tutorial

### `SMK-06` Start to search devices but no device found

- Source row: `14`
- Precondition: no discoverable FLIR meter nearby
- Steps:
  1. Launch app with required permission already granted
- Expected:
  1. App remains on search screen
  2. Empty-state guidance is visible
  3. Guidance tells user to check Bluetooth on both meter and phone

### `SMK-07` Can't connect?

- Source row: `15`
- Precondition: app is on device search screen
- Steps:
  1. Tap `Can't connect Flir Meterlink device?`
  2. Verify help/instruction page
  3. Tap in-app `X`
- Expected:
  1. Help page opens
  2. User can exit back to the search screen

### `SMK-08` Add device when bluetooth is disable

- Source row: `20`
- Precondition: system Bluetooth is off
- Steps:
  1. From Home, tap add/connect device
- Expected:
  1. App prompts the user to turn on Bluetooth before continuing

### `SMK-09` Dark mode

- Source row: `110`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
  2. Enable dark mode
- Expected:
  1. App UI changes to dark theme

### `SMK-10` Light mode

- Source row: `111`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
  2. Disable dark mode
- Expected:
  1. App UI changes to light theme

### `SMK-11` Support - Manual

- Source row: `112`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
  2. Tap `Manual`
- Expected:
  1. Browser or file viewer opens the manual resource

### `SMK-12` Support - FLIR support

- Source row: `113`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
  2. Tap `FLIR support`
- Expected:
  1. Browser opens the support link

### `SMK-13` Support - FLIR

- Source row: `114`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
  2. Tap `FLIR`
- Expected:
  1. Browser opens the FLIR link

### `SMK-14` App version information

- Source row: `115`
- Precondition: app can reach Settings
- Steps:
  1. Open Settings
- Expected:
  1. App version is displayed
  2. Version format follows release rule

### `SMK-15` App language is English

- Source row: `118`
- Precondition:
  1. Android system language is Traditional Chinese
- Steps:
  1. Launch app
  2. Go to Settings
- Expected:
  1. App strings remain in English

## Execution Notes

- `Auto`: suitable for `adb` or UIAutomator-driven smoke execution
- `Semi-auto`: likely needs install reset, permission state reset, app switch, or external intent verification
- Cases using first-launch permission dialogs are easiest to run after uninstall/reinstall or app data reset
- Cases that open browser/manual links should verify the handoff intent and top-level destination only

## Current Validation Status

Validated on connected Android device:

- `SMK-06`: search screen/empty-state flow reproduced successfully
- `SMK-07`: help page opened successfully and returned to search screen via in-app `X`

Observed during exploratory run:

- Selecting `Connect to VS80` can route to a Wi-Fi onboarding flow and trigger a precise location prompt
- Android system `Back` is not equivalent to the in-app `X` on the `Can't connect?` page

## Suggested Next Build Order

1. Automate `SMK-06`, `SMK-07`, `SMK-09`, `SMK-10`, `SMK-14`, `SMK-15`
2. Add reinstall/data-reset support for `SMK-01` to `SMK-05`
3. Add permission-state helpers for `SMK-02`, `SMK-03`, `SMK-08`
