---
name: meteorological-data-processor
description: "Creates meteorological data processors for NASA MERRA-2 or ERA5-Land NetCDF data. Invoke when user wants to process new meteorological variables (temperature, wind, humidity, precipitation, etc.), analyze NetCDF files to understand data structure, or add new data visualization capabilities. Follows the PM10 processor pattern."
---

# Meteorological Data Processor

A skill for creating meteorological data processors that generate Cesium-compatible visualizations from NetCDF files.

## When to Use

**INVOKE IMMEDIATELY when user:**
- Wants to process new meteorological data type (temperature, wind, humidity, snow, soil moisture, etc.)
- Has new NetCDF/CDL files and needs to understand their structure
- Wants to add new visualization capability to the nc4c project
- Asks to "process [variable name]" or "add support for [data type]"

## Workflow

### Step 1: Analyze NetCDF File

Use `xarray` to directly read NetCDF metadata — **do NOT use CDL files**.

**Python code to analyze NetCDF:**
```python
import xarray as xr

ds = xr.open_dataset("path/to/data.nc")

# 1. Print overview (dimensions, variables, attributes)
print(ds)

# 2. Get data variable info
var_name = list(ds.data_vars)[0]  # first data variable
var = ds[var_name]
print(f"Variable: {var_name}")
print(f"Dims: {var.dims}")        # dimension order
print(f"Shape: {var.shape}")     # dimension sizes
print(f"Attrs: {var.attrs}")     # units, _FillValue, etc.

# 3. Extract key metadata
units = var.attrs.get("units", "unknown")
fill_value = var.attrs.get("_FillValue")
long_name = var.attrs.get("long_name", var_name)

# 4. Get coordinate ranges (if available)
if "latitude" in ds.coords:
    lat_vals = ds["latitude"].values
    lat_range = (float(lat_vals.min()), float(lat_vals.max()))
if "longitude" in ds.coords:
    lon_vals = ds["longitude"].values
    lon_range = (float(lon_vals.min()), float(lon_vals.max()))

# 5. Check for GRIB/GEO metadata (ERA5-Land format)
grib_lats = [k for k in ds.attrs if "latitude" in k.lower()]
grib_lons = [k for k in ds.attrs if "longitude" in k.lower()]

# 6. Analyze data range and distribution (CRITICAL for colormap)
print(f"\nData range analysis:")
print(f"  Raw Min: {float(var.min())} ({units})")
print(f"  Raw Max: {float(var.max())} ({units})")
print(f"  Raw Mean: {float(var.mean())} ({units})")

# Check for negative values (common in evaporation/flux data)
neg_count = (var.values < 0).sum()
total_count = var.size
if neg_count > 0:
    print(f"  Negative values: {neg_count} / {total_count} ({100*neg_count/total_count:.1f}%)")
```

**IMPORTANT: For colormap design, also analyze data distribution statistics:**
```python
import numpy as np

flat = var.values.flatten()
flat = flat[~np.isnan(flat)]  # exclude nan

# Basic statistics
print(f"\nStatistics ({units}):")
print(f"  Min: {np.min(flat):.6f}")
print(f"  Max: {np.max(flat):.6f}")
print(f"  Mean: {np.mean(flat):.6f}")
print(f"  Median: {np.median(flat):.6f}")
print(f"  Std: {np.std(flat):.6f}")

# Percentiles (CRITICAL for colormap thresholds)
print(f"\nPercentiles:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    print(f"  P{p}: {np.percentile(flat, p):.6f}")

# Value distribution near zero (for evaporation/flux data)
print(f"\nValue distribution near zero:")
for threshold in [0, 0.0001, 0.001, 0.01, 0.1]:
    count_less = np.sum(np.abs(flat) < threshold)
    print(f"  |value| < {threshold}: {count_less} ({100*count_less/len(flat):.2f}%)")
```

