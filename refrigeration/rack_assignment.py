from .db_utils import get_data_from_db

# Distribution units using First-Fit Decreasing (FFD) Strategy
def distribute_units(data, racks, max_capacity_per_rack):
    # Pre-compute total rated capacity for consistent sorting
    for name, item in data.items():
        unit_count = item.get('unit_count') or item.get('number_of_units') or 1
        rated_capacity = item.get('rated_capacity', 0)
        if 'unit_length' in item:  # Case
            item['total_rated_capacity'] = rated_capacity * item.get('unit_length', 1) * unit_count
        else:  # Walk-in
            item['total_rated_capacity'] = rated_capacity * unit_count

    # Sort by descending total rated capacity
    units = sorted(data.items(), key=lambda x: x[1]['total_rated_capacity'], reverse=True)

    rack_list = []

    for name, item in units:
        total_capacity = item['total_rated_capacity']
        rated_capacity = item.get('rated_capacity', 0)
        unit_length = item.get('unit_length', 1) if 'unit_length' in item else 1
        unit_count = item.get('unit_count') or item.get('number_of_units') or 1

        if not rated_capacity or not unit_count:
            continue

        if total_capacity > max_capacity_per_rack:
            # Oversized unit → split across multiple racks
            remaining_units = unit_count
            split_index = 1
            
            if 'unit_length' in item:  # Case
                unit_capacity = rated_capacity * unit_length
            else:  # Walk-in
                unit_capacity = rated_capacity

            max_units_per_rack = max(int(max_capacity_per_rack // unit_capacity), 1)

            while remaining_units > 0:
                units_this_rack = min(remaining_units, max_units_per_rack)

                cap = units_this_rack * unit_capacity
                suffix = f" [{split_index}]"
                unique_name = name + suffix

                placed = False
                for rack in rack_list:
                    if rack["capacity"] + cap <= max_capacity_per_rack:
                        rack["units"].append({'name': unique_name, 'capacity': cap})
                        rack["capacity"] += cap
                        placed = True
                        break

                if not placed:
                    new_rack = {"units": [{'name': unique_name, 'capacity': cap}], "capacity": cap}
                    rack_list.append(new_rack)

                new_item = item.copy()
                new_item['total_rated_capacity'] = cap
                new_item['assigned_rack'] = len(rack_list)
                new_item['assigned_units'] = units_this_rack
                new_item['osm_name'] = unique_name
                data[unique_name] = new_item

                remaining_units -= units_this_rack
                split_index += 1

        else:
            # Fits into a rack as-is
            if 'unit_length' in item:  # Case
                unit_capacity = rated_capacity * unit_length
            else:  # Walk-in
                unit_capacity = rated_capacity
            
            unique_name = name
            placed = False
            
            for rack in rack_list:
                if rack["capacity"] + cap <= max_capacity_per_rack:
                    rack["units"].append({'name': unique_name, 'capacity': cap})
                    rack["capacity"] += cap
                    placed = True
                    break
            if not placed:
                new_rack = {"units": [{'name': unique_name, 'capacity': cap}], "capacity": cap}
                rack_list.append(new_rack)

            data[unique_name]['assigned_rack'] = len(rack_list)
            data[unique_name]['assigned_units'] = unit_count
            data[unique_name]['osm_name'] = unique_name

    # Finalize racks
    for i, rack in enumerate(rack_list, start=1):
        for unit in rack["units"]:
            base_name = unit["name"]
            if base_name in data:
                data[base_name]['assigned_rack'] = i
        racks.append(rack["units"])

    print("📦 Final distributed unit keys:")
    for k in data.keys():
        print(" -", k)
    
    print("\n🎯 Assigned unit count per object:")
    for k, v in data.items():
        print(f"{k}: assigned_units = {v.get('assigned_units')}, capacity = {v.get('total_rated_capacity')}")

    
    print("✅ Assigned rack units:")
    for name, item in data.items():
        print(f" - {name}: rack {item.get('assigned_rack')}, assigned_units = {item.get('assigned_units')}")

            
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

    # Split units by operation type (using osm_name)
    mt_case_data = {name: item for name, item in case_data.items() if item.get('operation_type') == 'MT'}
    mt_walkin_data = {name: item for name, item in walkin_data.items() if item.get('operation_type') == 'MT'}
    lt_case_data = {name: item for name, item in case_data.items() if item.get('operation_type') == 'LT'}
    lt_walkin_data = {name: item for name, item in walkin_data.items() if item.get('operation_type') == 'LT'}

    # Combine for full MT and LT assignment
    mt_combined = {**mt_case_data, **mt_walkin_data}
    lt_combined = {**lt_case_data, **lt_walkin_data}

    # Initialize rack containers
    mt_racks = []
    lt_racks = []

    # Assign racks (FFD greedy logic assumed)
    distribute_units(mt_combined, mt_racks, max_mt_capacity)
    distribute_units(lt_combined, lt_racks, max_lt_capacity)

    # Update original data with rack assignments
    case_data.update(mt_case_data)
    case_data.update(lt_case_data)
    walkin_data.update(mt_walkin_data)
    walkin_data.update(lt_walkin_data)

    # Attach osm_name to each unit in result for clarity
    for name, item in case_data.items():
        item["osm_name"] = name
    for name, item in walkin_data.items():
        item["osm_name"] = name
    
    for item in case_data.values():
        if 'assigned_units' not in item:
            item['assigned_units'] = item.get('unit_count') or item.get('number_of_units') or 1

    for item in walkin_data.values():
        if 'assigned_units' not in item:
            item['assigned_units'] = item.get('number_of_units') or item.get('unit_count') or 1

    return mt_racks, lt_racks, case_data, walkin_data


def display_rack_capacity(racks, selected_units, case_or_walkin_data, rack_type=""):
    print(f"\n{rack_type} Racks:")

    for i, rack in enumerate(racks, 1):
        total_capacity = sum(item['capacity'] for item in rack)
        print(f"Rack {i}: Total Capacity = {total_capacity:.2f} W")

        for item in rack:
            original_name = item['name']
            cap = item['capacity']

            obj_data = case_or_walkin_data.get(original_name)

            unit_count_est = ""
            if obj_data and "assigned_units" in obj_data:
                unit_count_est = f" ({int(obj_data['assigned_units'])} units)"

            print(f"  - {original_name} : {cap:.2f} W{unit_count_est}")

        print()

         