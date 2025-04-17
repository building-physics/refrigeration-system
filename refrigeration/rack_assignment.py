from refrigeration.db_utils import get_data_from_db

# distribution units using greedy algorithm
def distribute_units(data, racks, max_capacity_per_rack):
    units = sorted(
        data.items(),
        key=lambda x: x[1].get('total_rated_capacity', x[1].get('rated_capacity', 0)),
        reverse=True
    )

    rack_list = []

    for name, item in units:
        rated_capacity = item.get('rated_capacity')
        unit_count = item.get('unit_count') or item.get('number_of_units')

        if not rated_capacity or not unit_count:
            continue

        if rated_capacity * unit_count > max_capacity_per_rack:
            remaining_units = unit_count
            split_index = 1
            max_units_per_rack = int(max_capacity_per_rack // rated_capacity)

            while remaining_units > 0:
                units_this_rack = min(remaining_units, max_units_per_rack)
                cap = units_this_rack * rated_capacity
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
                data[unique_name] = new_item

                remaining_units -= units_this_rack
                split_index += 1
        else:
            cap = rated_capacity * unit_count
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

    return mt_racks, lt_racks, case_data, walkin_data

def display_rack_capacity(racks, selected_units, case_or_walkin_data, rack_type=""):
    print(f"\n{rack_type} Racks:")

    name_to_osm = {unit.osm_name: unit.osm_name for unit in selected_units}

    for i, rack in enumerate(racks, 1):
        total_capacity = sum(item['capacity'] for item in rack)
        print(f"Rack {i}: Total Capacity = {total_capacity:.2f} W")
        for item in rack:
            original_name = item['name']
            cap = item['capacity']

            base_name = original_name.split(" [")[0]
            suffix = " [" + original_name.split(" [")[1] if " [" in original_name else ""

            if original_name in name_to_osm:
                osm_display = name_to_osm[original_name]
            elif base_name in name_to_osm:
                osm_display = name_to_osm[base_name] + suffix
            else:
                osm_display = original_name

            rated = case_or_walkin_data.get(original_name, {}).get('rated_capacity')
            if not rated:
                rated = case_or_walkin_data.get(base_name, {}).get('rated_capacity')

            unit_count_est = ""
            if rated:
                n = int(round(cap / rated))
                unit_count_est = f" ({n} units)"

            print(f"  - {osm_display} : {cap:.2f} W{unit_count_est}")
        print()