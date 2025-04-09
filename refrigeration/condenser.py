from .utils import get_min_condensing_temp
def generate_condenser_objects(rack_info, operation_type, template):
    """
    Generate OS:Refrigeration:Condenser:AirCooled objects and corresponding performance curves
    for each rack based on the rack load and operation type (MT or LT).

    Args:
        rack_info (list): List of dicts with rack_number and rack_load
        operation_type (str): 'MT' or 'LT'
        template (str): 'old', 'new', or 'advanced'

    Returns:
        Tuple[List[dict], List[dict]]: condensers, curves
    """
    condensers = []
    curves = []

    min_cond_temp = get_min_condensing_temp(template, operation_type)

    for rack in rack_info:
        rack_num = rack['rack_number']
        load = rack['rack_load']

        # Condenser capacity 
        if operation_type == "LT":
            cond_capacity = 1.2 * load * (1 + 1 / 1.3)
        elif operation_type == "MT":
            cond_capacity = 1.2 * load * (1 + 1 / 2.0)
        else:
            raise ValueError("Invalid operation type. Must be 'MT' or 'LT'.")

        fan_power = 0.0441 * cond_capacity + 695
        condenser_name = f"{operation_type}_Rack{rack_num}_Condenser"
        curve_name = f"{condenser_name}_FanCurve"

        condensers.append({
            "type": "OS:Refrigeration:Condenser:AirCooled",
            "name": condenser_name,
            "RatedEffectiveTotalHeatRejectionRate": cond_capacity,
            "FanPower": fan_power,
            "RatedSubcoolingTemperatureDifference": 5 if operation_type == "MT" else 0,
            "FanPowerCurve": curve_name,
            "MinimumCondensingTemperature": min_cond_temp
        })

        curves.append({
            "type": "OS:Curve:Linear",
            "name": curve_name,
            "Coefficient1Constant": 0,
            "Coefficient2x": cond_capacity / 5.6,
            "MinimumValueofx": 0,
            "MaximumValueofx": 1,
            "InputUnitTypeforX": "Dimensionless",
            "OutputUnitType": "Dimensionless"
        })

    return condensers, curves


    
def prepare_and_store_condenser_objects(mt_info, lt_info, selected_template):
    """
    Generate and store condenser and curve objects without using global variables.

    Args:
        mt_info (list): List of MT rack data
        lt_info (list): List of LT rack data
        selected_template (str): Template type, 'old', 'new', or 'advanced'

    Returns:
        dict: A dictionary containing the condenser and curve objects for MT and LT
    """
    # Generate condenser and curve objects for MT and LT
    mt_condensers, mt_curves = generate_condenser_objects(mt_info, "MT", selected_template)
    lt_condensers, lt_curves = generate_condenser_objects(lt_info, "LT", selected_template)

    # Return the generated objects as a dictionary
    result = {
        "mt_condensers": mt_condensers,
        "lt_condensers": lt_condensers,
        "mt_curves": mt_curves,
        "lt_curves": lt_curves
    }

    print("✅ Condenser and curve objects generated and stored in the result.")
    return result