import sqlite3

def get_data_from_db(db_path, selected_case_units, selected_walkin_units):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    case_data = {}
    walkin_data = {}

    # CASES ---------------------------------
    case_counts = {}
    case_lookup = {}

    for unit in selected_case_units:
        osm_name = unit.osm_name
        base_name = unit.base_name
        count = unit.number_of_units
        template = unit.template
        full_case_name = f"{template} {base_name}"

        case_counts[osm_name] = count
        case_lookup[osm_name] = full_case_name  # Use base_name for query

    for osm_name, count in case_counts.items():
        base_name = case_lookup[osm_name]

        cursor.execute("""            
            SELECT 
                case_name, template, operation_type,
                rated_capacity, unit_length, case_operating_temperature,
                evaporator_temperature, fan_power, lighting_power,
                defrost_type, defrost_schedules, drip_down_schedules,
                case_lighting_schedules, fraction_of_lighting_energy_to_case,
                anti_sweat_power, anti_sweat_heater_control_type,
                fraction_of_anti_sweat_heater_energy_to_cases,
                rated_latent_heat_ratio, rated_runtime_fraction,
                latent_case_credit_curve_type, latent_case_credit_curve_name,
                defrost_energy_correction_curve_type, defrost_energy_correction_curve_name,
                HVAC_return_air_fraction, restocking_schedule, case_credit_fraction_schedule
            FROM refrigeration_cases 
            WHERE lower(case_name) = ?
            """, (base_name.lower(),))
        row = cursor.fetchone()

        if row:
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            row_dict["unit_count"] = count
            row_dict["total_rated_capacity"] = row_dict["rated_capacity"] * row_dict["unit_length"] * count
            case_data[osm_name] = row_dict

    # WALK-INS -------------------------------
    walkin_counts = {}
    walkin_lookup = {}

    for unit in selected_walkin_units:
        osm_name = unit.osm_name
        base_name = unit.base_name
        count = unit.number_of_units
        template = unit.template
        full_walkin_name = f"{unit.template} {unit.base_name}"

        walkin_counts[osm_name] = count
        walkin_lookup[osm_name] = full_walkin_name

    for osm_name, count in walkin_counts.items():
        base_name = walkin_lookup[osm_name]

        cursor.execute("""
             SELECT
                walkin_name, template, operation_type,
                rated_capacity, operating_temperature,
                rated_cooling_fan_power, lighting_power, lighting_schedule,
                defrost_type, defrost_control_type, defrost_schedule, drip_down_schedule,
                stocking_door_u, area_of_stocking_doors_facing_zone, stocking_door_schedule,
                reachin_door_uvalue, area_of_glass_reachin_doors_facing_zone
            FROM refrigeration_walkins
            WHERE lower(walkin_name) = ?
            """, (base_name.lower(),))
        row = cursor.fetchone()

        if row:
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            row_dict["number_of_units"] = count
            row_dict["total_rated_capacity"] = row_dict["rated_capacity"] * count
            walkin_data[osm_name] = row_dict

    conn.close()
    return case_data, walkin_data