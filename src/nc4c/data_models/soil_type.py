"""Soil Type 数据模型"""

import numpy as np
import xarray as xr

SOIL_TYPE_VARIABLE: tuple[str, ...] = ("slt",)

SOIL_TYPE_CATEGORIES: dict[int, str] = {
    0: "Water - 海洋/湖泊 (浅蓝灰)",
    1: "Coarse - 砂土，保水性低 (浅黄)",
    2: "Medium - 壤土，最主要类型 (棕黄)",
    3: "Medium-fine - 赭棕，中国广泛分布",
    4: "Fine - 粘土，保水性高 (深红棕)",
    6: "Organic - 高持水量，泥炭/有机土 (深橄榄绿)",
}


def calculate_soil_type(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = SOIL_TYPE_VARIABLE,
) -> xr.DataArray:
    """
    处理土壤类型数据

    ECMWF IFS Soil Type (FAO soil texture) 分类:
    0=Water, 1=Coarse, 2=Medium, 3=Medium-fine, 4=Fine, 6=Organic

    Args:
        dataset: 输入数据集
        variables: 变量名元组

    Returns:
        土壤质地分类数据数组
    """
    raw_data = dataset[variables[0]]

    rounded = np.round(raw_data.values)

    return xr.DataArray(
        rounded,
        dims=raw_data.dims,
        coords=raw_data.coords,
        attrs=raw_data.attrs,
    )


def get_soil_type_required_variables() -> tuple[str, ...]:
    """
    获取土壤类型计算所需的变量列表

    Returns:
        变量名元组
    """
    return SOIL_TYPE_VARIABLE
