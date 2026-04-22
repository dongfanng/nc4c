# Leaf Area Index (High Vegetation) 规范

## 数据源

- **来源**: ERA5-Land
- **变量**: `lai_hv`
- **长名称**: Leaf area index, high vegetation
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
    float32 lai_hv(valid_time, latitude, longitude)
        units: m**2 m**-2
        long_name: Leaf area index, high vegetation
        GRIB_paramId: 67
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0
    GRIB_missingValue: 3.4028234663852886e+38

# 数据范围:
# 原始数据: 0.0 ~ 5.53 (m²/m²)
# 负值比例: 0%

# 百分位数:
# P1: 0.000000, P5: 0.000000, P10: 0.000000
# P25: 0.000000, P50: 0.000000, P75: 1.625488
# P90: 2.471558, P95: 3.448029, P99: 4.683228

# 数值分布:
# < 0.1: 53.65% (无高植被区域)
# < 1.0: 61.87%
# < 2.0: 80.93%
# < 3.0: 93.21%
# < 4.0: 96.93%
# < 5.0: 99.99%

# 特点: 中位数=0，表示超过50%区域无高植被
```

## 可视化

- **色图**: 深绿色渐变（表示森林/树木）
- **数值范围**: 0.0 ~ 6.0 (m²/m²)
- **颜色映射**:

| 数值 (m²/m²) | HEX | 含义 |
|--------------|-----|------|
| 0.0 | #00000000 | 无高植被/裸土 (透明) |
| 0.5 | #90EE90 | 稀疏树木 |
| 1.5 | #228B22 | 低密度森林 |
| 3.0 | #006400 | 中等密度森林 |
| 4.5 | #004000 | 高密度森林 |
| 6.0 | #002800 | 茂密森林 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`