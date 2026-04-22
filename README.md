# nc4c

用于处理 NASA MERRA-2 / ERA5-Land 气溶胶和气象数据并生成 Cesium 可视化图像的 Python 项目。

## 功能特性

- 支持多种气象数据处理：PM10、温度、降水、蒸发、风场等
- 自动北京时间过滤（排除不变数据）
- 连续渐变与离散分类两种颜色映射模式
- 输出 Cesium 时间轴纹理图片

## 快速开始

```bash
# 安装依赖
uv sync

# 运行应用
uv run nc4c
```

## 数据类型

### 时变数据

| 类型 | 数据源 | 说明 |
|------|--------|------|
| PM10 | NASA MERRA-2 | 气溶胶质量浓度 |
| 2m Temperature | ERA5-Land | 地表气温 |
| Total Precipitation | ERA5-Land | 降水量 |
| Snow Depth | ERA5-Land | 雪深 |
| Soil Moisture | ERA5-Land | 土壤湿度 |
| Soil Temperature | ERA5-Land | 土壤温度 |
| Evaporation | ERA5-Land | 蒸发量（多种） |
| Radiation | ERA5-Land | 辐射（多种） |
| LAI | ERA5-Land | 叶面积指数 |
| Wind | ERA5-Land | 风速（JSON 输出） |

### 不变数据

| 类型 | 说明 |
|------|------|
| Soil Type | FAO 土壤质地分类 |
| High/Low Vegetation Type | 植被类型 |

## 参数配置

| 参数 | 默认值 |
|------|--------|
| 地理范围 | 纬度 33°N-53°N，经度 73°E-135°E |
| 时间范围 | 北京时间 2023.03.19 ~ 2023.03.24 |
| 图像尺寸 | 1190×384 像素 @ 96 DPI |

## 开发

```bash
# 代码格式化
uv run ruff format .

# 类型检查
uv run basedpyright

# 运行测试
uv run pytest
```

## 项目结构

```
src/nc4c/
├── main.py           # CLI 入口
├── config.py         # 配置参数
├── core/             # 核心功能（基类、IO）
├── processors/       # 数据处理器
├── data_models/     # 数据模型
├── visualization/   # 可视化（色图、渲染）
└── utils/           # 工具函数
```
