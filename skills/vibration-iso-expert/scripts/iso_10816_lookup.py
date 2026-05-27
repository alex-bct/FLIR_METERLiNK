import sys

def get_status_fm1313(machine_type, foundation, value, unit="mm/s"):
    # Updated thresholds from Confluence page 4020273173
    thresholds = {
        "large": {
            "rigid": {"mm": [4.5, 7.1], "inch": [0.18, 0.28]},
            "flexible": {"mm": [7.1, 11.0], "inch": [0.28, 0.43]}
        },
        "medium": {
            "rigid": {"mm": [2.8, 4.5], "inch": [0.11, 0.18]},
            "flexible": {"mm": [4.5, 7.1], "inch": [0.18, 0.28]}
        },
        "small": {
            "rigid": {"mm": [1.8, 4.5], "inch": [0.071, 0.18]}, # Inch values approximated if not in spec
            "flexible": {"mm": [1.8, 4.5], "inch": [0.071, 0.18]}
        }
    }
    
    m = machine_type.lower()
    f = foundation.lower()
    u = unit.lower()
    
    if m not in thresholds:
        return f"Unknown Machine Type: {m}"
    
    # Fallback to rigid if flexible not specified for small
    target_f = f if f in thresholds[m] else "rigid"
    
    key = "mm" if u == "mm/s" else "inch"
    t = thresholds[m][target_f][key]
    
    status = ""
    if value < t[0]:
        status = "Normal - WHITE"
    elif value < t[1]:
        status = "Alert - ORANGE"
    else:
        status = "Danger - RED"
        
    return {
        "status": status,
        "input": f"{value} {unit}",
        "machine": f"{m}/{target_f}",
        "thresholds": {"alert": t[0], "danger": t[1]}
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 iso_10816_lookup.py <large|medium|small> <rigid|flexible> <value> [unit: mm/s|inch/s]")
        sys.exit(1)
    
    machine_type = sys.argv[1]
    foundation = sys.argv[2]
    value = float(sys.argv[3])
    unit = sys.argv[4] if len(sys.argv) > 4 else "mm/s"
    
    res = get_status_fm1313(machine_type, foundation, value, unit)
    if isinstance(res, str):
        print(res)
    else:
        print(f"--- SV95 Vibration Evaluation (Spec 4020273173) ---")
        print(f"Machine: {res['machine'].upper()}")
        print(f"Input: {res['input']}")
        print(f"Status: {res['status']}")
        print(f"Thresholds applied: Alert {res['thresholds']['alert']} / Danger {res['thresholds']['danger']}")
