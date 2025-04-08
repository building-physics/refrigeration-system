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