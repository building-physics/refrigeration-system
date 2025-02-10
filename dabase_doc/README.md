# Database Structure and Descriptions

The updated modularized refrigeration database features three distinct templates: **Old, New, and Advanced System**. Each template includes a variety of display cases and walk-in units.
**This is a work in progress**

## Field Descriptions with Units
This dataset includes refrigerated cases (`refrigeration_cases`), walk-in coolers (`refrigeration_walkins`), and compressor units (`refrigeration_compressors`).

---

## Refrigeration Cases (`refrigeration_cases`)
**Data headers, descriptions, and units for refrigerated cases**

| Field | Description | Unit |
|-------|------------|------|
| `case_name` | Unique identifier for the refrigerated case | N/A |
| `template` | Classification of the case as Old, New, or Advanced refrigeration system | N/A |
| `operation_type` | Indicates whether the case operates at Low Temperature (LT < -18°C) or Medium Temperature (MT -2°C to 4°C) | N/A |
| `rated_capacity` | Total full-load cooling capacity per unit length at rated conditions | W/m |
| `unit_length` | Physical length of an individual refrigerated case | m |
| `number_of_units` | Total number of refrigerated cases grouped together | N/A |
| `total_length` | Sum of all refrigerated case lengths in a given group | m |
| `total_capacity` | Full-load cooling capacity of all cases in the group per unit length under rated conditions | W/m |
| `case_operating_temperature` | Average internal air and product temperature within the refrigerated case during operation | °C |
| `evaporator_temperature` | Design evaporator coil or brine inlet temperature influencing heat exchange | °C |
| `rated_latent_heat_ratio` | Ratio of latent cooling capacity to total cooling capacity at rated conditions | N/A |
| `rated_runtime_fraction` | Expected fraction of operational runtime under rated conditions | N/A |
| `latent_case_credit_curve_type` | Defines curve used to adjust latent case credits at off-rated conditions | N/A |
| `latent_case_credit_curve_name` | Name of the cubic performance curve defining variation in latent case credit at off-rated conditions | N/A |
| `fan_power` | Power consumption of the case’s fans per unit length | W/m |
| `lighting_power` | Total lighting power required per unit length of the refrigerated case | W/m |
| `case_lighting_schedule` | Schedule governing when the case lighting operates | N/A |
| `fraction_of_lighting_energy_to_case` | Proportion of lighting energy contributing to the refrigerated case heat load | N/A |
| `anti_sweat_power` | Electric anti-sweat heater power per unit length of the refrigerated case | W/m |
| `anti_sweat_heater_control_type` | Method used to regulate the anti-sweat heaters | N/A |
| `fraction_of_anti_sweat_heater_energy_to_case` | Proportion of anti-sweat heater energy directly contributing to case heat load | N/A |
| `defrost_power` | Electrical power used for defrosting per unit length of the refrigerated case | W/m |
| `defrost_type` | Method of defrosting used | N/A |
| `defrost_schedule` | Schedule indicating when defrost cycles occur | N/A |
| `drip_down_schedules` | Indicates whether additional time is needed for condensate drainage after defrost | N/A |
| `defrost_energy_correction_curve_type` | Type of correction curve modifying defrost energy use at off-rated conditions | N/A |
| `defrost_energy_correction_curve_name` | Cubic performance curve defining defrost energy variation at different conditions | N/A |
| `HVAC_return_air_fraction` | Fraction of HVAC return air passing beneath the refrigerated case, if applicable | N/A |
| `restocking_schedule` | Schedule indicating when the refrigerated case is restocked with products | N/A |
| `case_credit_fraction_schedule` | Schedule defining the fraction of both sensible and latent case credits applied to the zone or HVAC return air | N/A |
---

## Walk-in Coolers (`refrigeration_walkins`)
**Data headers, descriptions, and units for walk-in coolers**

