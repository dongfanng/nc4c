# 10米风速 U/V 分量规范

## 1. 概述

### 1.1 背景与目标
本规范定义基于 ERA5-Land 再分析数据集处理 10 米高度风速数据（U/V 分量）并生成 JSON 格式输出的完整流程。生成的 JSON 用于在 Cesium 三维地球引擎中展示风向和风速的时空分布特征。

### 1.2 数据来源
- **数据集**：ERA5-Land 10m u/v component of wind
- **官方说明**：https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview

### 1.3 默认参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| **地理范围** | 纬度 33°N – 53°N，经度 73°E – 135°E | 中国区域 |
| **坐标系** | WGS84 经纬度坐标系 | 标准地理坐标 |
| **输出格式** | JSON | 每时间步一个文件 |
| **时间分辨率** | 逐小时 | 24 帧/天 |
| **缺失值** | `3.4028234663852886e38` | IEEE 754 32位浮点最大值 |

## 2. 输入数据规范

### 2.1 NetCDF 数据变量

| 变量名 | 中文描述 | 单位 | 物理含义 |
|--------|----------|------|----------|
| `u10` | 10米U风分量 | m/s | 东西方向风速（正值=东向） |
| `v10` | 10米V风分量 | m/s | 南北方向风速（正值=北向） |

### 2.2 文件要求

| 项目 | 要求 |
|------|------|
| **格式** | NetCDF4 (.nc) |
| **维度** | 必须包含 `time`、`lat`、`lon` |
| **变量维度顺序** | `(time, lat, lon)` |
| **坐标** | 经纬度为一维数组，单位为度（WGS84） |
| **时间** | `hours since` 或 `valid_time` 格式 |
| **缺失值** | `3.4028234663852886e38` |

### 2.3 GRIB 元数据属性

| 属性名 | 值 | 说明 |
|--------|-----|------|
| `GRIB_Nx` | 621 | 经度方向网格点数 |
| `GRIB_Ny` | 201 | 纬度方向网格点数 |
| `GRIB_longitudeOfFirstGridPointInDegrees` | 73.0 | 首个网格点经度 |
| `GRIB_latitudeOfFirstGridPointInDegrees` | 53.0 | 首个网格点纬度 |
| `GRIB_iDirectionIncrementInDegrees` | 0.1 | 经度方向网格间距 |
| `GRIB_jDirectionIncrementInDegrees` | 0.1 | 纬度方向网格间距 |
| `GRIB_iScansNegatively` | 0 | 经度方向递增（从西向东） |
| `GRIB_jScansPositively` | 0 | 纬度方向递减（从北向南） |
| `GRIB_jPointsAreConsecutive` | 0 | 行优先存储（经度变化最快） |

### 2.4 实际数据规格

| 属性 | 值 | 说明 |
|------|-----|------|
| **时间维度** | 168（7天，逐小时） | 案例数据包含一周 |
| **经度范围** | 73.0°E - 135.0°E | 全范围 |
| **纬度范围** | 33.0°N - 53.0°N | 全范围 |
| **经度分辨率** | 0.1° | 621 个网格点 |
| **纬度分辨率** | 0.1° | 201 个网格点 |

## 3. 数据处理规范

### 3.1 坐标系说明

| 分量 | 正值方向 | 负值方向 |
|------|----------|----------|
| **U (东西)** | 东 | 西 |
| **V (南北)** | 北 | 南 |

### 3.2 精度控制

| 字段 | 精度 | 说明 |
|------|------|------|
| **经度** | 1位小数 | `np.round(lon, 1)` |
| **纬度** | 1位小数 | `np.round(lat, 1)` |
| **U/V风速** | 2位小数 | `float(f"{v:.2f}")` |

### 3.3 GRIB 扫描顺序处理

原始 NetCDF 数据中的 GRIB 属性描述了数据的存储和扫描顺序：

| 属性 | 值 | 含义 |
|------|-----|------|
| `GRIB_iScansNegatively` | 0 | 经度从西向东递增（73→135） |
| `GRIB_jScansPositively` | 0 | 纬度从北向南递减（53→33） |

处理流程：
1. 读取当前坐标的实际排序
2. 与 GRIB 属性描述的排序对比
3. 如不一致，执行维度翻转

```
示例：
- GRIB_jScansPositively = 0（纬度应递减：53→33）
- 实际坐标 lat[0] = 33（递增）
- 处理：lat = lat[::-1]（翻转）
```

### 3.4 数据展平顺序

U/V 数组 shape 为 `(201, 621)`，展平时采用 **行优先（C风格）** 顺序：

```
展平顺序：纬度（外层）× 经度（内层）
示例：[lat0_lon0, lat0_lon1, ..., lat0_lon620, lat1_lon0, ...]
总元素数：201 × 621 = 124,821
```

### 3.5 缺失值处理

| 原始值 | 处理方式 | JSON输出 |
|--------|----------|----------|
| `3.4028234663852886e38` | 替换为 `None` | `null` |
| `NaN` | 替换为 `None` | `null` |

## 4. 输出产物规范

### 4.1 输出目录结构

```
<ROOT_OUTPUT_DIR>/
└── wind/
    ├── 2023-03-18T00_00_00Z.json
    ├── 2023-03-18T01_00_00Z.json
    ├── ...
    └── 2023-03-24T23_00_00Z.json
```

### 4.2 文件命名规则

| 规则 | 说明 |
|------|------|
| **格式** | `YYYY-MM-DDTHH_MM_SSZ.json` |
| **时区** | UTC（协调世界时） |
| **分隔符** | 日期用 `-`，日期与时间用 `T` 连接，时间用 `_`，末尾 `Z` 标记 UTC |

### 4.3 JSON 结构