**Example output for evaporation data:**
```
Statistics (mm):
  Min: -10.2217
  Max: 0.1915
  Mean: -0.0239
  Median: -0.0001
  Std: 0.1054

Percentiles:
  P1: -0.5056
  P5: -0.1399
  P10: -0.0322
  P25: -0.0013
  P50: -0.0001
  P75: 0.0000
  P90: 0.0000
  P95: 0.0001
  P99: 0.0107

Value distribution near zero:
  |value| < 0.001: 71.62%
  |value| < 0.01: 84.96%
```

**Use these statistics to design colormap:**
- **For skewed data**: Set color stops at percentiles (P10, P25, P75, P90)
- **For values near zero**: Use narrow transparent zone like `(-0.001, "#00000000"), (0.001, "#00000000")`
- **Never use raw min/max** for colormap range unless data is uniformly distributed

**Example output for 2m_temperature.nc:**
```python
<xarray.Dataset>
  Dimensions:    (longitude=621, latitude=201, valid_time=168)
  Variables:
    float32 t2m(valid_time, latitude, longitude)
        units: K
        long_name: 2 metre temperature
        _FillValue: nan
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0

# Summary:
variables = ["t2m"]
units = "K"  # Kelvin → °C (需转换: -273.15)
dimensions = (168, 201, 621)  # (time, latitude, longitude)
missing_value = nan  # or 3.4028234663852886E38
lat_range = (33.0, 53.0)  # degrees_north
lon_range = (73.0, 135.0)  # degrees_east

# Data range:
# Raw (K): 233.66 ~ 299.60
# Converted (°C): -39.49 ~ 26.45
```

**Alternative: ncdump command line:**
```bash
ncdump -h data.nc  # print header only (like CDL)
```

**Important: Save analysis results to `docs/[data_type].spec.md`**

### Step 2: Write SPEC Document

Create `docs/[data_type].spec.md` (use Chinese):

```markdown
# [数据类型] 规范

## 数据源

- **来源**: ERA5-Land / MERRA-2
- **变量**: [short_name]
- **长名称**: [long_name from attrs]
- **单位**: [units from attrs]
- **维度**: [dims, e.g., (time, lat, lon)]

## 处理

- **公式** (如适用): [计算方法]
- **单位转换**: [如需要，e.g., K → °C = value - 273.15]
- **缺失值处理**: [value → np.nan]

## 数据分析

```
# 原始数据分析结果 (从 Step 1)
<xarray.Dataset>
  ...
</xarray>

# 数据范围:
# 原始数据: [min] ~ [max] ([units])
# 转换后: [converted_min] ~ [converted_max] ([target_units])
# 负值比例: [percentage]% (如有)
```

## 可视化

- **色图**: [gradient name or custom]
- **数值范围**: [min] ~ [max] (基于数据分析结果)
- **颜色映射**:

| 数值 | HEX |
|------|-----|
| [v1] | #RRGGBB |
| [v2] | #RRGGBB |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`
```

### Step 3: Implement Processor

Follow the **PM10 Processor Pattern**:

```
src/nc4c/
├── processors/
│   └── [data_type]_processor.py    # Processor class
├── data_models/
│   └── [data_type].py              # Calculation logic
└── config.py                       # gradient and data config
```

#### 3.1 Data Model (`data_models/[data_type].py`)

```python
"""[Data Type] calculation module"""

import xarray as xr

VARIABLE_NAME: tuple[str, ...] = ("var_name",)  # or multiple for composite

UNIT_CONVERT: float = 1.0  # conversion factor if needed

