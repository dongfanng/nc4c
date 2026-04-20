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

### 2.3 实际数据规格

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

### 3.3 时区转换

原始数据为 UTC 时间，输出时需转换为东八区（UTC+8）时间。

| 转换步骤 | 说明 |
|----------|------|
| 1. 读取 UTC 时间戳 | `timestamp` from NetCDF |
| 2. 应用 UTC+8 偏移 | `timestamp + np.timedelta64(8, "h")` |
| 3. 格式化为字符串 | `YYYY.MM.DD HH:MM:SS` |

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
    ├── 2023.03.18_00-00-00.json
    ├── 2023.03.18_01-00-00.json
    ├── ...
    └── 2023.03.24_23-00-00.json
```

### 4.2 文件命名规则

| 规则 | 说明 |
|------|------|
| **格式** | `YYYY.MM.DD_HH-MM-SS.json` |
| **时区** | UTC+8（东八区） |
| **分隔符** | 日期用 `_`，时间用 `-` |

### 4.3 JSON 结构

```json
{
  "time": "2023.03.19 00:00:00",
  "longitude": [73.0, 73.1, 73.2, ..., 135.0],
  "latitude": [53.0, 52.9, 52.8, ..., 33.0],
  "u": [1.58, 1.68, 1.77, ..., -0.54],
  "v": [2.34, 2.45, 2.56, ..., -1.23]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `time` | string | 东八区时间，格式 `YYYY.MM.DD HH:MM:SS` |
| `longitude` | number[] | 经度数组，长度 621 |
| `latitude` | number[] | 纬度数组，长度 201 |
| `u` | (number\|null)[] | U风分量数组，长度 124,821 |
| `v` | (number\|null)[] | V风分量数组，长度 124,821 |

### 4.4 数组长度验证

```
longitude 数组长度：621
latitude 数组长度：201
u/v 数组长度：201 × 621 = 124,821
```

## 5. 关键实现

### 5.1 时间戳处理

```python
from nc4c.utils.datetime_utils import format_timestamp_filename

output_file = format_timestamp_filename(output_path, timestamp, suffix="json")
# 生成：output/wind/2023-03-18_08-00-00.json

# 从文件名提取时间字符串
ts_str = output_file.stem  # "2023-03-18_08-00-00"
date_part, time_part = ts_str.split("_")  # "2023-03-18", "08-00-00"
year, month, day = date_part.split("-")  # "2023", "03", "18"
hour, minute, second = time_part.split("-")  # "08", "00", "00"
time_str = f"{year}.{month}.{day} {hour}:{minute}:{second}"  # "2023.03.18 08:00:00"
```

### 5.2 U/V 数据展平

```python
u_slice = u_data.isel(time=time_idx).values  # shape: (201, 621)
v_slice = v_data.isel(time=time_idx).values  # shape: (201, 621)

# 使用 float() 确保保留两位小数精度
u_flat = [float(f"{v:.2f}") for v in u_slice.flatten()]
v_flat = [float(f"{v:.2f}") for v in v_slice.flatten()]
```

### 5.3 缺失值替换

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
