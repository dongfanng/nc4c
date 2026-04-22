# Leaf Area Index (Low Vegetation) 规范

## 数据源

- **来源**: ERA5-Land
- **变量**: `lai_lv`
- **长名称**: Leaf area index, low vegetation
- **单位**: m²/m² (无单位，表示单位面积上叶片单面面积)
- **维度**: (valid_time=168, latitude=201, longitude=621)

## 处理

- **公式**: 无需计算，直接使用原始值
- **单位转换**: 无
- **缺失值处理**: `3.4028234663852886E38` → `np.nan`
- **维度顺序**: (valid_time, latitude, longitude) — 时间在最前面

## 数据分析

```
<xarray.Dataset>
  Dimensions:    (valid_time=168, latitude=201, longitude=621)
  Variables:
    float32 lai_lv(valid_time, latitude, longitude)
        units: m**2 m**-2
        long_name: Leaf area index, low vegetation
        GRIB_paramId: 66
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0
    GRIB_missingValue: 3.4028234663852886e+38

# 数据范围:
# 原始数据: 0.0 ~ 3.99 (m²/m²)
# 负值比例: 0%

# 百分位数:
# P1: 0.000000, P5: 0.000000, P10: 0.222900
# P25: 0.507812, P50: 0.684326, P75: 1.117920
# P90: 2.098877, P95: 2.596802, P99: 2.930176

# 数值分布:
# < 0.1: 8.84% (接近裸土/水体)
# < 1.0: 72.19%
# < 2.0: 89.00%
# < 3.0: 99.61%
```

## 可视化

- **色图**: 植被绿色渐变
- **数值范围**: 0.0 ~ 4.0 (m²/m²)
- **颜色映射**:

| 数值 (m²/m²) | HEX | 含义 |
|--------------|-----|------|
| 0.0 | #F5F5DC | 裸土/水体 |
| 0.5 | #90EE90 | 稀疏植被 |
| 1.0 | #32CD32 | 低密度植被 |
| 2.0 | #228B22 | 中等密度植被 |
| 3.0 | #006400 | 高密度植被 |
| 4.0 | #004000 | 茂密植被 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`