from refrigeration.db_utils import get_data_from_db
def assign_racks_to_cases_and_walkins(db_path, selected_case_units, selected_walkin_units, default_max_capacity=30000):
    # get case and walkin data from DB
    case_data, walkin_data = get_data_from_db(db_path, selected_case_units, selected_walkin_units)

    # Determine template from selected units
    template = None
    if selected_case_units:
        template = selected_case_units[0].template.lower()
    elif selected_walkin_units:
        template = selected_walkin_units[0].template.lower()

    # Set MT and LT limits based on template
    if template == "advanced":
        max_mt_capacity = 30000
        max_lt_capacity = 15000
    elif template in ["old", "new"]:
        max_mt_capacity = 50000
        max_lt_capacity = 25000
    else:
        max_mt_capacity = max_lt_capacity = default_max_capacity  # fallback    

    # assign cases and walkins to MT rack and LT rack
    mt_racks = []
    lt_racks = []

    def distribute_units(data, racks, max_capacity_per_rack, is_walkin=False):
        units = sorted(
            data.items(),
            key=lambda x: x[1].get('total_rated_capacity', x[1].get('rated_capacity', 0)),
            reverse=True
        )

        current_rack = []
        current_capacity = 0
        rack_index = 1

        for name, item in units:
            total_capacity = item.get('total_rated_capacity') or item.get('rated_capacity')

            if current_capacity + total_capacity <= max_capacity_per_rack:
                current_rack.append({'name': name, 'capacity': total_capacity})
                current_capacity += total_capacity
            else:
                if current_rack:
                    for unit in current_rack:
                        if unit['name'] in data:
                            data[unit['name']]['assigned_rack'] = rack_index
                    racks.append(current_rack)
                    rack_index += 1
                current_rack = [{'name': name, 'capacity': total_capacity}]
                current_capacity = total_capacity

        if current_rack:
            for unit in current_rack:
                if unit['name'] in data:
                    data[unit['name']]['assigned_rack'] = rack_index
            racks.append(current_rack)

    mt_case_data = {name: item for name, item in case_data.items() if item.get('operation_type') == 'MT'}
    mt_walkin_data = {name: item for name, item in walkin_data.items() if item.get('operation_type') == 'MT'}
    lt_case_data = {name: item for name, item in case_data.items() if item.get('operation_type') == 'LT'}
    lt_walkin_data = {name: item for name, item in walkin_data.items() if item.get('operation_type') == 'LT'}

    # combine MT/LT data
    mt_combined = {**mt_case_data, **mt_walkin_data}
    lt_combined = {**lt_case_data, **lt_walkin_data}

    # Assign to MT/LT racks and embed rack numbers
    distribute_units(mt_combined, mt_racks, max_mt_capacity)
    distribute_units(lt_combined, lt_racks, max_lt_capacity)

    # Update case_data and walkin_data with assigned rack info
    case_data.update(mt_case_data)
    case_data.update(lt_case_data)
    walkin_data.update(mt_walkin_data)
    walkin_data.update(lt_walkin_data)

    return mt_racks, lt_racks, case_data, walkin_data

def display_rack_capacity(racks, selected_units, rack_type=""):
    print(f"\n{rack_type} Racks:")
    name_to_osm = {}
    for unit in selected_units:
        name_to_osm[unit.case_name] = unit.osm_name
        name_to_osm[unit.walkin_name] = unit.osm_name  # walkin도 포함

    for i, rack in enumerate(racks, 1):
        total_capacity = sum(item['capacity'] for item in rack)
        print(f"Rack {i}: Total Capacity = {total_capacity:.2f} W")
        for item in rack:
            original_name = item['name']
            osm_display = name_to_osm.get(original_name, original_name)  # fallback 처리
            print(f"  - {osm_display} : {item['capacity']:.2f} W")
        print()