"""Low Vegetation Type 数据模型"""

import numpy as np
import xarray as xr

LOW_VEGETATION_VARIABLE: tuple[str, ...] = ("tvl",)

LOW_VEGETATION_CATEGORIES: dict[int, str] = {
    0: "No vegetation - 无植被 (透明)",
    1: "Crops, Mixed farming - 农田/混合农业",
    2: "Grass - 草地",
    7: "Tall grass - 高草",
    9: "Tundra - 苔原",
    10: "Irrigated crops - 灌溉农田",
    11: "Semidesert - 半荒漠",
    13: "Bogs and marshes - 沼泽/湿地",
    16: "Evergreen shrubs - 常绿灌木",
    17: "Deciduous shrubs - 落叶灌木",
    20: "Water and land mixtures - 水陆混合",
}


def calculate_low_vegetation_type(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = LOW_VEGETATION_VARIABLE,
) -> xr.DataArray:
    """
    处理低植被类型数据

    ECMWF GRIB Code table 4.234 分类:
    0=无植被, 1=农田/混合农业, 2=草地, 7=高草, 9=苔原,
    10=灌溉农田, 11=半荒漠, 13=沼泽/湿地, 16=常绿灌木, 17=落叶灌木, 20=水陆混合

    Args:
        dataset: 输入数据集
        variables: 变量名元组

    Returns:
        低植被类型分类数据数组
    """
    raw_data = dataset[variables[0]]
    rounded = np.round(raw_data.values)
    return xr.DataArray(
        rounded,
        dims=raw_data.dims,
        coords=raw_data.coords,
        attrs=raw_data.attrs,
    )


def get_low_vegetation_type_required_variables() -> tuple[str, ...]:
    """
    获取低植被类型计算所需的变量列表

    Returns:
        变量名元组
    """
    return LOW_VEGETATION_VARIABLE
