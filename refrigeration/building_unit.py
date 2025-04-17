import sqlite3
ZONE_MAPPING = {
    "SuperMarket":{
        "case_zone": "MainSales",
        "walkin_zone": "ActiveStorage"
    },
    "ConvenienceStore": {
        "case_zone": "conv_casezone",
        "walkin_zone": "conv_walkinzone"
    }
}

BUILDING_LABELS = {
    "SuperMarket": "SuperMarket",
    "ConvenienceStore": "Convenience Store (Not Available yet)"
}

class BuildingUnit:
    def __init__(self, building_type, base_name, category, number_of_units=None, template=None, user_mode=False, zone_name=None):
        self.building_type = building_type
        self.base_name = base_name.strip()
        self.category = category
        self.template = template
        self.user_mode = user_mode
        self.zone_name = zone_name or ("MainSales" if "walk-in" not in base_name.lower() else "ActiveStorage")
        self.number_of_units = number_of_units if number_of_units is not None else 1

        base_clean = self.base_name.replace(",", "")

        # Define naming conventions
        self.case_name = f"{self.template} {base_clean}"
        self.walkin_name = f"{self.template} {base_clean}"

        if self.user_mode:
            self.osm_name = f"User {self.template} {base_clean}"
        else:
            self.osm_name = f"{self.building_type} {self.template} {base_clean} - {self.category}"

    def __repr__(self):
        return f'"osm name": "{self.osm_name}", "case_name": "{self.case_name}", "number_of_units": {self.number_of_units}'


class SuperMarketSystem:
    def __init__(self, system_type, db_path):
        self.building_type = "SuperMarket"
        self.system_type = system_type
        self.db_path = db_path
        self.cases = []
        self.walkins = []

    def load_defaults(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Load case units
        cursor.execute("""
            SELECT base_name, category, number_of_units
            FROM building_category_mapping
            WHERE building_type = 'SuperMarket' AND system_type = 'case' AND template = ?;
        """, (self.system_type,))
        case_results = cursor.fetchall()
        self.cases = [BuildingUnit(self.building_type, base, category, qty, self.system_type) for base, category, qty in case_results]

        # Load walk-in units
        cursor.execute("""
            SELECT base_name, category
            FROM building_category_mapping
            WHERE building_type = 'SuperMarket' AND system_type = 'walkin' AND template = ?;
        """, (self.system_type,))
        walkin_results = cursor.fetchall()
        self.walkins = [BuildingUnit(self.building_type, base, category, template=self.system_type) for base, category in walkin_results]

        conn.close()