| Field | Description | Unit |
|-------|------------|------|
| `walkin_name` | Unique identifier for the walk-in cooler | N/A |
| `template` | Classification of the walk-in cooler as Old, New, or Advanced refrigeration system | N/A |
| `operation_type` | Identifies whether the walk-in cooler operates at Low Temperature (LT < -18°C) or Medium Temperature (MT -2°C to 4°C) | N/A |
| `insulated_floor_area` | Total insulated floor area of the walk-in cooler | m² |
| `rated_capacity` | Total full-load cooling capacity (sensible plus latent) at rated conditions | W |
| `operating_temperature` | Average internal air and product temperature maintained within the walk-in cooler | °C |
| `rated_cooling_source_temperature` | Temperature of the cooling source for the walk-in cooler | °C |
| `rated_total_heating_power` | Total heating power including anti-sweat, door, and floor heaters | W |
| `rated_cooling_fan_power` | Power consumption of the cooling coil fan | W |
| `lighting_power` | Total lighting power in the walk-in cooler | W |
| `lighting_schedule` | Schedule governing when the walk-in lighting operates | N/A |
| `defrost_type` | Method of defrosting used in the walk-in cooler | N/A |
| `defrost_control_type` | Control mechanism for defrosting operations | N/A |
| `defrost_schedule` | Schedule indicating when defrost cycles occur | N/A |
| `drip_down_schedule` | Indicates whether additional time is needed for condensate drainage after defrost | N/A |
| `defrost_power` | Power consumption for defrosting | W |
| `temperature_termination_defrost_fraction_to_ice` | Fraction of defrost energy contributing to ice melting | N/A |a
| `insulated_floor_uvalue` | Thermal transmittance (U-value) of the insulated floor | W/m²·K |
| `total_insulated_surface_area_facing_zone` | Total insulated surface area (walls and ceilings) facing the conditioned zone | m² |
| `insulated_surface_uvalue_facing_zone` | Thermal transmittance (U-value) of insulated surfaces facing the zone | W/m²·K |
| `area_of_glass_reachin_doors_facing_zone` | Total area of glass reach-in doors facing the conditioned zone | m² |
| `reachin_door_uvalue` | Thermal transmittance (U-value) of reach-in doors | W/m²·K |
| `area_of_stocking_doors_facing_zone` | Total area of stocking doors facing the conditioned zone | m² |
| `height_of_stocking_doors_facing_zone` | Height of stocking doors facing the conditioned zone | m |
| `stocking_door_u` | Thermal transmittance (U-value) of stocking doors | W/m²·K |
| `stocking_door_schedule` | Schedule defining the fraction of time stocking doors are open | N/A |
| `stocking_door_opening_protection` | Type of stocking door opening protection used | N/A |

---

## Refrigeration Compressors (`refrigeration_compressors`)
**Data headers, descriptions, and units for refrigeration compressor curves**

### Bicubic Curve Formula:
```
Curve Output = C1 + C2*x + C3*x² + C4*y + C5*y² + C6*x*y + C7*x³ + C8*y³ + C9*x²*y + C10*x*y²
```

- `x`: Saturation temperature corresponding to suction pressure (°C), equal to evaporating temperature (°C) - 1.
- `y`: Saturation temperature corresponding to discharge pressure (°C), equal to condensing temperature (°C) + 0.5.

   *(Reference: Engineering Reference, EnergyPlus Version 22.2.0, Chapter 18.2.6.2 – Compressor Energy Use.)*
- `C1` to `C10`: Coefficients used in the bicubic equation. (e.g.,`coefficient1` to `coefficient10`)



| Field | Description | Unit |
|-------|------------|------|
| `curve_name` | Name of the refrigeration compressor curve | N/A |
| `template` | Classification of the compressor curve as Old, New, or Advanced refrigeration system | N/A |
| `operation_type` | Classification based on temperature operation (LT < -18°C, MT -2°C to 4°C) | N/A |
| `curve_type` | Specifies whether the curve defines compressor power consumption or cooling capacity | N/A |
| `coefficient1` | First coefficient in the bicubic equation | N/A |
| `coefficient2` | Second coefficient in the bicubic equation | N/A |
| `coefficient3` | Third coefficient in the bicubic equation | N/A |
| `coefficient4` | Fourth coefficient in the bicubic equation | N/A |
| `coefficient5` | Fifth coefficient in the bicubic equation | N/A |
| `coefficient6` | Sixth coefficient in the bicubic equation | N/A |
| `coefficient7` | Seventh coefficient in the bicubic equation | N/A |
| `coefficient8` | Eighth coefficient in the bicubic equation | N/A |
| `coefficient9` | Ninth coefficient in the bicubic equation | N/A |
| `coefficient10` | Tenth coefficient in the bicubic equation | N/A |
| `min_val_x` | Minimum value for the x variable (suction pressure temperature) | °C |
| `max_val_x` | Maximum value for the x variable (suction pressure temperature) | °C |
| `min_val_y` | Minimum value for the y variable (discharge pressure temperature) | °C |
| `max_val_y` | Maximum value for the y variable (discharge pressure temperature) | °C |





## **License**
**This is a work in progress**  
Will be distributed under the terms of the BSD-3-Clause license

