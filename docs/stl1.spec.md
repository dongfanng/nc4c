# Soil Temperature Level 1 规范

## 数据源

- **来源**: ERA5-Land (ECMWF)
- **变量**: stl1
- **长名称**: Soil temperature level 1
- **单位**: K (Kelvin)
- **维度**: (valid_time, latitude, longitude)
- **时间范围**: 2023-03-18 ~ 2023-03-24
- **地理范围**: 纬度 33°N-53°N，经度 73°E-135°E

## 处理

- **公式**: K → °C = value - 273.15
- **缺失值处理**: GRIB_missingValue (3.4028234663852886e+38) → np.nan

## 数据分析

```
<xarray.Dataset>
  Dimensions:     (valid_time: 168, latitude: 201, longitude: 621)
  Variables:
    stl1        (valid_time, latitude, longitude) float32
        units: K
        long_name: Soil temperature level 1
        GRIB_missingValue: 3.4028234663852886e+38
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0
```

### 数据范围

| 统计量 | K | °C |
|--------|---|-----|
| Min | 242.66 | -30.49 |
| Max | 309.64 | 36.49 |
| Mean | 273.99 | 0.84 |
| Median | 272.33 | -0.82 |
| Std | 7.34 | - |

### 百分位数 (°C)

| 百分位 | °C |
|--------|-----|
| P1 | -15.35 |
| P5 | -9.47 |
| P10 | -6.16 |
| P25 | -2.52 |
| P50 | -0.82 |
| P75 | 3.49 |
| P90 | 11.43 |
| P95 | 15.57 |
| P99 | 23.66 |

## 可视化

- **色图**: 自定义土壤温度渐变 (蓝-黄-红)
- **数值范围**: -15°C ~ 30°C (基于数据分布)

### 颜色映射

| 数值 (°C) | HEX |
|-----------|-----|
| -15 | #2B2D6B |
| -5 | #3D82D4 |
| 5 | #C8DDF6 |
| 15 | #EDE787 |
| 25 | #E8DC19 |
| 30 | #E15E5D |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`
- **目录**: `output/stl1/`