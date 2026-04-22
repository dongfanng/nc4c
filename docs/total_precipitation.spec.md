# Total Precipitation 规范

## 数据源

- **来源**: ERA5-Land
- **变量**: tp
- **长名称**: Total precipitation
- **单位**: m
- **维度**: (valid_time, latitude, longitude)

## 处理

- **公式**: 直接使用 `tp` 变量值
- **单位转换**: m → mm (= value × 1000)
- **缺失值处理**: 3.4028234663852886E38 → np.nan

## 数据分析

```
<xarray.Dataset>
Dimensions:     (valid_time: 168, latitude: 201, longitude: 621)
Variables:
    tp          (valid_time, latitude, longitude) float32
Attributes:
    GRIB_name:  Total precipitation
    GRIB_units: m
</xarray>

# 数据范围:
# 原始数据: 0.0 ~ 0.0645 (m)
# 转换后: 0.0 ~ 64.5 (mm)
# 负值比例: 0%

# 百分位数 (mm):
# P50: 0.001
# P75: 0.086
# P90: 0.869
# P95: 2.087
# P99: 6.882

# 数值分布:
# |value| < 0.1mm: 75.85%
# |value| < 1mm: 90.89%
# |value| < 10mm: 99.63%
```

## 可视化

- **色图**: 降水蓝渐变
- **数值范围**: 0 ~ 10 mm（基于 P99 分布）
- **颜色映射**:

| 数值 (mm) | HEX |
|-----------|-----|
| 0 | #00000000 |
| 0.1 | #C8E3F5 |
| 1 | #75B4F0 |
| 5 | #2E6AB3 |
| 10 | #1A3A6B |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`