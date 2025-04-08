
def generate_case_objects_from_data(case_data, selected_case_units):
    """Generate OS:Refrigeration:Case JSON objects based on database data and unit zones."""
    name_to_osm = {unit.case_name: unit.osm_name for unit in selected_case_units}
    name_to_zone = {unit.case_name: unit.zone_name for unit in selected_case_units}

    objects = []
    for case_name, info in case_data.items():
        osm_name = name_to_osm.get(case_name, case_name)
        zone_name = name_to_zone.get(case_name, "MainSales")

        obj = {
            "type": "OS:Refrigeration:Case",
            "name": osm_name,
            "ZoneName": zone_name,
            "CaseLength": info.get("unit_length"),
            "RatedTotalCoolingCapacity": info.get("rated_capacity"),
            "OperatingTemperature": info.get("case_operating_temperature"),
            "EvaporatorTemperature": info.get("evaporator_temperature"),
            "FanPowerPerUnitLength": info.get("fan_power_per_unit_length"),
            "LightingPowerPerUnitLength": info.get("lighting_power_per_unit_length"),
            "DefrostType": info.get("defrost_type"),
            "DefrostSchedule": info.get("defrost_schedule"),
            "DripDownSchedule": info.get("drip_down_schedule"),
            "CaseLightingScheduleName": info.get("case_lighting_schedule")
        }
        objects.append(obj)
    return objects


def generate_walkin_objects_from_data(walkin_data, selected_walkin_units):
    """Generate OS:Refrigeration:WalkIn JSON objects based on database data and unit zones."""
    name_to_osm = {unit.walkin_name: unit.osm_name for unit in selected_walkin_units}
    name_to_zone = {unit.walkin_name: unit.zone_name for unit in selected_walkin_units}

    objects = []
    for walkin_name, info in walkin_data.items():
        osm_name = name_to_osm.get(walkin_name, walkin_name)
        zone_name = name_to_zone.get(walkin_name, "ActiveStorage")

        obj = {
            "type": "OS:Refrigeration:WalkIn",
            "name": osm_name,
            "ZoneName": zone_name,
            "RatedCoolingCapacity": info.get("rated_capacity"),
            "OperatingTemperature": info.get("operating_temperature"),
            "CoolingFanPower": info.get("rated_cooling_fan_power"),
            "LightingPower": info.get("lighting_power"),
            "LightingScheduleName": info.get("lighting_schedule"),
            "DefrostType": info.get("defrost_type"),
            "DefrostControlType": info.get("defrost_control_type"),
            "DefrostScheduleName": info.get("defrost_schedule"),
            "DripDownScheduleName": info.get("drip_down_schedule"),
            "StockingDoorUValue": info.get("stocking_door_u"),
            "StockingDoorAreaFacingZone": info.get("area_of_stocking_doors_facing_zone"),
            "StockingDoorScheduleName": info.get("stocking_door_schedule"),
            "GlassReachInDoorUValue": info.get("reachin_door_uvalue"),
            "GlassReachInDoorAreaFacingZone": info.get("area_of_glass_reachin_doors_facing_zone")
        }
        objects.append(obj)
    return objects

def prepare_and_store_case_and_walkin_objects(case_data, walkin_data, selected_case_units, selected_walkin_units):
    """
    Generate and store refrigeration case and walk-in JSON objects into global variables.

    Args:
        case_data (dict): Case data from DB
        walkin_data (dict): Walk-in data from DB
        selected_case_units (list): List of BuildingUnit objects for cases
        selected_walkin_units (list): List of BuildingUnit objects for walk-ins
    """

    globals()["case_data"] = case_data
    globals()["walkin_data"] = walkin_data
    globals()["selected_case_units"] = selected_case_units
    globals()["selected_walkin_units"] = selected_walkin_units

    # Generate objects
    case_objects = generate_case_objects_from_data(case_data, selected_case_units)
    walkin_objects = generate_walkin_objects_from_data(walkin_data, selected_walkin_units)

    # Store into globals
    globals()["case_objects"] = case_objects
    globals()["walkin_objects"] = walkin_objects

    print("✅ Case and walk-in objects generated and stored in globals.")