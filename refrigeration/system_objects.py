from .utils import get_suction_temp, get_min_condensing_temp
from itertools import count
import json

def generate_system_and_casewalkin_lists(
    selected_case_units,
    selected_walkin_units,
    mt_racks,
    lt_racks,
    selected_template,
    system_name_prefix="Supermarket Rack",
    compressor_prefix="Compressor_List",
    condenser_prefix="Condenser",
    refrigerant="R404A",
    end_use_category="Refrigeration"
):
    """
    Generate RefrigerationSystem and CaseAndWalkInList objects.
    Returns a list of JSON objects.
    """

    if not selected_case_units and not selected_walkin_units:
        raise ValueError("Selected case or walk-in units not found.")

    name_map = {u.case_name: u.osm_name for u in selected_case_units}
    name_map.update({u.walkin_name: u.osm_name for u in selected_walkin_units})

    system_objects = []
    rack_id_gen = count(1)

    def create_objects_for_rack(rack, rack_type):
        rack_number = next(rack_id_gen)
        case_and_walkin_names = [name_map.get(item["name"], item["name"]) for item in rack]
        suction_temp = get_suction_temp(selected_template, rack_type)
        min_cond_temp = get_min_condensing_temp(selected_template, rack_type)

        system_name = f"{system_name_prefix} {rack_type} {rack_number}"
        list_name = f"{system_name}_CaseWalkinList"

        system = {
            "type": "OS:Refrigeration:System",
            "name": system_name,
            "CompressorListName": f"{compressor_prefix}_{rack_type}_Rack{rack_number}",
            "CondenserName": f"{condenser_prefix}_{rack_type}_Rack{rack_number}",
            "CaseAndWalkInListName": list_name,
            "RefrigerantType": refrigerant,
            "SuctionTemperature": suction_temp,
            "MinimumCondensingTemperature": min_cond_temp,
            "EndUseSubcategory": end_use_category
        }

        case_list = {
            "type": "OS:Refrigeration:CaseAndWalkInList",
            "name": list_name,
            "CaseAndWalkInNames": case_and_walkin_names
        }

        return system, case_list

    for rack in mt_racks:
        system, case_list = create_objects_for_rack(rack, "MT")
        system_objects.extend([system, case_list])

    for rack in lt_racks:
        system, case_list = create_objects_for_rack(rack, "LT")
        system_objects.extend([system, case_list])

    return system_objects


def prepare_and_store_system_and_casewalkin_lists(
    selected_case_units,
    selected_walkin_units,
    mt_racks,
    lt_racks,
    template
):
    """
    Wrapper function to generate system + case/walkin list and return the result.
    """
    system_objects = generate_system_and_casewalkin_lists(
        selected_case_units,
        selected_walkin_units,
        mt_racks,
        lt_racks,
        template
    )
    
    # Instead of using globals(), return the generated system objects
    print("✅ Refrigeration system +  case/walkin list objects generated and ready.")
    return system_objects