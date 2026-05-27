# FLIR MeterLiNK Mock Case Mapping

Source: [FLIR_QA_TCs_METERLiNK.xlsx](/Users/alex/Documents/Project/FLIR_METERLiNK/FLIR_QA_TCs_METERLiNK.xlsx)

This mapping separates the existing spreadsheet cases into three buckets:

- `Mock-ready`: can validate UI and flows with dev-tool injected devices/data
- `Mock-partial`: can validate most UI with mock data, but still leaves a real-device/system edge
- `Real-device`: depends on Bluetooth behavior, live data timing, firmware/device state, or actual transfers

## First 10 Mock Cases To Build

- Row 22: `Home - Device Connection / Device disconnect`
- Row 36: `Home - Device Card / Alert - Device disconnected`
- Row 49: `Device Detail / Device details component without connecting`
- Row 54: `Device Detail / Check device detail - Device reconnected`
- Row 110: `Settings / Dark mode`
- Row 115: `Settings / App version information`
- Row 118: `General / App language is English`
- Row 144: `Device Detail -Report / Report preview with live meter`
- Row 181: `File - Gallery / Empty page`
- Row 199: `File - Log / Browse log list`

## Mock-ready

These are good candidates for mock-device coverage because they mostly assert visible UI state rather than physical Bluetooth behavior.

### OOBE / Permissions / Settings

- Row 9: `Allow Android location permission`
- Row 10: `Denying Android location permission`
- Row 11: `Tutorial progress in OOBE`
- Row 12: `Interruption when in tutorial progress`
- Row 15: `Can't connect?`
- Row 80: `Ask for notification permission - Allow`
- Row 81: `Ask for notification permission - Don't Allow`
- Row 110: `Dark mode`
- Row 111: `Light mode`
- Row 112: `Support - Manual`
- Row 113: `Support - FLIR support`
- Row 114: `Support - FLIR`
- Row 115: `App version information`
- Row 116: `App UI Appearance mode default is dark`
- Row 117: `System display Appearance won't impact App Appearance`
- Row 118: `App language is English`
- Row 119: `Landscape UI check`

### Home / Device Card / Main

- Row 22: `Device disconnect`
- Row 23: `Add removed device`
- Row 25: `Reconnect to device between two phones`
- Row 26: `Remove device and keep the measurement data`
- Row 27: `Remove device and erase the measurement data`
- Row 30: `Up to max connected devices`
- Row 36: `Alert - Device disconnected`
- Row 43: `Switch the unit`
- Row 45: `Switch the MAX/ MIN/ AVG/ Hold function`

### Device Detail / More / Report

- Row 49: `Device details component without connecting`
- Row 50: `Device support capture function`
- Row 51: `Device support IGM to measure center spot temperature`
- Row 52: `Device support capture to capture device screen`
- Row 53: `Device support capture to capture device screen fail`
- Row 54: `Check device detail - Device reconnected`
- Row 57: `Turn on test device BT and reconnect`
- Row 58: `Turn off test device BT and reconnect`
- Row 75: `Check unit limation of test device`
- Row 76: `Switch test device unit under device detail page`
- Row 77: `Switch the MAX/ MIN/ AVG/ Hold function under device detail page`
- Row 122: `Change device name`
- Row 123: `Interrupt rename`
- Row 124: `Rename device name with special character`
- Row 125: `Change device name when disconnected`
- Row 132: `Add device information - add photo`
- Row 133: `Add device information - remove photo`
- Row 134: `Add device information - add over 3 photos`
- Row 135: `Add device information - add location info`
- Row 136: `Add device information - add description`
- Row 137: `Remove device -- keep the data`
- Row 138: `Remove device -- erase the data`
- Row 139: `Remove device -- no record data`
- Row 143: `Cancel remove device during ask user keep the data`
- Row 144: `Report preview with live meter`
- Row 145: `Report preview without live meter`
- Row 146: `Report preview - with device name changed`
- Row 147: `Add Page header logo - Export via email`
- Row 148: `Add Location - Export via email`
- Row 149: `Add Summary - Export via email`
- Row 150: `Add Image - Export via email`
- Row 151: `Add Notes - Export via email`
- Row 152: `Add measurement log - Export via email`
- Row 153: `Add gallery - Export via email`
- Row 154: `Share report via iOS AirDrop`
- Row 155: `Share report via Android NearBy`
- Row 157: `Remove Page header logo`
- Row 158: `Remove Images`
- Row 160: `Remove gallery`
- Row 161: `Cancel to export`

### Files / Gallery / Logs

- Row 181: `Empty page`
- Row 182: `Browse images`
- Row 183: `Sort by Newest to Oldest`
- Row 184: `Sort by Oldest to Newest`
- Row 185: `Long press to active edit mode`
- Row 186: `Cancel active edit mode`
- Row 187: `Select one image to remove`
- Row 188: `Select one video to remove`
- Row 189: `Select images to remove`
- Row 190: `Select videos to remove`
- Row 191: `Select image and video to remove`
- Row 192: `Unselect images or videos`
- Row 193: `Select 5 images or up to share`
- Row 194: `Select 5 images and 1 video to share`
- Row 195: `Select one image to share as image`
- Row 196: `Select one image to share as PDF`
- Row 197: `Select 4 images to share as PDF`
- Row 198: `Empty page`
- Row 199: `Browse log list`
- Row 200: `Sort by Newest to Oldest`
- Row 201: `Sort by Oldest to Newest`
- Row 202: `Long press to active edit mode`
- Row 203: `Cancel active edit mode`
- Row 204: `Remove single log`
- Row 205: `Select multiple logs to remove`
- Row 206: `Unselect logs`
- Row 207: `Select logs`
- Row 208: `Switch controller in edit mode`

## Mock-partial

These can mostly be covered by mock data, but still have at least one remaining dependency on system behavior, permissions, or share targets that may need separate verification.

- Row 2: `Splash screen on Phone`
- Row 3: `Splash screen on Pad/Tablet`
- Row 14: `Start to search devices but no device found`
- Row 37: `Alert priority`
- Row 47: `Device details component with connecting`
- Row 48: `Function card component`
- Row 155: `Share report via Android NearBy`
- Row 162: `Observe the battery comsumption in 1 hour - Background and suspend`

## Real-device

These should stay in the real-device bucket because they validate Bluetooth scanning, pairing, recording, disconnect timing, live battery states, firmware updates, file transfer, or hardware-originated notifications.

- Rows 4-8: Bluetooth permission and system Bluetooth flows
- Rows 13, 16-21, 24: scan/add/connect flows
- Rows 28-29, 31-42, 44, 46: recording and live card behavior
- Rows 55-79 except the mock-ready detail cases above
- Rows 82-109: device-originated notifications and alarm state
- Rows 120-121, 126-131, 140-142, 156, 159, 163-180

## Suggested Next Step

Build the first mock set around stable, high-value UI surfaces:

1. Home disconnected device state
2. Device detail without connection
3. Device reconnected state
4. Report preview with live meter
5. Gallery empty page
6. Log list browse page
