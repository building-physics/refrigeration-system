import json

import pytest

from refrigeration.building_unit import SuperMarketSystem
from refrigeration.case_walkin_objects import (
    prepare_and_store_case_and_walkin_objects,
)
from refrigeration.compressor import (
    prepare_and_store_compressor_objects,
    summarize_compressor_assignment,
)
from refrigeration.condenser import prepare_and_store_condenser_objects
from refrigeration.full_export import export_full_refrigeration_system_to_json
from refrigeration.rack_assignment import assign_racks_to_cases_and_walkins
from refrigeration.system_objects import (
    prepare_and_store_system_and_casewalkin_lists,
)
from refrigeration.utils import set_mode


def _build_complete_model(db_path, template, output_path):
    selected = SuperMarketSystem(template, db_path)
    selected.load_defaults()

    mt_racks, lt_racks, case_data, walkin_data = (
        assign_racks_to_cases_and_walkins(
            db_path, selected.cases, selected.walkins
        )
    )
    case_walkin = prepare_and_store_case_and_walkin_objects(
        case_data, walkin_data, selected.cases, selected.walkins,
        "MainSales", "ActiveStorage",
    )
    mt_info, lt_info = summarize_compressor_assignment(
        mt_racks, lt_racks, template, db_path
    )
    compressor = prepare_and_store_compressor_objects(
        mt_info, lt_info, template, db_path
    )
    condenser = prepare_and_store_condenser_objects(
        mt_info, lt_info, template, db_path
    )
    systems = prepare_and_store_system_and_casewalkin_lists(
        selected.cases, selected.walkins, mt_racks, lt_racks, template
    )

    set_mode("automated")
    export_full_refrigeration_system_to_json(
        mt_compressors=compressor["mt_compressors"],
        lt_compressors=compressor["lt_compressors"],
        mt_power_curve=compressor["mt_power_curve"],
        mt_capacity_curve=compressor["mt_capacity_curve"],
        lt_power_curve=compressor["lt_power_curve"],
        lt_capacity_curve=compressor["lt_capacity_curve"],
        mt_condensers=condenser["mt_condensers"],
        lt_condensers=condenser["lt_condensers"],
        mt_curves=condenser["mt_curves"],
        lt_curves=condenser["lt_curves"],
        case_objects=case_walkin["case_objects"],
        walkin_objects=case_walkin["walkin_objects"],
        system_and_casewalkin_objects=systems,
        case_zone_name="MainSales",
        walkin_zone_name="ActiveStorage",
        output_path=str(output_path),
    )
    return json.loads(output_path.read_text(encoding="utf-8"))


def _assert_reference_exists(owner, field, names):
    reference = owner.get(field)
    assert reference, f"Missing {field} in {owner.get('name')}"
    assert reference in names, (
        f"{owner.get('name')} references missing {field}: {reference}"
    )


def test_complete_automated_model_has_valid_object_graph(
    db_path, template, tmp_path
):
    document = _build_complete_model(
        db_path, template, tmp_path / f"{template}_full.json"
    )
    objects = document["objects"]
    names = {obj["name"] for obj in objects if obj.get("name")}
    named_objects = [obj for obj in objects if obj.get("name")]

    assert document["Building"] == "SuperMarket"
    assert len(names) == len(named_objects), "Duplicate object names found"

    for obj in objects:
        if obj.get("type") == "OS:Refrigeration:Compressor":
            _assert_reference_exists(
                obj, "RefrigerationCompressorPowerCurveName", names
            )
            _assert_reference_exists(
                obj, "RefrigerationCompressorCapacityCurveName", names
            )
        elif obj.get("type") == "OS:Refrigeration:Condenser:AirCooled":
            _assert_reference_exists(obj, "FanPowerCurve", names)
        elif obj.get("type") == "OS:Refrigeration:System":
            _assert_reference_exists(obj, "CondenserName", names)
            _assert_reference_exists(obj, "CaseAndWalkInListName", names)
        elif obj.get("type") == "OS:Refrigeration:CaseAndWalkInList":
            for reference in obj.get("CaseAndWalkInNames", []):
                assert reference in names, (
                    f"{obj['name']} references missing case/walk-in: {reference}"
                )

    assert sum(obj.get("type") == "OS:Refrigeration:Case" for obj in objects) == 14
    assert sum(obj.get("type") == "OS:Refrigeration:WalkIn" for obj in objects) == 10

