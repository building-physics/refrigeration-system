from refrigeration.building_unit import (
    BUILDING_SUPERMARKET,
    SuperMarketSystem,
)


def test_internal_building_key_matches_database():
    assert BUILDING_SUPERMARKET == "SuperMarket"


def test_supermarket_defaults_load(db_path, template):
    system = SuperMarketSystem(template, db_path)
    system.load_defaults()

    assert len(system.cases) == 14
    assert len(system.walkins) == 10
    assert all(unit.template == template for unit in system.cases)
    assert all(unit.template == template for unit in system.walkins)
    assert len({unit.osm_name for unit in system.cases}) == 14
    assert len({unit.osm_name for unit in system.walkins}) == 10

