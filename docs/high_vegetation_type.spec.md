# High Vegetation Type 数据处理规范

## 1. 数据源

- **来源**: ERA5-Land 高植被类型数据
- **变量**: `tvh` (Type of high vegetation)
- **长名称**: Type of high vegetation
- **单位**: `~` (无量纲，分类数据)
- **维度**: `(time, latitude, longitude) = (1, 201, 621)`
- **时间**: 1996-01-01 (不变数据，只需处理一次)
- **来源说明**: ECMWF IFS GRIB Code table 4.234

## 2. 植被类型分类定义

依据 ECMWF GRIB Code table 4.234 - High Vegetation (tvh):

| ID | 英文名称 | 中文含义 | 中国区域分布 |
|----|----------|----------|--------------|
| 3 | Evergreen needleleaf trees | 常绿针叶树 | 占 0.46% |
| 4 | Deciduous needleleaf trees | 落叶针叶树 | 占 4.46% |
| 5 | Deciduous broadleaf trees | 落叶阔叶树 | 占 1.59% |
| 6 | Evergreen broadleaf trees | 常绿阔叶树 | 占 0.01% |
| 18 | Mixed forest/woodland | 混交林/林地 | 占 8.34% |
| 19 | Interrupted forest | 间断森林 | 占 23.47% |

> **说明**: 其他类型 (1,2,7,9,10,11,13,16,17,20) 属于低矮植被；0=无植被；8=荒漠；12=冰盖/冰川；14=内陆水体；15=海洋
>
> **来源**: <https://codes.ecmwf.int/grib/param-db/30>

## 3. 数据分析

### 3.1 数据结构

```
<xarray.Dataset> Size: 1MB
Dimensions:    (time: 1, latitude: 201, longitude: 621)
Coordinates:
  * time       (time) datetime64[ns] 8B 1996-01-01
  * latitude   (latitude) float32 804B 53.0 ~ 33.0 (201 points)
  * longitude  (longitude) float32 2kB 73.0 ~ 135.0 (621 points)
Data variables:
    tvh        (time, latitude, longitude) float64 999kB
Attributes:
    Conventions:  CF-1.6
    history:      Thu Oct 21 16:33:12 2021: ncpdq -U tvh_packed.nc tvh.nc
```

### 3.2 地理范围

| 坐标 | 最小值 | 最大值 | 单位 |
|------|--------|--------|------|
| 纬度 | 33.0 | 53.0 | degrees_north |
| 经度 | 73.0 | 135.0 | degrees_east |

### 3.3 实际数据分布

| ID | 像素数 | 占比 | 植被类型 |
|----|--------|------|----------|
| 0 | 76,973 | 61.67% | 无植被 (No vegetation) |
| 3 | 578 | 0.46% | 常绿针叶树 |
| 4 | 5,570 | 4.46% | 落叶针叶树 |
| 5 | 1,987 | 1.59% | 落叶阔叶树 |
| 6 | 7 | 0.01% | 常绿阔叶树 |
| 18 | 10,413 | 8.34% | 混交林/林地 |
| 19 | 29,293 | 23.47% | 间断森林 |

> **注**: 值为近似值 (如 2.99990844 ≈ 3, 3.99987792 ≈ 4)，存储时可能有微小浮点误差。

## 4. 处理流程

### 4.1 预处理

1. **读取数据**: 使用 xarray 打开 NetCDF 文件
2. **范围裁剪**: 可选裁剪至指定经纬度范围
3. **缺失值处理**: 本数据集无缺失值

### 4.2 数值处理

- **取整**: 将浮点数值四舍五入到最近的整数类别 (0, 3, 4, 5, 6, 18, 19)

## 5. 可视化

### 5.1 色图配置

使用分类颜色映射，每种植被类型对应一种颜色：

| ID | 植被类型 | 颜色 | HEX | 视觉含义 |
|----|----------|------|-----|----------|
| 0 | 无高植被 | 透明 | #00000000 | 无高植被 |
| 3 | 落叶阔叶疏林 | 橙棕 | #D2691E | 暖色调森林 |
| 4 | 常绿针叶林 | 深绿 | #228B22 | 针叶林 |
| 5 | 落叶针叶林 | 浅绿 | #90EE90 | 季节性绿 |
| 6 | 混交林 | 草绿 | #6B8E23 | 混合林 |
| 18 | 农田/灌木/草地镶嵌 | 黄绿 | #9ACD32 | 农业景观 |
| 19 | 裸地 | 沙黄 | #F4A460 | 荒漠化 |

### 5.2 数值范围

色图使用离散分段映射，边界计算:
```
bound[i] = (gradient[i-1].value + gradient[i].value) / 2
bound[0] = gradient[0].value - 0.5
bound[last] = gradient[last].value + 0.5
```

### 5.3 输出规格

- **格式**: PNG images
- **分辨率**: 1190×384 @ 96 DPI
- **文件名**: `high_vegetation_type_1996-01-01_00-00-00.png` (时间固定为数据时间戳)
- **投影**: WGS84 经纬度坐标系

## 6. 实现模块

| 模块 | 文件路径 |
|------|----------|
| 数据模型 | `src/nc4c/data_models/high_vegetation_type.py` |
| 处理器 | `src/nc4c/processors/high_vegetation_type_processor.py` |
| 配置 | `src/nc4c/config.py` |

## 7. 生态学意义提示

高植被类型反映地表覆盖特征，对沙尘传输研究有重要意义：

| ID | 植被类型 | 防风固沙作用 | 中国区域意义 |
|----|----------|--------------|--------------|
| 0 | 无植被/裸地 | 无，**高起沙风险** | 塔克拉玛干等沙漠 |
| 4 | 常绿针叶林 | 强，冬季也有效 | 东北林区 |
| 5 | 落叶针叶林 | 强，季节性 | 大兴安岭林区 |
| 18 | 农田镶嵌 | 中 | 农牧交错带 |
| 19 | 裸地 | 无，**高起沙风险** | 荒漠边缘 |
