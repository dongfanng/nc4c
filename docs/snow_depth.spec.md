# Snow Depth 规范

## 数据源

- **来源**: ERA5-Land (ECMWF)
- **变量**: sde
- **长名称**: Snow depth
- **单位**: m (米)
- **维度**: (valid_time, latitude, longitude)
- **时间范围**: 2023-03-18 ~ 2023-03-24
- **地理范围**: 纬度 33°N-53°N，经度 73°E-135°E

## 处理

- **公式**: m → cm = value × 100
- **缺失值处理**: GRIB_missingValue (3.4028234663852886e+38) → np.nan

## 数据分析

```
<xarray.Dataset>
  Dimensions:     (valid_time: 168, latitude: 201, longitude: 621)
  Variables:
    sde        (valid_time, latitude, longitude) float32
        units: m
        long_name: Snow depth
        GRIB_missingValue: 3.4028234663852886e+38
  Attributes:
    GRIB_latitudeOfFirstGridPointInDegrees = 53.0
    GRIB_latitudeOfLastGridPointInDegrees = 33.0
    GRIB_longitudeOfFirstGridPointInDegrees = 73.0
    GRIB_longitudeOfLastGridPointInDegrees = 135.0
```

### 数据范围

| 统计量 | m | cm |
|--------|---|-----|
| Min | 0 | 0 |
| Max | 33.33 | 3333.30 |
| Mean | 0.21 | 20.92 |
| Median | 0.007 | 0.68 |
| Std | 1.58 | - |

### 百分位数 (cm)

| 百分位 | cm |
|--------|-----|
| P1 | 0.00 |
| P5 | 0.00 |
| P10 | 0.00 |
| P25 | 0.00 |
| P50 | 0.68 |
| P75 | 7.81 |
| P90 | 40.53 |
| P95 | 71.29 |
| P99 | 153.22 |

### 积雪分布

| 阈值 | 占比 |
|------|------|
| = 0 cm | 34.54% |
| < 1 cm | 52.80% |
| < 5 cm | 70.60% |
| < 10 cm | 77.12% |
| < 20 cm | 82.59% |
| < 50 cm | 92.11% |

## 可视化

- **色图**: 自定义积雪深度渐变
- **数值范围**: 0 ~ 50 cm (基于积雪分布)

### 颜色映射

| 积雪深度 (cm) | 描述 | HEX |
|---------------|------|-----|
| 0 | 无积雪 | #00000000 (透明) |
| 1 ~ 5 | 浅积雪 | #ADD8E6 |
| 5 ~ 10 | 中度积雪 | #00BFFF |
| 10 ~ 20 | 深雪 | #0000FF |
| 20 ~ 50 | 极深积雪 | #00008B |
| 50+ | 极雪区 | #000080 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`
- **目录**: `output/snow_depth`