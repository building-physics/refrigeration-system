# SPDX-FileCopyrightText: 2025-present Oak Ridge National Laboratory, managed by UT-Battelle
#
# SPDX-License-Identifier: BSD-3-Clause
from .db_utils import get_data_from_db
from typing import Dict, List

# Distribution units using First-Fit Decreasing (FFD) Strategy
def distribute_units(data: Dict, racks: List, max_capacity_per_rack):
    # Pre-compute total rated capacity for consistent sorting
    for name, item in data.items():
        unit_count = item.get('unit_count') or item.get('number_of_units') or 1
        rated_capacity = item.get('rated_capacity', 0)
        if 'unit_length' in item:  # Case
            item['total_rated_capacity'] = rated_capacity * item.get('unit_length', 1) * unit_count
        else:  # Walk-in
            item['total_rated_capacity'] = rated_capacity * unit_count

    # Sort by descending total rated capacity
    sorted_units = sorted(data.items(), key=lambda x: x[1]['total_rated_capacity'], reverse=True)

    rack_list = []

    for name, item in sorted_units:
        total_capacity = item['total_rated_capacity']

        if not total_capacity:
            continue

        placed = False

        for rack in rack_list:
            if rack["capacity"] + total_capacity <= max_capacity_per_rack:
                rack["units"].append({'name': name, 'capacity': total_capacity})
                rack["capacity"] += total_capacity
                placed = True
                break

        if not placed:
            rack_list.append({
                "units": [{"name": name, "capacity": total_capacity}],
                "capacity": total_capacity
            })

        item['assigned_rack'] = len(rack_list)
        item["assigned_units"] = item.get("unit_count") or item.get("number_of_units") or 1
        item["osm_name"] = name

    # Finalize racks
    for i, rack in enumerate(rack_list, start=1):
        for unit in rack["units"]:
            base_name = unit["name"]
            if base_name in data:
                data[base_name]['assigned_rack'] = i
        racks.append(rack["units"])

            
def assign_racks_to_cases_and_walkins(db_path, selected_case_units, selected_walkin_units, default_max_capacity=30000):
    # Load case and walk-in data
    case_data, walkin_data = get_data_from_db(db_path, selected_case_units, selected_walkin_units)

    # Determine template from selected units
    template = None
    if selected_case_units:
        template = selected_case_units[0].template.lower()
    elif selected_walkin_units:
        template = selected_walkin_units[0].template.lower()

    # Define max capacities
    if template == "advanced":
        max_mt_capacity = 30000
        max_lt_capacity = 15000
    elif template in ["old", "new"]:
        max_mt_capacity = 50000
        max_lt_capacity = 25000
    else:
        max_mt_capacity = max_lt_capacity = default_max_capacity

    combined_mt = {
        **{k: v for k, v in case_data.items() if v.get("operation_type") == "MT"},
        **{k: v for k, v in walkin_data.items() if v.get("operation_type") == "MT"}
    }

    combined_lt = {
        **{k: v for k, v in case_data.items() if v.get("operation_type") == "LT"},
        **{k: v for k, v in walkin_data.items() if v.get("operation_type") == "LT"}
    }

    # Initialize racks
    mt_racks = []
    lt_racks = []

    # Distribute units (make sure distribute_units assigns osm_name correctly!)
    distribute_units(combined_mt, mt_racks, max_mt_capacity)
    distribute_units( combined_lt, lt_racks, max_lt_capacity)
  
    case_data.update({k: v for k, v in combined_mt.items() if k in case_data})
    case_data.update({k: v for k, v in combined_lt.items() if k in case_data})
    walkin_data.update({k: v for k, v in combined_mt.items() if k in walkin_data})
    walkin_data.update({k: v for k, v in combined_lt.items() if k in walkin_data})

 
    for item in list(case_data.values()) + list(walkin_data.values()):
        item["osm_name"] = item.get("osm_name") or item.get("case_name") or item.get("walkin_name")
        item["assigned_units"] = item.get("assigned_units") or item.get("unit_count") or item.get("number_of_units") or 1


    return mt_racks, lt_racks, case_data, walkin_data


def display_rack_capacity(racks, case_or_walkin_data, rack_type=""):
    print(f"\n{rack_type} Racks:")

    for i, rack in enumerate(racks, 1):
        total_capacity = sum(item['capacity'] for item in rack)
        print(f"Rack {i}: Total Capacity = {total_capacity:.2f} W")

        for item in rack:
            name = item['name']
            cap = item['capacity']

            obj_data = case_or_walkin_data.get(name)


            unit_info = ""

            if obj_data and "assigned_units" in obj_data:
                unit_info = f" ({int(obj_data['assigned_units'])} units)"

            print(f"  - {name} : {cap:.2f} W{unit_info}")


        print()

         