# AGENTS.md

本项目为 AI 编程助手提供代码开发指导。

## 项目概述

nc4c 是用于处理 NASA MERRA-2 / ERA5-Land 气溶胶和气象数据并生成 Cesium 可视化图像的 Python 项目。

**语言**: Python 3.12+
**用途**: NetCDF 转 Cesium 时间轴纹理生成

## 常用命令

```bash
# 安装依赖
uv sync

# 运行应用
uv run nc4c

# 代码格式化
uv run ruff format .

# 类型检查
uv run basedpyright

# 运行测试
uv run pytest
```

## 项目结构

```
src/nc4c/              # 主包
├── __init__.py       # 包导出
├── main.py           # CLI 入口
├── config.py         # 配置参数
├── constants.py      # 常量定义
├── core/             # 核心功能
│   ├── __init__.py
│   ├── base_processor.py  # 处理器基类
│   └── io.py              # NetCDF 读取与时间过滤
├── processors/       # 数据处理器
│   ├── pm10_processor.py
│   ├── temperature_processor.py
│   └── ... (更多处理器)
├── data_models/      # 数据模型
│   ├── __init__.py
│   ├── pm10.py
│   └── ...
├── visualization/   # 可视化模块
│   ├── __init__.py
│   ├── colormap.py           # 色图创建
│   ├── colormap_configs.py  # 色图配置
│   └── renderer.py          # 图像渲染
└── utils/           # 工具函数
    ├── datetime_utils.py    # 时间戳格式化
    └── color_utils.py       # 颜色处理
tests/                 # 测试
data/                  # 数据文件
docs/                  # 规范文档
pyproject.toml        # 项目配置
```

## 默认参数

| 参数 | 默认值 |
|------|--------|
| 地理范围 | 纬度 33°N-53°N，经度 73°E-135°E |
| 时间范围 | 北京时间 2023.03.19 00:00 ~ 2023.03.24 23:59 |
| 图像尺寸 | 1190×384 像素 @ 96 DPI |
| 宽高比 | 3.1:1 |

## 数据类型

### 时变数据（自动按时间范围过滤）

| 处理器 | 数据源 | 变量 | 单位转换 |
|--------|--------|------|----------|
| PM10 | NASA MERRA-2 | BCSMASS, OCSMASS, SO4SMASS, DUSMASS, SSSMASS | μg/m³ → 直接使用 |
| 2m Temperature | ERA5-Land | t2m | K → °C (-273.15) |
| Total Precipitation | ERA5-Land | tp | m → mm (×1000) |
| Snow Depth | ERA5-Land | sd | m → cm (×100) |
| Soil Moisture | ERA5-Land | swvl1 | m³/m³ → 直接使用 |
| Soil Temperature | ERA5-Land | stl1 | K → °C (-273.15) |
| Evaporation | ERA5-Land | (多种) | m → mm (×1000) |
| Radiation | ERA5-Land | (多种) | W/m² → 直接使用 |
| LAI | ERA5-Land | (多种) | 无量纲 → 直接使用 |
| Wind | ERA5-Land | 10u, 10v | JSON 格式输出 |

### 不变数据（无需时间过滤）

| 处理器 | 数据源 | 说明 |
|--------|--------|------|
| Soil Type | ERA5-Land | FAO 土壤质地分类 (0-6) |
| High Vegetation Type | ERA5-Land | GRIB Code table 4.234 |
| Low Vegetation Type | ERA5-Land | GRIB Code table 4.234 |

## PM10 计算

```
PM10 = BCSMASS + OCSMASS + SO4SMASS + DUSMASS + SSSMASS
```

## 颜色映射

### 连续渐变模式
适用于温度、降水等连续变化的数据，颜色平滑过渡。

### 离散分类模式
适用于土壤类型、植被类型等枚举值数据，每个值对应固定颜色。

## 开发指南

### 添加新数据类型

1. 创建规范文档 `docs/[data_type].spec.md`
2. 在 `src/nc4c/data_models/` 添加数据模型
3. 在 `src/nc4c/processors/` 添加处理器
4. 在 `src/nc4c/config.py` 添加配置
5. 在 `src/nc4c/main.py` 注册处理器
6. 运行质量检查

### 处理器基类

所有处理器继承 `BaseDataProcessor`，自动支持：
- `time_range_beijing`: 北京时间过滤（非不变数据）
- `read_netcdf`: 自动缺失值检测
- `create_colormap_and_norm` / `create_discrete_colormap_and_norm`: 色图创建

## 注意事项

- 坐标系：WGS84 (EPSG:4326)
- 时间偏移：原始数据 XX:30，输出文件 XX:00
- 缺失值：自动从元数据检测，或使用默认值 `9.9999999E14`
- 不变数据位于 `data/invariant_data/`，不受时间过滤影响