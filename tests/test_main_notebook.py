import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "main.ipynb"


def _notebook_calls():
    document = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    calls = []
    for cell in document.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        calls.extend(node for node in ast.walk(tree) if isinstance(node, ast.Call))
    return calls


def _named_calls(name):
    return [
        call for call in _notebook_calls()
        if isinstance(call.func, ast.Name) and call.func.id == name
    ]


def _passes_db_path(call):
    positional = any(
        isinstance(arg, ast.Name) and arg.id == "db_path"
        for arg in call.args
    )
    keyword = any(
        item.arg == "db_path"
        and isinstance(item.value, ast.Name)
        and item.value.id == "db_path"
        for item in call.keywords
    )
    return positional or keyword


def test_main_notebook_exists_and_is_valid_json():
    assert NOTEBOOK.is_file(), f"Notebook not found: {NOTEBOOK}"
    json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def test_main_sets_selected_mode():
    calls = _named_calls("set_mode")
    assert calls, "main.ipynb does not call set_mode(mode)"
    assert any(
        call.args
        and isinstance(call.args[0], ast.Name)
        and call.args[0].id == "mode"
        for call in calls
    )


def test_main_passes_db_path_to_compressor_workflow():
    for name in (
        "summarize_compressor_assignment",
        "prepare_and_store_compressor_objects",
    ):
        calls = _named_calls(name)
        assert calls, f"main.ipynb does not call {name}"
        assert all(_passes_db_path(call) for call in calls), (
            f"main.ipynb must pass db_path to {name}"
        )


def test_main_passes_db_path_to_condenser_workflow():
    calls = _named_calls("prepare_and_store_condenser_objects")
    assert calls, "main.ipynb does not call prepare_and_store_condenser_objects"
    assert all(_passes_db_path(call) for call in calls), (
        "main.ipynb must pass db_path to prepare_and_store_condenser_objects"
    )
