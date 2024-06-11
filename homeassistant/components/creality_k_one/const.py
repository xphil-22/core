"""Constants for the Creality K1 integration."""

DOMAIN = "creality_k_one"

LIGHTS = [{"id": "lightSw", "friendly_name": "Light Switch"}]

SENSOR_NAMES = [
    {"id": "bedTemp0", "friendly_name": "Bed Temperature 0"},
    {"id": "nozzleTemp", "friendly_name": "Nozzle Temperature"},
]

# "fanCase": 1, "caseFanPct": 100 back fan
# "fan": 0, "modelFanPct": 0 Model
# "fanAuxiliary": 0, "auxiliaryFanPct": 0
