"""PM10 计算模块"""

import xarray as xr

PM10_VARIABLES: tuple[str, ...] = (
    "BCSMASS",  # 黑碳
    "OCSMASS",  # 有机碳
    "SO4SMASS",  # 硫酸盐
    "DUSMASS",  # 粉尘
    "SSSMASS",  # 海盐
)

# 单位转换系数: kg/m3 -> ug/m3
PM10_UNIT_CONVERT: float = 1e9


def calculate_pm10(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = PM10_VARIABLES,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算 PM10 (颗粒物浓度)

    PM10 = BCSMASS + OCSMASS + SO4SMASS + DUSMASS + SSSMASS

    Args:
        dataset: 包含气溶胶变量的数据集
        variables: PM10 组成变量列表
        unit_convert: 单位转换系数 (kg/m3 -> ug/m3), 默认为 None 表示自动检测

    Returns:
        PM10 数据数组，维度 (lon, lat, time)，单位 μg/m³
    """
    # ========== 自动检测单位转换系数 ==========
    # 从第一个变量的 units 属性判断输入数据单位
    if unit_convert is None:
        units = dataset[variables[0]].attrs.get("units", "").lower()
        if "kg" in units:
            unit_convert = PM10_UNIT_CONVERT  # kg/m3 -> ug/m3
        else:
            unit_convert = 1.0  # 已是 ug/m3, 不转换

    # ========== 链式调用 (xarray 向量化操作) ==========
    # 1. 选取变量: dataset[list(variables)] -> Dataset
    # 2. 合并为数组: to_array(dim="component") -> DataArray (新增 component 维度)
    # 3. 沿 component 求和: sum(dim="component") -> DataArray (component 维度消除)
    # 4. 单位转换: * unit_convert -> DataArray (lon, lat, time)

    return (
        dataset[list(variables)].to_array(dim="component").sum(dim="component")
        * unit_convert
    )


def get_pm10_required_variables() -> tuple[str, ...]:
    """
    获取 PM10 计算所需的变量列表

    Returns:
        变量名元组
    """
    return PM10_VARIABLES
