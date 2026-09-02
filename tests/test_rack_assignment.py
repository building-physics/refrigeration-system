import pytest

from refrigeration.building_unit import SuperMarketSystem
from refrigeration.rack_assignment import (
    assign_racks_to_cases_and_walkins,
    distribute_units,
)


CASE_DATA_KEYS = {
    "case_name", "template", "operation_type", "rated_capacity",
    "unit_length", "case_operating_temperature", "evaporator_temperature",
    "defrost_schedule", "drip_down_schedule", "case_lighting_schedule",
    "defrost_power", "defrost_time", "dripdown_time",
    "number_of_defrost_per_day",
}

WALKIN_DATA_KEYS = {
    "walkin_name", "template", "operation_type", "insulated_floor_area",
    "rated_capacity", "rated_cooling_source_temperature",
    "rated_total_heating_power", "defrost_power",
    "insulated_floor_uvalue", "total_insulatedsurface_area_facing_zone",
    "height_of_stocking_doors_facing_zone", "defrost_time",
    "drip_down_time", "number_of_defrost_per_day",
}


def test_rack_assignment_preserves_total_load_and_db_fields(db_path, template):
    system = SuperMarketSystem(template, db_path)
    system.load_defaults()
    mt_racks, lt_racks, case_data, walkin_data = (
        assign_racks_to_cases_and_walkins(
            db_path, system.cases, system.walkins
        )
    )

    expected_mt = sum(
        item["total_rated_capacity"]
        for item in (*case_data.values(), *walkin_data.values())
        if item["operation_type"] == "MT"
    )
    expected_lt = sum(
        item["total_rated_capacity"]
        for item in (*case_data.values(), *walkin_data.values())
        if item["operation_type"] == "LT"
    )
    actual_mt = sum(item["capacity"] for rack in mt_racks for item in rack)
    actual_lt = sum(item["capacity"] for rack in lt_racks for item in rack)

    assert actual_mt == pytest.approx(expected_mt)
    assert actual_lt == pytest.approx(expected_lt)
    assert all(CASE_DATA_KEYS <= set(item) for item in case_data.values())
    assert all(WALKIN_DATA_KEYS <= set(item) for item in walkin_data.values())


def test_rack_target_overage_warns_but_does_not_stop(capsys):
    data = {
        "large group": {
            "rated_capacity": 130.0,
            "number_of_units": 1,
        },
        "small group": {
            "rated_capacity": 10.0,
            "number_of_units": 1,
        },
    }
    racks = []
    distribute_units(data, racks, max_capacity_per_rack=100.0)
    output = capsys.readouterr().out

    assert "REVIEW REQUIRED" in output
    assert len(racks) == 2
    assert sum(item["capacity"] for item in racks[0]) == pytest.approx(130.0)

