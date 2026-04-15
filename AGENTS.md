# AGENTS.md

本项目为 AI 编程助手提供代码开发指导。

## 项目概述

nc4c 是用于处理 NASA MERRA-2 气溶胶数据并生成 Cesium 可视化图像的 Python 项目。

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
├── core.py           # 核心读取功能
├── data_models/      # 数据模型
│   ├── __init__.py
│   └── pm10.py       # PM10 计算
└── visualization/   # 可视化模块
    ├── __init__.py
    ├── colormap.py           # 色图创建
    ├── colormap_configs.py  # 色图配置
    └── renderer.py          # 图像渲染
tests/                 # 测试
data/                  # 数据文件
pyproject.toml        # 项目配置
```

## 默认参数

| 参数 | 默认值 |
|------|--------|
| 地理范围 | 纬度 33°N-53°N，经度 73°E-135°E |
| 时间范围 | 2023.03.19 ~ 2023.03.24 |
| 图像尺寸 | 1190×384 像素 @ 96 DPI |
| 宽高比 | 3.1:1 |

## PM10 计算

```
PM10 = BCSMASS + OCSMASS + SO4SMASS + DUSMASS + SSSMASS
```

## 颜色映射

Ventusky PM10 渐变：#3D82D4 → #C8DDF6 → #EDE787 → #E8DC19 → #EAB939 → #E98F43 → #E15E5D → #A31B56 → #721638 → #2B0001

## 开发指南

1. 更新 `PM10_Calculation_ImageGen.spec.md` 规范
2. 在 `src/nc4c/` 实现代码
3. 在 `tests/` 添加测试
4. 运行质量检查

### 开发原则

- **函数优先**：优先使用函数（纯函数）开发，避免不必要的类封装
- **模块化设计**：按功能划分模块，每个模块负责单一职责
- **配置外置**：参数通过配置文件或命令行传递，代码中不使用硬编码值

## 注意事项

- 坐标系：WGS84 (EPSG:4326)
- 时间偏移：原始数据 XX:30，输出文件 XX:00
- 缺失值：`9.9999999E14` → `np.nan`
