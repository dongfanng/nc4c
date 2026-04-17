# 2米温度规范

## 数据源

- **来源**: ERA5-Land
- **变量**: `t2m`
- **长名称**: 2 metre temperature
- **单位**: K (Kelvin) → °C (Celsius)
- **维度**: (longitude=621, latitude=201, valid_time=168)

## 处理

- **公式**: `°C = K - 273.15`
- **单位转换**: K → °C (-273.15)
- **缺失值处理**: `3.4028234663852886E38` → `np.nan`
- **维度顺序**: (valid_time, latitude, longitude) — 时间在最前面

## 数据分析

```
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

# 数据范围:
# 原始数据(K): 233.66 ~ 299.60
# 转换后(°C): -39.49 ~ 26.45
```

## 可视化

- **色图**: 自定义渐变
- **数值范围**: -40°C ~ 50°C
- **颜色映射**:

| 数值 (°C) | HEX |
|-----------|-----|
| -40 | #E6E6E6 |
| -30 | #FFAAFF |
| -20 | #910991 |
| -15 | #24186A |
| -10 | #554EB1 |
| -5 | #3E79C6 |
| 0 | #4BB698 |
| 5 | #59D049 |
| 10 | #BEE43D |
| 15 | #EBD735 |
| 20 | #EAA43E |
| 25 | #E56D53 |
| 30 | #BE3066 |
| 40 | #6B1527 |
| 50 | #2B0001 |

## 输出

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **命名**: `YYYY-MM-DD_HH-MM-SS.png`
