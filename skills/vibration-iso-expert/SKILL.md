---
name: vibration-iso-expert
description: Evaluate vibration levels based on SV95 Spec 4020273173. Supports Large, Medium, and Small machines with exact UI threshold mappings for mm/s and inch/s.
---

# Vibration ISO Expert (SV95 Full Spec)

Validates vibration severity logic for SV95 using thresholds from the latest specification table.

## Threshold Mapping

| Machine Type | Foundation | Alert (mm/s) | Danger (mm/s) | Alert (inch/s) | Danger (inch/s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Large** | Rigid | 4.5 | 7.1 | 0.18 | 0.28 |
| **Large** | Flexible | 7.1 | 11.0 | 0.28 | 0.43 |
| **Medium** | Rigid | 2.8 | 4.5 | 0.11 | 0.18 |
| **Medium** | Flexible | 4.5 | 7.1 | 0.18 | 0.28 |
| **Small** | Rigid/Flex | 1.8 | 4.5 | 0.07 | 0.18 |

## Workflow
1. Identify machine type, foundation, and unit.
2. Run: `python3 skills/vibration-iso-expert/scripts/iso_10816_lookup.py <large|medium|small> <rigid|flexible> <value> <mm/s|inch/s>`
