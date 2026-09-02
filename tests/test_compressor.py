import pytest

from refrigeration.compressor import (
    calculate_compressors_for_racks,
    generate_compressor_objects,
    get_compressor_specs,
    load_and_print_compressor_curves,
)


EXPECTED_COP = {
    ("old", "MT"): 2.1152,
    ("old", "LT"): 1.4357,
    ("new", "MT"): 2.4667,
    ("new", "LT"): 1.7594,
    ("advanced", "MT"): 2.7975,
    ("advanced", "LT"): 1.8320,
}


@pytest.mark.parametrize("operation_type", ("MT", "LT"))
def test_reference_specs_come_from_db(db_path, template, operation_type):
    capacity, power, cop, eer = get_compressor_specs(
        db_path, template, operation_type
    )
    assert capacity > 0
    assert power > 0
    assert cop == pytest.approx(EXPECTED_COP[(template, operation_type)], abs=5e-4)
    assert eer == pytest.approx(cop * 3.412141633)


def test_compressor_generation_uses_both_curves_and_minimum_15(db_path, template):
    mt_power, mt_capacity, _, _ = load_and_print_compressor_curves(
        db_path, template, verbose=False
    )
    rack_info = [{
        "rack_number": 1,
        "rack_load": 10_000.0,
        "compressors_needed": 1,
    }]
    objects = generate_compressor_objects(
        rack_info, template, "MT", db_path,
        power_curve_json=mt_power,
        capacity_curve_json=mt_capacity,
    )

    assert len(objects) == 15
    assert len({obj["name"] for obj in objects}) == 15
    assert all(obj["RatedCapacity"] > 0 for obj in objects)
    assert all(obj["RatedPowerConsumption"] > 0 for obj in objects)
    assert all(
        obj["RefrigerationCompressorPowerCurveName"] == mt_power["name"]
        for obj in objects
    )
    assert all(
        obj["RefrigerationCompressorCapacityCurveName"] == mt_capacity["name"]
        for obj in objects
    )


def test_compressor_count_uses_db_reference_capacity(db_path, template):
    capacity, _, _, _ = get_compressor_specs(db_path, template, "MT")
    racks = [[{"name": "synthetic", "capacity": 1.5 * capacity}]]
    result = calculate_compressors_for_racks(
        racks, "MT", template, db_path, redundancy=True
    )
    assert result[0]["compressors_needed"] == 3

