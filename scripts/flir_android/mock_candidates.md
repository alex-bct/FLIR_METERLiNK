# FLIR MeterLiNK Mock-Friendly Android Cases

These are the next cases worth adding now that dev tools can expose mocked device data. The goal is to move more of the Excel coverage into stable UI smoke coverage without waiting for real Bluetooth hardware.

## Best First Mock Cases

### Home / Device List

- `MOCK-01`: Home with zero devices
- `MOCK-02`: Home with one connected device card
- `MOCK-03`: Home with multiple devices
- `MOCK-04`: Home with disconnected device
- `MOCK-05`: Home with low-battery device

### Device Detail

- `MOCK-06`: Device detail with measurements
- `MOCK-07`: Device detail with no history
- `MOCK-08`: Device detail with alarm enabled
- `MOCK-09`: Device detail in loading state

### Files / Gallery / Logs

- `MOCK-10`: Files page empty state
- `MOCK-11`: Mixed image/video/log results
- `MOCK-12`: Large file list

### Notifications / Settings

- `MOCK-13`: Notification center entry for low battery
- `MOCK-14`: Notification center entry for disconnect
- `MOCK-15`: Settings screen with all toggles on

## Suggested Next 5 To Build

1. `MOCK-01` Home with zero devices
2. `MOCK-02` Home with one connected device card
3. `MOCK-04` Home with disconnected device
4. `MOCK-06` Device detail with measurements
5. `MOCK-10` Files page empty state

## Implemented So Far

- `MOCK-04` style add-device baseline:
  `Available devices -> tap mock device -> Skip -> verify Home card`
