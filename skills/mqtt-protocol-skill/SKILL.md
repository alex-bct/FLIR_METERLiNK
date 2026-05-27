---
name: mqtt-protocol-skill
description: Comprehensive guide for MQTT protocol validation, troubleshooting, and SV95-specific configuration rules. Use this skill when working with MQTT settings, connection testing logic, or port/passcode validation requirements.
---

# MQTT Protocol & SV95 Configuration Skill

Procedural guidance for validating and troubleshooting MQTT and related device settings for the SV95 project.

## 0. What is MQTT? (A Simple Introduction)

**MQTT** (Message Queuing Telemetry Transport) is a lightweight messaging protocol designed for IoT (Internet of Things) devices with limited bandwidth or unreliable connections.

Think of it as a **"Bulletin Board System"**:
-   **Publisher (The SV95 Device)**: "Posts" measurement data to a specific **Topic** (e.g., `factory/pump1/vibration`).
-   **Broker (The Server)**: The "Board Manager" who receives messages and ensures they reach the right people.
-   **Subscriber (The App or PC)**: Anyone who "Follows" a topic. Whenever a new post appears, they get notified immediately.

Unlike Bluetooth, which requires a direct "face-to-face" connection, MQTT allows the SV95 to send data to the office from across the factory (or the world) via Wi-Fi.

## 1. Core MQTT Validation Rules

When implementing or testing MQTT configuration screens, adhere to these strict limits:

- **MQTT Port Range**: Must be within **1 - 65535**.
  - Validation: Block 0 or values > 65535.
- **MQTT Test Button Behavior**:
  - Implement a **cooldown period** (e.g., 5-10 seconds) after a tap to prevent spamming the broker.
  - UI should indicate a "Testing..." state during the process.
- **Broker/Topic Naming**:
  - Topics should follow the hierarchical structure: `[Company]/[AssetID]/[DataPoint]`.
  - Avoid special characters except `/`, `-`, and `_`.

## 2. Device Security & Passcode

SV95 supports local passcode protection for configuration access:

- **Length**: Strictly **6 - 8 characters**.
- **Type**: **Alphanumeric** only (A-Z, a-z, 0-9).
- **Validation**: Block any input outside the 6-8 length range or containing non-alphanumeric symbols.

## 3. MQTT vs. BLE Usage Scenarios

| Feature | Bluetooth Low Energy (BLE) | MQTT (Wi-Fi) |
| :--- | :--- | :--- |
| **Range** | Short (~10m) | Unlimited (via Internet) |
| **Dependence** | Requires App in foreground | Independent (Device-to-Broker) |
| **Best For** | Initial Setup, Real-time debugging | Long-term monitoring, Automation |
| **Sync** | Point-to-point | Multi-client subscription |

## 4. Troubleshooting Workflow

If an MQTT connection fails:

1.  **Network Check**: Verify the SV95 is connected to a Wi-Fi network with internet access.
2.  **Credential Check**: Re-verify the Username/Password and Client ID.
3.  **Port/Firewall**: Ensure the target Port (usually 1883 or 8883 for SSL) is open on the industrial network.
4.  **Broker Logs**: Check the MQTT Broker logs for "Unauthorized" or "Socket Closed" errors.

## 5. Automated Testing Tips

- **Validation Testing**: Always test boundary values (Port 1, 65535, 0, 65536).
- **Interruption Testing**: Force disconnect Wi-Fi during a "Test Connection" sequence to ensure the App handles the timeout gracefully.
