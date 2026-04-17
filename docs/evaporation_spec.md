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
# 负值比例: 90.5% (凝结为主，负值表示水汽从大气返回地表)
```

## 可视化

- **色图**: 自定义渐变（蓝=凝结 → 白=0 → 黄=蒸发）
- **数值范围**: -60 ~ 1 mm
- **颜色映射**:

| 数值 (mm) | HEX |
|-----------|-----|
| -60 | #3D82D4 |
| -40 | #7AAFE7 |
| -20 | #C8DDF6 |
| -5 | #EDE787 |
| 0 | #FFFFFF |
| 0.5 | #E8DC19 |
| 1 | #EAB939 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`