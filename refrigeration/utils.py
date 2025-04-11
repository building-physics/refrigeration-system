import sqlite3
# define the building type (SuperMarket or User Defined System)
def get_building_name():
    mode = globals().get("mode", "user").lower()
    return "SuperMarket" if mode == "automated" else "User Defined System"



# get SST (Saturated Suction Temperature)
def get_suction_temp(template, operation_type):
    """
    Return SST (Suction Temperature) for given template and operation type.
    These values are fixed regardless of template as per latest specification.
    """
    if operation_type == "MT":
        return -6.6667
    elif operation_type == "LT":
        return -31.67
    else:
        raise ValueError(f"Invalid operation type: {operation_type}")
    
# get SCT (Saturated Condensing Temperature)
def get_min_condensing_temp(template, operation_type):
    """
    Return SCT (Minimum Condensing Temperature) for given template and operation type.
    These values are fixed regardless of template as per latest specification.
    """
    if operation_type == "MT":
        return 48.8889
    elif operation_type == "LT":
        return 40.56
    else:
        raise ValueError(f"Invalid operation type: {operation_type}")

def clean_name(name, prefix_to_remove):
    if name.lower().startswith(prefix_to_remove):
        return name[len(prefix_to_remove):]
    return name

def generate_available_units_markdown(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT case_name FROM refrigeration_cases ORDER BY case_name")
    case_rows = cur.fetchall()
    cur.execute("SELECT DISTINCT walkin_name FROM refrigeration_walkins ORDER BY walkin_name")
    walkin_rows = cur.fetchall()
    conn.close()

    oldnew_cases = sorted(set(clean_name(row[0], prefix) for row in case_rows
                              for prefix in ['old ', 'new '] if row[0].lower().startswith(prefix)))
    advanced_cases = sorted(set(clean_name(row[0], 'advanced ') for row in case_rows
                                if row[0].lower().startswith('advanced ')))

    oldnew_walkins = sorted(set(clean_name(row[0], prefix) for row in walkin_rows
                                for prefix in ['old ', 'new '] if row[0].lower().startswith(prefix)))
    advanced_walkins = sorted(set(clean_name(row[0], 'advanced ') for row in walkin_rows
                                  if row[0].lower().startswith('advanced ')))

    markdown = "## 🧊 Available Refrigeration Units\n\n"
    markdown += "### 🔹 For **Old/New System Templates**\n"
    markdown += "**Available Cases:**\n"
    markdown += "\n".join(f"- {name}" for name in oldnew_cases) or "- (None found)"
    markdown += "\n\n**Available Walk-ins:**\n"
    markdown += "\n".join(f"- {name}" for name in oldnew_walkins) or "- (None found)"
    markdown += "\n\n---\n\n"
    markdown += "### 🔸 For **Advanced System Template**\n"
    markdown += "**Available Cases:**\n"
    markdown += "\n".join(f"- {name}" for name in advanced_cases) or "- (None found)"
    markdown += "\n\n**Available Walk-ins:**\n"
    markdown += "\n".join(f"- {name}" for name in advanced_walkins) or "- (None found)"

    return markdown