```json
{
  "header": {
    "dx": 0.1,
    "dy": 0.1,
    "forecastTime": 1,
    "la1": 53.0,
    "lo1": 73.0,
    "nx": 621,
    "ny": 201,
    "refTime": "2023-03-18T00:00:00Z"
  },
  "time": "2023.03.18 00:00:00",
  "longitude": [73.0, 73.1, 73.2, ..., 135.0],
  "latitude": [53.0, 52.9, 52.8, ..., 33.0],
  "u": [4.95, 4.62, 4.28, ..., null],
  "v": [2.75, 2.71, 2.68, ..., null]
}
```

### 4.4 JSON 字段说明

| 名称 | 说明 | 对应元数据 | 数据类型 |
|------|------|-----------|----------|
| `header.dx` | 经度方向网格间距 | `GRIB_iDirectionIncrementInDegrees` | `number` |
| `header.dy` | 纬度方向网格间距 | `GRIB_jDirectionIncrementInDegrees` | `number` |
| `header.forecastTime` | 预测时长（小时） | 固定值 | `number` |
| `header.la1` | 首个网格点纬度（左上角） | `GRIB_latitudeOfFirstGridPointInDegrees` | `number` |
| `header.lo1` | 首个网格点经度（左上角） | `GRIB_longitudeOfFirstGridPointInDegrees` | `number` |
| `header.nx` | 经度方向网格点数 | `GRIB_Nx` | `number` |
| `header.ny` | 纬度方向网格点数 | `GRIB_Ny` | `number` |
| `header.refTime` | 参考时间（UTC） | 当前时刻 | `string` (ISO 8601) |
| `time` | 数据有效时间（UTC） | - | `string` ("YYYY.MM.DD HH:MM:SS") |
| `longitude` | 经度数组（从西到东递增） | `GRIB_iScansNegatively = 0` | `array<number>` |
| `latitude` | 纬度数组（从北到南递减） | `GRIB_jScansPositively = 0` | `array<number>` |
| `u` | U 风速分量（东西方向） | - | `array<number | null>` |
| `v` | V 风速分量（南北方向） | - | `array<number | null>` |

### 4.5 数组长度验证

```
longitude 数组长度：621
latitude 数组长度：201
u/v 数组长度：201 × 621 = 124,821
```

## 5. 关键实现

### 5.1 GRIB 扫描顺序处理

```python
def _apply_grib_scan_order(data: xr.DataArray) -> xr.DataArray:
    lat_vals = data.coords["lat"].values
    lon_vals = data.coords["lon"].values

    lat_ascending = lat_vals[0] < lat_vals[-1]
    lon_ascending = lon_vals[0] < lon_vals[-1]

    j_scans_positively = data.attrs.get("GRIB_jScansPositively", None)
    i_scans_negatively = data.attrs.get("GRIB_iScansNegatively", None)

    if j_scans_positively == 0 and lat_ascending:
        data = data.isel(lat=slice(None, None, -1))
    elif j_scans_positively == 1 and not lat_ascending:
        data = data.isel(lat=slice(None, None, -1))

    if i_scans_negatively == 0 and not lon_ascending:
        data = data.isel(lon=slice(None, None, -1))
    elif i_scans_negatively == 1 and lon_ascending:
        data = data.isel(lon=slice(None, None, -1))

    return data
```

### 5.2 时间戳处理

```python
# 生成文件名（UTC）
output_file = format_timestamp_filename(output_path, timestamp, suffix="json")
# 输出：output/wind/2023-03-18T00_00_00Z.json

# time 字段（UTC）
ts_str = output_file.stem  # "2023-03-18T00_00_00Z"
date_part, time_part = ts_str.split("T")
year, month, day = date_part.split("-")
hour, minute, second = time_part.replace("Z", "").split("_")
time_str = f"{year}.{month}.{day} {hour}:{minute}:{second}"  # "2023.03.18 00:00:00"

# refTime 字段（UTC ISO 格式）
ref_time = pd.Timestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
# 输出："2023-03-18T00:00:00Z"
```

### 5.3 U/V 数据展平

```python
u_slice = u_data.isel(time=time_idx).values  # shape: (201, 621)
v_slice = v_data.isel(time=time_idx).values  # shape: (201, 621)

u_flat = [float(f"{v:.2f}") for v in u_slice.flatten()]
v_flat = [float(f"{v:.2f}") for v in v_slice.flatten()]
```

### 5.4 缺失值替换

```python
def _replace_missing_values(data: list) -> list:
    result = []
    for val in data:
        if isinstance(val, float) and np.isnan(val):
            result.append(None)
        else:
            result.append(val)
    return result
```

## 6. 配置参数

```python
@dataclass
class WindConfig:
    name: str = "10m_u_component_of_wind-10m_v_component_of_wind"
    data_files: list[str] = field(
        default_factory=lambda: [
            str(DATA_DIR / "raw_met_data" / "10m_u_component_of_wind 10m_v_component_of_wind.nc")
        ]
    )
    output_dir: str = "output/wind"
    unit: str = "m/s"
```

## 7. 已知限制

1. **浮点精度**：IEEE 754 浮点数无法精确表示某些小数（如 `1.58`），使用 `float(f"{v:.2f}")` 格式化确保输出为 2 位小数。
2. **JSON 尾随零**：JSON 格式不保留尾随零，`1.50` 会显示为 `1.5`，这是 JSON 规范行为，不影响实际精度。
3. **文件名冒号**：Windows 文件名不允许冒号（`:`），因此文件名中时间分隔符使用 `_`（如 `2023-03-18T00_00_00Z.json`），而 JSON 内容中 `refTime` 使用标准 ISO 8601 冒号格式。
