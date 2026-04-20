# Potential Evaporation 规范

## 数据源

- **来源**: ERA5-Land
- **变量**: `pev`
- **长名称**: Potential evaporation
- **单位**: m (米)
- **维度**: (valid_time=168, latitude=201, longitude=621)

## 处理

- **公式**: `mm = m × 1000`
- **单位转换**: m → mm (×1000)
- **缺失值处理**: `3.4028234663852886E38` → `np.nan`

## 数据分析

```
<xarray.Dataset>
  Dimensions:     (valid_time=168, latitude=201, longitude=621)
  Variables:
    float32 pev(valid_time, latitude, longitude)
        units: m
        long_name: Potential evaporation
        GRIB_missingValue: 3.4028234663852886e+38
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0
</xarray>

# 数据范围:
# 原始数据 (m): -0.0521 ~ 0.00077
# 转换后 (mm): -52.1 ~ 0.77
# 负值比例: 90.5% (ECMWF 惯例：负值=蒸发，正值=凝结)
```

## 可视化

- **色图**: 自定义渐变（棕=蒸发 → 白=0 → 青=凝结）
- **数值范围**: -50 ~ 0.8 mm
- **颜色映射**:

| 数值 (mm) | HEX |
|-----------|-----|
| -50 | #8c510a |
| -25 | #dfc27d |
| -5 | #f6e8c3 |
| 0 | #f7f7f7 |
| 0.5 | #c7eae5 |
| 0.8 | #35978f |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`