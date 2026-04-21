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

### 统计分布

| 统计量 | 值 (mm) |
|--------|---------|
| Mean | -3.050 |
| Median | -2.224 |
| P25 | -3.811 |
| P75 | -0.752 |
| P90 | -0.099 |
| P95 | -0.016 |

- **1.29%** 的数据在 `|value| < 0.001` 范围内

## 可视化

- **色图**: 自定义渐变（棕=蒸发 → 白=0 → 青=凝结）
- **数值范围**: -6 ~ 0.8 mm
- **颜色映射**:

| 数值 (mm) | HEX | 含义 |
|-----------|-----|------|
| -6 | #8c510a | 强蒸发 |
| -2 | #d8b365 | 中等蒸发 |
| -0.1 | #f6e8c3 | 弱蒸发 |
| 0 | #00000000 | 零（透明） |
| 0.001 | #c7eae5 | 弱凝结 |
| 0.8 | #35978f | 强凝结 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`