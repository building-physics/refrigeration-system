
import sqlite3, json
from .utils import get_suction_temp

def generate_compressor_objects(compressor_info, template, operation_type, curve_json=None):
    """
    Generate RefrigerationCompressor OpenStudio JSON objects including performance curve and suction temp.

    Args:
        compressor_info (list): rack_number, rack_load, compressors_needed
        template (str): 'old', 'new', or 'advanced'
        operation_type (str): 'MT' or 'LT'
        curve_json (dict): Performance curve JSON (optional)

    Returns:
        List[dict]: List of RefrigerationCompressor JSON objects
    """
    compressor_objects = []
    capacity_w, power_w, cop, eer = get_compressor_specs(template, operation_type)
    suction_temp = get_suction_temp(template, operation_type)  
    curve_name = curve_json.get("name") if curve_json else None

    for rack in compressor_info:
        rack_number = rack['rack_number']
        num_compressors = max(rack['compressors_needed'], 15) 

        for i in range(1, num_compressors + 1):
            name = f"{template.upper()}_{operation_type}_Rack{rack_number}_Comp{i}"
            comp = {
                "type": "OS:Refrigeration:Compressor",
                "name": name,
                "RatedPowerConsumption": power_w,
                "RatedCapacity": capacity_w,
                "RefrigerantOilCoolerPower": 0,
                "EndUseSubcategory": f"{operation_type}_Compressor_Rack{rack_number}",
                "SuctionTemperature": suction_temp  
            }
            if curve_name:
                comp["CompressorCurve"] = curve_name

            compressor_objects.append(comp)

    return compressor_objects

def get_compressor_specs(template, operation_type):
    """Return compressor specs: capacity (W), power (W), COP, EER."""
    if operation_type == "MT":
        if template == "old":
            return 52733.94, 24945, 2.12, 7.22
        else:
            return 38099.93, 15448, 2.47, 8.42
    elif operation_type == "LT":
        if template == "old":
            return 20038.77, 13963, 1.44, 4.90
        else:
            return 17181.96, 9766, 1.76, 6.00
    else:
        raise ValueError(f"Unknown operation type: {operation_type}")

def summarize_compressor_assignment(mt_racks, lt_racks, selected_template):
    """
    Calculate and display compressor assignment and specs based on rack loads and template.
    
    Args:
        mt_racks (list): List of MT rack load info
        lt_racks (list): List of LT rack load info
        selected_template (str): Template type ('old', 'new', 'advanced')
    
    Returns:
        Tuple: (mt_info, lt_info) list of compressor assignments for each rack
    """
    mt_info = calculate_compressors_for_racks(mt_racks, "MT", template=selected_template)
    lt_info = calculate_compressors_for_racks(lt_racks, "LT", template=selected_template)

    print("\n🧊 MT Rack Compressor Assignment:")
    for info in mt_info:
        print(f"Rack {info['rack_number']}: Load = {info['rack_load']:.2f} W → Compressors Needed = {info['compressors_needed']}")

    print("\n❄️ LT Rack Compressor Assignment:")
    for info in lt_info:
        print(f"Rack {info['rack_number']}: Load = {info['rack_load']:.2f} W → Compressors Needed = {info['compressors_needed']}")

    # Specs 출력
    mt_capacity, mt_power, mt_cop, mt_eer = get_compressor_specs(selected_template, "MT")
    lt_capacity, lt_power, lt_cop, lt_eer = get_compressor_specs(selected_template, "LT")

    print(f"\n⚙️ Compressor Specs for the selected template '{selected_template}':")
    print(f"🧊 MT → Capacity: {mt_capacity:.2f} W, Power: {mt_power:.2f} W, COP: {mt_cop:.2f}, EER: {mt_eer:.2f}")
    print(f"❄️ LT → Capacity: {lt_capacity:.2f} W, Power: {lt_power:.2f} W, COP: {lt_cop:.2f}, EER: {lt_eer:.2f}")

    return mt_info, lt_info

