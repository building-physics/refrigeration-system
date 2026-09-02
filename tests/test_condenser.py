import pytest

from refrigeration.compressor import get_compressor_specs
from refrigeration.condenser import (
    generate_condenser_objects,
    prepare_and_store_condenser_objects,
)


@pytest.mark.parametrize("operation_type", ("MT", "LT"))
def test_condenser_uses_db_reference_cop(db_path, template, operation_type):
    load = 20_000.0
    rack_info = [{"rack_number": 1, "rack_load": load}]
    _, _, cop, _ = get_compressor_specs(
        db_path, template, operation_type
    )
    expected = round(1.2 * load * (1 + 1 / cop), 2)

    condensers, curves = generate_condenser_objects(
        rack_info, operation_type, template, db_path
    )

    assert len(condensers) == 1
    assert len(curves) == 1
    assert condensers[0]["RatedEffectiveTotalHeatRejectionRate"] == expected
    assert condensers[0]["FanPowerCurve"] == curves[0]["name"]
    assert curves[0]["Coefficient2x"] == pytest.approx(expected / 5.6)


def test_condenser_prepare_matches_rack_counts(db_path, template):
    mt_info = [
        {"rack_number": 1, "rack_load": 20_000.0},
        {"rack_number": 2, "rack_load": 10_000.0},
    ]
    lt_info = [{"rack_number": 1, "rack_load": 8_000.0}]
    result = prepare_and_store_condenser_objects(
        mt_info, lt_info, template, db_path
    )
    assert len(result["mt_condensers"]) == len(mt_info)
    assert len(result["lt_condensers"]) == len(lt_info)
    assert len(result["mt_curves"]) == len(mt_info)
    assert len(result["lt_curves"]) == len(lt_info)

