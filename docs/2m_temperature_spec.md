# 2米温度 Specification

## Data Source

- **Source**: ERA5-Land
- **Variable**: `t2m`
- **Long name**: 2 metre temperature
- **Units**: K (Kelvin) → °C (Celsius)
- **Dimensions**: (longitude=621, latitude=201, valid_time=168)

## Processing

- **Formula**: `°C = K - 273.15`
- **Unit conversion**: K → °C (-273.15)
- **Missing value handling**: `3.4028234663852886E38` → `np.nan`
- **Dimension order**: (valid_time, latitude, longitude) — 注意时间在最前面

## CDL Analysis

```
dimensions:
  longitude = 621;
  latitude = 201;
  valid_time = 168;

variables:
  float t2m(valid_time=168, latitude=201, longitude=621);
    :units = "K";
    :_FillValue = NaNf;
    :GRIB_latitudeOfFirstGridPointInDegrees = 53.0;
    :GRIB_latitudeOfLastGridPointInDegrees = 33.0;
    :GRIB_longitudeOfFirstGridPointInDegrees = 73.0;
    :GRIB_longitudeOfLastGridPointInDegrees = 135.0;
```

## Visualization

- **Colormap**: t2m (已有配置)
- **Value range**: -30°C ~ 40°C
- **Color mapping**:

| Value (°C) | RGB | HEX |
|-------------|-----|-----|
| -30 | (0, 0, 255) | #0000FF |
| -20 | (93, 156, 253) | #5D9CFD |
| -10 | (145, 199, 249) | #91C7F9 |
| 0 | (201, 232, 247) | #C9E8F7 |
| 10 | (246, 250, 215) | #F6FAD7 |
| 20 | (249, 229, 168) | #F9E5A8 |
| 30 | (245, 176, 65) | #F5B041 |
| 40 | (214, 69, 69) | #D64545 |

## Output

- **Format**: PNG images
- **Resolution**: 1190×384 @ 96 DPI
- **Naming**: `YYYYMMDD_HHMM_t2m.png`
