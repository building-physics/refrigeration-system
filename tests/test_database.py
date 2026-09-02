import sqlite3

import pytest


REQUIRED_TABLES = {
    "building_category_mapping",
    "refrigeration_cases",
    "refrigeration_walkins",
    "refrigeration_compressors",
}

CASE_COLUMNS = {
    "case_name", "template", "operation_type", "rated_capacity",
    "unit_length", "case_operating_temperature", "evaporator_temperature",
    "fan_power", "lighting_power", "defrost_type", "defrost_schedule",
    "drip_down_schedule", "case_lighting_schedule", "defrost_power",
    "defrost_time", "dripdown_time", "number_of_defrost_per_day",
}

WALKIN_COLUMNS = {
    "walkin_name", "template", "operation_type", "insulated_floor_area",
    "rated_capacity", "operating_temperature",
    "rated_cooling_source_temperature", "rated_total_heating_power",
    "rated_cooling_fan_power", "lighting_power", "lighting_schedule",
    "defrost_type", "defrost_control_type", "defrost_schedule",
    "drip_down_schedule", "defrost_power", "insulated_floor_uvalue",
    "total_insulatedsurface_area_facing_zone",
    "insulated_surface_uvalue_facing_zone", "defrost_time",
    "drip_down_time", "number_of_defrost_per_day",
}


def _columns(conn, table):
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def test_required_tables_and_columns_exist(db_path):
    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        assert REQUIRED_TABLES <= tables
        assert CASE_COLUMNS <= _columns(conn, "refrigeration_cases")
        assert WALKIN_COLUMNS <= _columns(conn, "refrigeration_walkins")


@pytest.mark.parametrize("template", ("old", "new", "advanced"))
def test_supermarket_mapping_counts(db_path, template):
    with sqlite3.connect(db_path) as conn:
        rows = dict(conn.execute(
            """
            SELECT system_type, COUNT(*)
            FROM building_category_mapping
            WHERE building_type = 'SuperMarket' AND template = ?
            GROUP BY system_type
            """,
            (template,),
        ))
    assert rows == {"case": 14, "walkin": 10}


@pytest.mark.parametrize("template", ("old", "new", "advanced"))
def test_every_mapping_resolves_to_equipment(db_path, template):
    with sqlite3.connect(db_path) as conn:
        missing_cases = conn.execute(
            """
            SELECT m.base_name
            FROM building_category_mapping AS m
            LEFT JOIN refrigeration_cases AS c
              ON lower(c.case_name) = lower(m.template || ' ' || m.base_name)
            WHERE m.building_type = 'SuperMarket'
              AND m.template = ? AND m.system_type = 'case'
              AND c.case_name IS NULL
            """,
            (template,),
        ).fetchall()
        missing_walkins = conn.execute(
            """
            SELECT m.base_name
            FROM building_category_mapping AS m
            LEFT JOIN refrigeration_walkins AS w
              ON lower(w.walkin_name) = lower(m.template || ' ' || m.base_name)
            WHERE m.building_type = 'SuperMarket'
              AND m.template = ? AND m.system_type = 'walkin'
              AND w.walkin_name IS NULL
            """,
            (template,),
        ).fetchall()
    assert missing_cases == []
    assert missing_walkins == []


@pytest.mark.parametrize("template", ("old", "new", "advanced"))
def test_compressor_curve_matrix_is_complete(db_path, template):
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT operation_type, curve_type, COUNT(*)
            FROM refrigeration_compressors
            WHERE template = ?
            GROUP BY operation_type, curve_type
            """,
            (template,),
        ).fetchall()
    assert {(op, curve) for op, curve, count in rows if count == 1} == {
        ("MT", "capacity"), ("MT", "power"),
        ("LT", "capacity"), ("LT", "power"),
    }


def test_conditional_walkin_nulls_are_consistent(db_path):
    with sqlite3.connect(db_path) as conn:
        bad_reachin = conn.execute(
            """
            SELECT COUNT(*) FROM refrigeration_walkins
            WHERE reachin_door_uvalue IS NULL
              AND area_of_glass_reachin_doors_facing_zone <> 0
            """
        ).fetchone()[0]
        bad_defrost = conn.execute(
            """
            SELECT COUNT(*) FROM refrigeration_walkins
            WHERE defrost_type = 'Electric'
              AND (defrost_time IS NULL OR drip_down_time IS NULL
                   OR number_of_defrost_per_day IS NULL)
            """
        ).fetchone()[0]
    assert bad_reachin == 0
    assert bad_defrost == 0

