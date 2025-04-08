import sqlite3

def get_data_from_db(db_path, selected_case_units, selected_walkin_units):
    """
    Load case and walk-in data from the database using selected units.

    Args:
        db_path (str): Path to the SQLite DB.
        selected_case_units (list): List of CaseUnit objects (with .case_name and .number_of_units).
        selected_walkin_units (list): List of WalkInUnit objects (with .walkin_name and .number_of_units).

    Returns:
        Tuple[dict, dict]: (case_data, walkin_data)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    case_data = {}
    walkin_data = {}

    # CASES ---------------------------------
    case_counts = {}
    for unit in selected_case_units:
        key = unit.case_name.lower()
        case_counts[key] = case_counts.get(key, 0) + unit.number_of_units

    for case_name, count in case_counts.items():
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
            """, (case_name,))
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            row_dict["unit_count"] = count
            row_dict["total_rated_capacity"] = row_dict["rated_capacity"] * row_dict["unit_length"] * count
            case_data[row[0]] = row_dict

    # WALK-INS -------------------------------
    walkin_counts = {}
    for unit in selected_walkin_units:
        key = unit.walkin_name.lower()
        walkin_counts[key] = walkin_counts.get(key, 0) + unit.number_of_units

    for walkin_name, count in walkin_counts.items():
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
            """, (walkin_name,))
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            row_dict["number_of_units"] = count
            row_dict["total_rated_capacity"] = row_dict["rated_capacity"] * count
            walkin_data[row[0]] = row_dict

    conn.close()
    return case_data, walkin_data