def get_compressor_curve(db_path, template, operation_type, curve_type=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT curve_name, coefficient1, coefficient2, coefficient3, coefficient4, 
           coefficient5, coefficient6, coefficient7, coefficient8, coefficient9, coefficient10,
           min_val_x, max_val_x, min_val_y, max_val_y
    FROM refrigeration_compressors
    WHERE template = ? AND operation_type = ?
    """
    params = [template, operation_type]

    if curve_type:
        query += " AND curve_type = ?"
        params.append(curve_type)

    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    (curve_name, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
     min_x, max_x, min_y, max_y) = row

    curve_json = {
        "type": "OS:Curve:Bicubic",
        "name": curve_name,
        "Coefficient1Constant": c1,
        "Coefficient2x": c2,
        "Coefficient3x2": c3,
        "Coefficient4y": c4,
        "Coefficient5y2": c5,
        "Coefficient6xy": c6,
        "Coefficient7x3": c7,
        "Coefficient8x2y": c8,
        "Coefficient9xy2": c9,
        "Coefficient10y3": c10,
        "MinimumValueofx": min_x,
        "MaximumValueofx": max_x,
        "MinimumValueofy": min_y,
        "MaximumValueofy": max_y,
        "InputUnitTypeforX": "Temperature",
        "InputUnitTypeforY": "Temperature",
        "OutputUnitType": "Dimensionless"
    }

    return curve_json

def load_and_print_compressor_curves(db_path, selected_template, verbose=True):
    mt_power_curve = get_compressor_curve(db_path, selected_template, "MT", curve_type="power")
    mt_capacity_curve = get_compressor_curve(db_path, selected_template, "MT", curve_type="capacity")
    lt_power_curve = get_compressor_curve(db_path, selected_template, "LT", curve_type="power")
    lt_capacity_curve = get_compressor_curve(db_path, selected_template, "LT", curve_type="capacity")

    if verbose:
        print("📈 MT Power Curve JSON:")
        print(json.dumps(mt_power_curve, indent=4) if mt_power_curve else "❌ No MT power curve found.")
        print("\n📈 MT Capacity Curve JSON:")
        print(json.dumps(mt_capacity_curve, indent=4) if mt_capacity_curve else "❌ No MT capacity curve found.")
        print("\n📈 LT Power Curve JSON:")
        print(json.dumps(lt_power_curve, indent=4) if lt_power_curve else "❌ No LT power curve found.")
        print("\n📈 LT Capacity Curve JSON:")
        print(json.dumps(lt_capacity_curve, indent=4) if lt_capacity_curve else "❌ No LT capacity curve found.")

    return mt_power_curve, mt_capacity_curve, lt_power_curve, lt_capacity_curve

    
def calculate_compressors_for_racks(racks, rack_type, template, redundancy=True):
    capacity, _, _, _ = get_compressor_specs(template, rack_type)

    compressors_per_rack = []
    for i, rack in enumerate(racks, 1):
        total_capacity = sum(item['capacity'] for item in rack)
        compressors = total_capacity / capacity
        compressors = int(compressors) + (1 if compressors % 1 > 0 else 0)

        if redundancy:
            compressors += 1

        compressors_per_rack.append({
            "rack_number": i,
            "rack_load": total_capacity,
            "compressors_needed": compressors
        })

    return compressors_per_rack

def prepare_and_store_compressor_objects(mt_info, lt_info, template, db_path):
    # 1. Load performance curves from database
    mt_power_curve, mt_capacity_curve, lt_power_curve, lt_capacity_curve = load_and_print_compressor_curves(db_path, template, verbose=False)
    # 2. Generate compressor objects using power curves
    mt_compressors = generate_compressor_objects(mt_info, template, "MT", curve_json=mt_power_curve)
    lt_compressors = generate_compressor_objects(lt_info, template, "LT", curve_json=lt_power_curve)

    result = {
        "mt_compressors": mt_compressors,
        "lt_compressors": lt_compressors,
        "mt_power_curve": mt_power_curve,
        "mt_capacity_curve": mt_capacity_curve,
        "lt_power_curve": lt_power_curve,
        "lt_capacity_curve": lt_capacity_curve
    }
    # 4. Store in global scope
    globals().update(result)
    print("✅ Compressor objects and performance curves ready.")
    return result
