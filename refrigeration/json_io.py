from refrigeration.utils import get_building_name
import json

# Compressors
def export_existing_compressors_to_json(
    mt_compressors,
    lt_compressors,
    mt_power_curve,
    mt_capacity_curve,
    lt_power_curve,
    lt_capacity_curve,
    output_path="All_Compressors.json"
):
    zones = [
        {"type": "OS:ThermalZone", "name": "MainSales"},
        {"type": "OS:ThermalZone", "name": "ActiveStorage"}
    ]
    # Concatenate the objects correctly into a list
    objects = [
        *zones, 
        mt_power_curve, mt_capacity_curve,
        lt_power_curve, lt_capacity_curve,
        *mt_compressors, *lt_compressors
    ]


    openstudio_json = {
        "Version": "0.2.1",
        "Building": get_building_name(),
        "objects": objects
    }

    # Save to output path
    with open(output_path, "w") as f:
        json.dump(openstudio_json, f, indent=4)

    print(f"✅ Compressor + Curve JSON with zones saved to: {output_path}")
    print("\n📦 OpenStudio JSON Preview:\n")
    print(json.dumps(openstudio_json, indent=2))

# Condensers
def export_existing_condensers_to_json(
    mt_condensers,
    lt_condensers,
    mt_curves,
    lt_curves,
    output_path="All_Condensers.json"
):
    zones = [
        {"type": "OS:ThermalZone", "name": "MainSales"},
        {"type": "OS:ThermalZone", "name": "ActiveStorage"}
    ]

    objects = (
        zones +
        mt_condensers + lt_condensers +
        mt_curves + lt_curves
    )

    openstudio_json = {
        "Version": "0.2.1",
        "Building": get_building_name(),
        "objects": objects
    }

    with open(output_path, "w") as f:
        json.dump(openstudio_json, f, indent=2)

    print(f"✅ Condensers + Curves with zones saved to: {output_path}")
    print("\n📤 Condenser JSON Preview:")
    print(json.dumps(openstudio_json, indent=2))

# Case + Walk-in
def export_cases_and_walkins_to_json(
    case_objects,
    walkin_objects,
    output_path="Cases_and_Walkins.json"
):
    zones = [
        {"type": "OS:ThermalZone", "name": "MainSales"},
        {"type": "OS:ThermalZone", "name": "ActiveStorage"}
    ]

    objects = zones + case_objects + walkin_objects

    openstudio_json = {
        "Version": "0.2.1",
        "Building": get_building_name(),
        "objects": objects
    }

    with open(output_path, "w") as f:
        json.dump(openstudio_json, f, indent=2)

    print(f"✅ Case + Walk-in JSON with zones saved to: {output_path}")
    print("\n📦 Preview:")
    print(json.dumps(openstudio_json, indent=2))


# System + Case list
def export_system_and_casewalkin_lists_to_json(
    refrigeration_system_objects,
    output_path="case_walkin_list.json"
):
    zones = [
        {"type": "OS:ThermalZone", "name": "MainSales"},
        {"type": "OS:ThermalZone", "name": "ActiveStorage"}
    ]

    objects = zones + refrigeration_system_objects

    openstudio_json = {
        "Version": "0.2.1",
        "Building": get_building_name(),
        "objects": objects
    }

    with open(output_path, "w") as f:
        json.dump(openstudio_json, f, indent=2)


    print(f"✅ Refrigeration system + Case/Walk-in list saved to: {output_path}")
    print("\n📦 Preview:")
    print(json.dumps(openstudio_json, indent=2))