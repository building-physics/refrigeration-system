import json
from .utils import get_building_name

def export_full_refrigeration_system_to_json(
    mt_compressors,
    lt_compressors,
    mt_power_curve,
    mt_capacity_curve,
    lt_power_curve,
    lt_capacity_curve,
    mt_condensers,
    lt_condensers,
    mt_curves,
    lt_curves,
    case_objects,
    walkin_objects,
    system_and_casewalkin_objects,
    case_zone_name="MainSales",
    walkin_zone_name="ActiveStorage",
    output_path="Full_Refrigeration_System.json"
):
    zones = [
        {"type": "OS:ThermalZone", "name": case_zone_name},
        {"type": "OS:ThermalZone", "name": walkin_zone_name}
    ]

    all_objects = (
        zones +
        [mt_power_curve, mt_capacity_curve, lt_power_curve, lt_capacity_curve] +
        mt_compressors + lt_compressors +
        mt_condensers + lt_condensers +
        mt_curves + lt_curves +
        case_objects + walkin_objects +
        system_and_casewalkin_objects
    )

    openstudio_json = {
        "Version": "0.2.1",
        "Building": get_building_name(),
        "objects": all_objects
    }

    with open(output_path, "w") as f:
        json.dump(openstudio_json, f, indent=2)

    print(f"✅ Full OpenStudio Refrigeration JSON saved to: {output_path}")
    print("\n📦 Preview:")
    print(json.dumps(openstudio_json, indent=2))