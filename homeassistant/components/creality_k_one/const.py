"""Constants for the Creality K1 integration."""

from homeassistant.components.button import ButtonDeviceClass

DOMAIN = "creality_k_one"

LIGHTS = [{"id": "lightSw", "friendly_name": "Light Switch"}]

SWITCHES = [
    {"id": "aiSw", "friendly_name": "aiSw"},
]

SENSORS = [
    {"id": "bedTemp0", "friendly_name": "Hot Bed Temperature"},
    {"id": "nozzleTemp", "friendly_name": "Nozzle Temperature"},
    {"id": "boxTemp", "friendly_name": "Box Temperature"},
    {"id": "cornerVelocityLimits", "friendly_name": "cornerVelocityLimits"},
    {"id": "curPosition", "friendly_name": "Current Position"},
    {"id": "hostname", "friendly_name": "Hostname"},
    {"id": "layer", "friendly_name": "Layer"},
    {"id": "maxBedTemp", "friendly_name": "Maximum Bed Temperature"},
    {"id": "maxNozzleTemp", "friendly_name": "Maximum Nozzle Temperature"},
    {"id": "modelVersion", "friendly_name": "Model Version"},
    {"id": "printId", "friendly_name": "autohome"},
    {"id": "printFileName", "friendly_name": "Print file Name"},
    {"id": "printJobTime", "friendly_name": "printJobTime"},
    {"id": "printLeftTime", "friendly_name": "printLeftTime"},
    {"id": "printProgress", "friendly_name": "printProgress"},
    {"id": "printStartTime", "friendly_name": "printStartTime"},
    {"id": "realTimeFlow", "friendly_name": "realTimeFlow"},
    {"id": "realTimeSpeed", "friendly_name": "realTimeSpeed"},
    {"id": "targetBedTemp0", "friendly_name": "Target Bed Temperature"},
    {"id": "targetNozzleTemp", "friendly_name": "targetNozzleTemp"},
    {"id": "usedMaterialLength", "friendly_name": "usedMaterialLength"},
    {"id": "velocityLimits", "friendly_name": "velocityLimits"},
    {"id": "autohome", "friendly_name": "autohome"},
    {"id": "state", "friendly_name": "state"},
]

BINARY_SENSORS = [
    {"id": "aiDetection", "friendly_name": "aiDetection"},
    {"id": "aiPausePrint", "friendly_name": "aiDetection"},
    {"id": "enableSelfTest", "friendly_name": "enableSelfTest"},
    {"id": "materialDetect", "friendly_name": "materialDetect"},
    {"id": "repoPlrStatus", "friendly_name": "repoPlrStatus"},
    {"id": "video", "friendly_name": "Video available"},
]

FANS = [
    {
        "id": "fanCase",
        "friendly_name": "Back Fan",
        "percentage_get_command": "caseFanPct",
        "fan_number": 0,
    },
    {
        "id": "fan",
        "friendly_name": "Model Fan",
        "percentage_get_command": "modelFanPct",
        "fan_number": 1,
    },
    {
        "id": "fanAuxiliary",
        "friendly_name": "Side Fan",
        "percentage_get_command": "auxiliaryFanPct",
        "fan_number": 2,
    },
]

BUTTONS = [
    {
        "id": "restart_button",
        "friendly_name": "Restart Button",
        "device_class": ButtonDeviceClass.RESTART,
    }
]
# input sensors
# buttos to move around
