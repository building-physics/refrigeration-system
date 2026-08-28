# SPDX-FileCopyrightText: 2025-present Oak Ridge National Laboratory, managed by UT-Battelle
#
# SPDX-License-Identifier: BSD-3-Clause
def generate_case_objects_from_data(case_data, selected_case_units, case_zone_name):
    """Generate OS:Refrigeration:Case JSON objects based on database data and unit zones."""

    objects = []
    for osm_name, info in case_data.items():
        zone_name = info.get("zone_name", case_zone_name)

        obj = {
            "type": "OS:Refrigeration:Case",
            "name": osm_name,
            "ZoneName": zone_name,
            "CaseName": info.get("case_name"),
            "Template": info.get("template"),
            "OperationType": info.get("operation_type"),
            "RatedTotalCoolingCapacity": info.get("rated_capacity"),
            "CaseLength": round(info.get("unit_length") * info.get("assigned_units", info.get("unit_count", 1)), 1),
            "OperatingTemperature": info.get("case_operating_temperature"),
            "EvaporatorTemperature": info.get("evaporator_temperature"),
            "RatedLatentHeatRatio": info.get("rated_latent_heat_ratio"),
            "RatedRuntimeFraction": info.get("rated_runtime_fraction"),
            "LatentCaseCreditCurveType": info.get("latent_case_credit_curve_type"),
            "LatentCaseCreditCurveName": info.get("latent_case_credit_curve_name"),
            "FanPowerPerUnitLength": info.get("fan_power"),
            "LightingPowerPerUnitLength": info.get("lighting_power"),
            "CaseLightingScheduleName": info.get("case_lighting_schedules"),
            "FractionofLightingEnergytoCase": info.get("fraction_of_lighting_energy_to_case"),
            "AntiSweatHeaterPowerperUnitLength": info.get("anti_sweat_power"),
            "AntiSweatHeaterControlType": info.get("anti_sweat_heater_control_type"),
            "FractionofAntiSweatHeaterEnergytoCase": info.get("fraction_of_anti_sweat_heater_energy_to_cases"),
            "DefrostPowerPerUnitLength": info.get("defrost_power"),
            "DefrostType": info.get("defrost_type"),
            "DefrostScheduleName": info.get("defrost_schedule"),
            "DripDownScheduleName": info.get("drip_down_schedule"),
            "DefrostEnergyCorrectionCurveType": info.get("defrost_energy_correction_curve_type"),
            "DefrostEnergyCorrectionCurveName": info.get("defrost_energy_correction_curve_name"),
            "DesignCaseHVACReturnAirFraction": info.get("HVAC_return_air_fraction"),
            "CaseRestockingScheduleName": info.get("restocking_schedule"),
            "CaseCreditFractionScheduleName": info.get("case_credit_fraction_schedule"),
            "DefrostTime": info.get("defrost_time"),
            "DripdownTime": info.get("dripdown_time"),
            "DefrostNumber": info.get("number_of_defrost_per_day")
        }
        objects.append(obj)
    return objects


def generate_walkin_objects_from_data(walkin_data, selected_walkin_units, walkin_zone_name):
    """Generate OS:Refrigeration:WalkIn JSON objects based on database data and unit zones."""
    objects = []
    for osm_name, info in walkin_data.items():
        zone_name = info.get("zone_name", walkin_zone_name)

        obj = {
            "type": "OS:Refrigeration:WalkIn",
            "name": osm_name,
            "ZoneName": zone_name,
            "WalkInName": info.get("walkin_name"),
            "Template": info.get("template"),
            "OperationType": info.get("operation_type"),
            "InsulatedFloorArea": info.get("insulated_floor_area"),
            "RatedCoolingCapacity": info.get("rated_capacity"),
            "OperatingTemperature": info.get("operating_temperature"),
            "RatedCoolingSourceTemperature": info.get("rated_cooling_source_temperature"),
            "RatedTotalHeatingPower": info.get("rated_total_heating_power"),
            "CoolingFanPower": info.get("rated_cooling_fan_power"),
            "LightingPower": info.get("lighting_power"),
            "LightingScheduleName": info.get("lighting_schedule"),
            "DefrostType": info.get("defrost_type"),
            "DefrostControlType": info.get("defrost_control_type"),
            "DefrostScheduleName": info.get("defrost_schedule"),
            "DripDownScheduleName": info.get("drip_down_schedule"),
            "DefrostPower": info.get("defrost_power"),
            "TemperatureTerminationDefrostFractionToIce": info.get("temperature_termination_defrost_fraction_to_ice"),
            "InsulatedFloorUValue": info.get("insulated_floor_uvalue"),
            "TotalInsulatedSurfaceAreaFacingZone": info.get("total_insulatedsurface_area_facing_zone"),
            "InsulatedSurfaceUValueFacingZone": info.get("insulated_surface_uvalue_facing_zone"),
            "GlassReachInDoorAreaFacingZone": info.get("area_of_glass_reachin_doors_facing_zone"),
            "GlassReachInDoorUValue": info.get("reachin_door_uvalue"),
            "StockingDoorAreaFacingZone": info.get("area_of_stocking_doors_facing_zone"),
            "HeightOfStockingDoorsFacingZone": info.get("height_of_stocking_doors_facing_zone"),
            "StockingDoorUValue": info.get("stocking_door_u"),
            "StockingDoorScheduleName": info.get("stocking_door_schedule"),
            "StockingDoorOpeningProtection": info.get("stocking_door_opening_protection"),
            "DefrostTime": info.get("defrost_time"),
            "DripdownTime": info.get("dripdown_time"),
            "DefrostNumber": info.get("number_of_defrost_per_day"),
            "AssignedUnits": info.get("assigned_units", 1)
        }
        objects.append(obj)
    return objects

def prepare_and_store_case_and_walkin_objects(case_data, walkin_data, selected_case_units, selected_walkin_units, case_zone_name, walkin_zone_name):


    # Generate objects
    case_objects = generate_case_objects_from_data(case_data, selected_case_units, case_zone_name)
    walkin_objects = generate_walkin_objects_from_data(walkin_data, selected_walkin_units, walkin_zone_name)


        # Return the generated objects
    print("✅ Case and walk-in objects generated and stored")
    return {
        "case_objects": case_objects,
        "walkin_objects": walkin_objects
    }