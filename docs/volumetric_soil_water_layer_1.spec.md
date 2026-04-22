# 土壤水分层1规范

## 数据源

- **来源**: ERA5-Land
- **变量**: `swvl1`
- **长名称**: Volumetric soil water layer 1 (0-7cm)
- **单位**: m³/m³ (体积含水量)
- **维度**: (valid_time=168, latitude=201, longitude=621)

## 处理

- **公式**: 无需转换，直接使用 m³/m³
- **单位转换**: 无 (可直接使用，或转换为百分比 ×100)
- **缺失值处理**: `3.4028234663852886E38` → `np.nan`
- **维度顺序**: (valid_time, latitude, longitude) — 时间在最前面

## 数据分析

```
<xarray.Dataset>
  Dimensions:    (valid_time=168, latitude=201, longitude=621)
  Variables:
    float32 swvl1(valid_time, latitude, longitude)
        units: m**3 m**-3
        long_name: Volumetric soil water layer 1
        _FillValue: nan
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0

# 数据范围:
# 原始数据(m³/m³): 0.0 ~ 0.77
# 转换为百分比(%): 0 ~ 77
# 负值比例: 0.01% (2085个无效值)
```

## 可视化

- **色图**: 自定义渐变 (白色到深蓝)
- **数值范围**: 0 ~ 0.5 m³/m³ (或 0 ~ 50%)
- **颜色映射**:

| 数值 (m³/m³) | 百分比 | HEX |
|--------------|--------|-----|
| 0.00 | 0% | #F5F5F5 |
| 0.05 | 5% | #E0F2FE |
| 0.10 | 10% | #BAE6FD |
| 0.15 | 15% | #7DD3FC |
| 0.20 | 20% | #38BDF8 |
| 0.25 | 25% | #0EA5E9 |
| 0.30 | 30% | #0284C7 |
| 0.35 | 35% | #0369A1 |
| 0.40 | 40% | #075985 |
| 0.45 | 45% | #0C4A6E |
| 0.50 | 50% | #082F49 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`
- **目录**: `output/volumetric_soil_water_layer_1/`