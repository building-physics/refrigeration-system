# Refrigeration Module
This folder contains the core Python modules for building and exporting OpenStudio-compatible refrigeration system objects. Each file handles a specific part of the modeling pipeline, from data access to JSON export.

**This is a work in progress.**

## Folder Structure

```
refrigeration/
├── __init__.py               # Initializes the package
├── building_unit.py          # Defines building units and naming logic
├── mode_selection.py         # Automated and user-defined system setup
├── json_io.py                # Export functions for refrigeration JSON files
├── db_utils.py               # Load case and walk-in data from DB
├── compressor.py             # Compressor generation and curve logic
├── condenser.py              # Condenser and fan curve generation
├── rack_assignment.py        # Assigns cases/walk-ins to MT/LT racks
├── case_walkin_objects.py    # Create refrigeration case and walk-in objects
├── system_objects.py         # Build system structure and object lists
├── full_export.py            # Export complete system JSON
└── utils.py                  # Utility functions for formatting and naming
```

## Module Overview

- **`__init__.py`**  
  Initializes the module namespace for import use.

- **`building_unit.py`**  
  Defines building unit metadata and naming logic for refrigeration objects.

- **`case_walkin_objects.py`**  
  Handles creation of case and walk-in objects using template-specific data.

- **`compressor.py`**  
  Generates compressor objects and performance curves based on template and suction type (MT/LT).

- **`condenser.py`**  
  Builds condenser and fan components with appropriate performance characteristics.

- **`db_utils.py`**  
  Provides utilities for loading refrigeration data from the database (cases, walk-ins, etc).

- **`full_export.py`**  
  Coordinates the full export process of refrigeration systems into OpenStudio JSON format.

- **`json_io.py`**  
  Reads and writes JSON files for compressor, condenser, system, case, walkin objects.

- **`mode_selection.py`**  
  Implements logic for selecting automated or user-defined modes and associated configurations.

- **`rack_assignment.py`**  
  Assigns refrigeration racks based on thermal loads and operation type groupings.

- **`system_objects.py`**  
  Builds high-level system objects (e.g., operation type, refrigeration systems) and links components together.

- **`utils.py`**  
  Helper functions used across modules for formatting, naming, and conversions.

---