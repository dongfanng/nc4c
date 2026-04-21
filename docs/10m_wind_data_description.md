# 10米风速 U/V 分量规范

## 1. JSON 结构

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
    "refTime": "2023-03-18T00:00:00.000.000Z"
  },
  "time": "2023.03.18 08:00:00",
  "longitude": [73.0, 73.1, 73.2, 73.3……],
  "latitude": [53.0, 52.9, 52.8, 52.9……],
  "u": [4.95,4.62,4.28,3.95……],
  "v": [2.75,2.71,2.68,2.63……]
}
```

| 名称         | 说明                                       | 对应元数据（:Conventions = "CF-1.7";）                       |
| ------------ | ------------------------------------------ | ------------------------------------------------------------ |
| dx           | 经度方向网格间距                           | :GRIB_iDirectionIncrementInDegrees = 0.1;                    |
| dy           | 纬度方向网格间距                           | :GRIB_jDirectionIncrementInDegrees = 0.1;                    |
| forecastTime | 单个数据文件预测时常，当前固定为一小时     | 数据按每小时切片                                             |
| la1          | 首个点纬度（左上角）                       | :GRIB_latitudeOfFirstGridPointInDegrees = 53.0;              |
| lo1          | 首个点精度（左上角）                       | :GRIB_longitudeOfFirstGridPointInDegrees = 73.0;             |
| nx           | 多少行，对应精度个数                       | :GRIB_Nx = 621L;                                             |
| ny           | 多少列，对应纬度个数                       | :GRIB_Ny = 201L;                                             |
| refTime      | UTC时间                                    | 数据valid_time维度中获取实际的时间值                         |
| time         | 北京时间                                   |                                                              |
| longitude    | 经度数组，按照元数据声明递增排列，长度 621 | :GRIB_iScansNegatively = 0L; // long 经度方向递增，从西向东扫描 |
| latitude     | 纬度数组，按照元数据声明递减排列，长度 201 | :GRIB_jScansPositively = 0L; // long  纬度方向递减，从北向南扫描 |
| u            | U 风速分量，长度 124,821                   | dataset[u10]                                                 |
| v            | V 风速分量，长度 124,821                   | dataset[v10]                                                 |

## 2.数据使用

1. 元数据 `:GRIB_jPointsAreConsecutive = 0L;` 指示行存储顺序为行优先，展平时先遍历纬度，再遍历精度，U/V 数组 shape 为 `(201, 621)`；
2. u 、v 数组中的缺省值已统一替换为 `null`

```
展平顺序：纬度（外层）× 经度（内层）
示例：[lat0_lon0, lat0_lon1, ..., lat0_lon620, lat1_lon0, ...]
总元素数：201 × 621 = 124,821
```

