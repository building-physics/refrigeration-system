from pathlib import Path
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "database" / "openstudio_refrigeration_system.db"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session")
def db_path():
    assert DB_PATH.is_file(), f"Database not found: {DB_PATH}"
    return str(DB_PATH)


@pytest.fixture(params=("old", "new", "advanced"))
def template(request):
    return request.param

