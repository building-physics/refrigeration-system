# Refrigeration System Validation Tests

Copy the `tests` folder, `pytest.ini`, `requirements-test.txt`, and `.github`
folder into the root of the `refrigeration-system` repository. The expected
repository layout is:

```text
refrigeration-system/
|-- database/
|   `-- openstudio_refrigeration_system.db
|-- refrigeration/
|   |-- building_unit.py
|   |-- compressor.py
|   |-- condenser.py
|   `-- ...
|-- tests/
|-- main.ipynb
|-- pytest.ini
`-- requirements-test.txt
```

## Run on Windows

From the repository root:

```powershell
py -m pip install -r requirements-test.txt
py -m pytest -q
```

Successful output will look similar to:

```text
........................
47 passed
```

If a test fails, pytest reports the exact calculation, object reference, DB
mapping, or file that did not match the expected behavior.

## What is validated

- Required SQLite tables and columns exist.
- Old, New, and Advanced each map to 14 cases and 10 walk-ins.
- Every building mapping resolves to a real case or walk-in DB row.
- Capacity and power curves exist for MT and LT.
- Reference COP is calculated from the DB curves at the documented SST/SCT.
- Compressor generation preserves the intentional minimum of 15 compressors.
- Rack loads preserve the total selected refrigeration load.
- Rack target-capacity overages produce the intended warning without stopping.
- Condenser capacity uses the DB-derived reference COP and the 20% sizing factor.
- The complete JSON object graph has unique names and valid curve, condenser,
  case/walk-in-list, and case/walk-in references.
- The main notebook passes `db_path` to every DB-dependent compressor and
  condenser function and initializes the selected mode.

The test suite validates software behavior and internal model consistency. A
separate OpenStudio/EnergyPlus simulation check is still needed to validate
physical results and confirm that no Severe or Fatal errors are produced.
