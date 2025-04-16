from .building_unit import BuildingUnit, SuperMarketSystem, ZONE_MAPPING, BUILDING_LABELS

def get_valid_template():
    valid_templates = ["old", "new", "advanced"]
    template = input("Choose template (old/new/advanced): ").lower()
    while template not in valid_templates:
        print("Invalid template. Please choose from 'old', 'new', or 'advanced'.")
        template = input("Choose template (old/new/advanced): ").lower()
    return template


def select_test_mode():
    mode = input("Select test mode (user/automated): ").lower()
    while mode not in ["user", "automated"]:
        print("Invalid mode. Please choose from 'user' or 'automated'.")
        mode = input("Select test mode (user/automated): ").lower()
    return mode


def user_mode():
    selected_case_units = []
    selected_walkin_units = []
    selected_template = get_valid_template()

    print("\n--- Add Case Units ---")
    while True:
        case_name = input("Enter case name (or 'done' to finish): ")
        if case_name.lower() == 'done':
            break
        try:
            number_of_units = int(input(f"Enter number of units for {case_name}: "))
        except ValueError:
            print("❌ Invalid number. Please enter an integer.")
            continue
        selected_case_units.append(
        BuildingUnit("User", f"{selected_template} {case_name}", "Category", number_of_units, template=selected_template, user_mode=True)
        )

    print("\n--- Add Walk-in Units ---")
    while True:
        walkin_name = input("Enter walk-in name (or 'done' to finish): ")
        if walkin_name.lower() == 'done':
            break
        try:
            number_of_units = int(input(f"Enter number of units for {walkin_name}: "))
        except ValueError:
            print("❌ Invalid number. Please enter an integer.")
            continue
        selected_walkin_units.append(
            BuildingUnit("User", f"{selected_template} {walkin_name}", "Category", number_of_units, template=selected_template, user_mode=True)
        )
    
    print("\n--- Add Zone names ---")
    case_zone_name = input("Enter zone name for refrigeration *cases* [default: MainSales]: ").strip()
    if not case_zone_name:
        case_zone_name = "MainSales"
    walkin_zone_name = input("Enter zone name for *walkins* [default: ActiveStorage]: ").strip()
    if not walkin_zone_name:
        walkin_zone_name = "ActiveStorage"


    return selected_case_units, selected_walkin_units, selected_template, case_zone_name, walkin_zone_name


def automated_mode(db_path):
    building_types = list(BUILDING_LABELS.keys())

    print("Choose building type:")
    for idx, building_type in enumerate(building_types, 1):
        print(f"{idx}. {BUILDING_LABELS[building_type]}") 
    
    choice = int(input("Enter the number of your choice: "))
    while choice < 1 or choice > len(building_types):
        print("Invalid choice. Please try again.")
        choice = int(input("Enter the number of your choice: "))
    
    selected_building_type = building_types[choice - 1]
    print(f"Chosen building type: {BUILDING_LABELS[selected_building_type]}")
    
    selected_template = get_valid_template()

    system = None
    if selected_building_type == "SuperMarket":
        system = SuperMarketSystem(selected_template, db_path)
    elif selected_building_type == "Convenience Store":
        # Future placeholder
        raise NotImplementedError("Convenience Store system type is not yet supported.")
    
    # Zone mapping with default setting
    zone_map = ZONE_MAPPING.get(selected_building_type, {
        "case_zone": "MainSales",
        "walkin_zone": "ActiveStorage"
    })

    if system:
        system.load_defaults()
        selected_case_units = system.cases
        selected_walkin_units = system.walkins

        return selected_case_units, selected_walkin_units, selected_template

    return [], [], selected_template, "MainSales", "ActiveStorage"