def calculate_[data_type](
    dataset: xr.Dataset,
    variables: tuple[str, ...] = VARIABLE_NAME,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    Calculate [data type description]

    Args:
        dataset: Input dataset
        variables: Variable names to use
        unit_convert: Unit conversion factor

    Returns:
        [Data type] data array
    """
    if unit_convert is None:
        unit_convert = UNIT_CONVERT

    return dataset[variables[0]] * unit_convert
```

#### 3.2 Processor (`processors/[data_type]_processor.py`)

```python
"""[Data Type] data processor"""

from pathlib import Path

import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.[data_type] import calculate_[data_type], VARIABLE_NAME
from nc4c.utils.datetime_utils import format_timestamp_filename
from nc4c.visualization import create_colormap_and_norm, render_image


class [DataType]Processor(BaseDataProcessor):
    """[Data Type] image generation processor"""

    def __init__(
        self,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]],
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
    ) -> None:
        """
        Initialize [DataType] processor

        Args:
            input_paths: Input file paths
            output_dir: Output directory
            gradient: Color gradient list
            lon_range: Longitude range, None for auto-detect
            lat_range: Latitude range, None for auto-detect
        """
        super().__init__(input_paths=input_paths, output_dir=output_dir, gradient=gradient)
        self.lon_range = lon_range
        self.lat_range = lat_range

    def get_required_variables(self) -> list[str]:
        """Get required variable list"""
        return list(VARIABLE_NAME)

    def get_output_name(self) -> str:
        """Get output directory name"""
        return "[data_type]"

    def load(self) -> xr.Dataset:
        """Load NetCDF data"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=9.9999999e14,  # or from CDL
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """Calculate [data type]"""
        return calculate_[data_type](
            dataset=dataset,
            variables=VARIABLE_NAME,
        )

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """Generate [data type] images"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        colormap_obj, norm = create_colormap_and_norm(self.gradient)

        generated_files: list[Path] = []
        n_times = len(data.coords["time"])

        for time_idx in range(n_times):
            timestamp = data.coords["time"].values[time_idx]
            output_file = format_timestamp_filename(output_path, timestamp)

            render_image(
                data=data,
                time_index=time_idx,
                output_path=output_file,
                colormap=colormap_obj,
                norm=norm,
                lon_range=self.lon_range,
                lat_range=self.lat_range,
            )
            generated_files.append(output_file)

        return generated_files
```

### Step 4: Update Config (`config.py`)

Add a new dataclass with `gradient` in `config.py`:

```python
from dataclasses import dataclass, field

@dataclass
class [DataType]Config:
    name: str = "[data_type]"
    data_files: list[str] = field(default_factory=lambda: [
        str(DATA_DIR / "[data_dir]" / "*.nc"),  # or specific file
    ])
    output_dir: str = "output/[data_type]"
    unit: str = "[units]"
    gradient: list[tuple[float, str]] = field(default_factory=lambda: [
        (min_val, "#color1"),
        (max_val, "#color2"),
    ])

# Register in the global config object
cfg.[data_type] = [DataType]Config()
```

### Step 5: Register Processor (`processors/__init__.py`)

```python
from nc4c.processors.[data_type]_processor import [DataType]Processor

__all__ = [..., "[DataType]Processor"]
```

## Available Meteorological Data Types

From the ERA5-Land dataset in `data/raw_met_data/`:

| Variable | CDL File | Units | Processing |
|----------|----------|-------|------------|
| 2m Temperature | 2m_temperature.cdl | K | K → °C (-273.15) |
| 10m Wind U/V | (combined) | m/s | wind speed √(u²+v²) |
| Snow Depth | snow_depth.nc | m | m → cm (×100) |
| Soil Moisture | volumetric_soil_water_layer_1.nc | m³/m³ | fraction → % (×100) |
| LAI | leaf_area_index_*.nc | dimensionless | direct use |
| Radiation | surface_*.nc | W/m² | direct use |
| Evaporation | *evaporation*.nc | m | m → mm (×1000) |
| Precipitation | total_precipitation.nc | m | m → mm (×1000) |

## Reference Files

- PM10 implementation: `src/nc4c/processors/pm10_processor.py`
- PM10 data model: `src/nc4c/data_models/pm10.py`
- Config: `src/nc4c/config.py`
