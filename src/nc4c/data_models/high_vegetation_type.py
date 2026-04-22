"""High Vegetation Type 数据模型"""

import numpy as np
import xarray as xr

HIGH_VEGETATION_VARIABLE: tuple[str, ...] = ("tvh",)

HIGH_VEGETATION_CATEGORIES: dict[int, str] = {
    0: "No high vegetation - 无高植被 (透明)",
    3: "Evergreen needleleaf trees - 常绿针叶树",
    4: "Deciduous needleleaf trees - 落叶针叶树",
    5: "Deciduous broadleaf trees - 落叶阔叶树",
    6: "Evergreen broadleaf trees - 常绿阔叶树",
    18: "Mixed forest/woodland - 混交林/林地",
    19: "Interrupted forest - 间断森林",
}


def calculate_high_vegetation_type(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = HIGH_VEGETATION_VARIABLE,
) -> xr.DataArray:
    """
    处理高植被类型数据

    ECMWF GRIB Code table 4.234 分类:
    0=无植被, 3=落叶阔叶疏林, 4=常绿针叶林, 5=落叶针叶林,
    6=混交林, 18=农田/灌木/草地镶嵌, 19=裸地

    Args:
        dataset: 输入数据集
        variables: 变量名元组

    Returns:
        高植被类型分类数据数组
    """
    raw_data = dataset[variables[0]]
    rounded = np.round(raw_data.values)
    return xr.DataArray(
        rounded,
        dims=raw_data.dims,
        coords=raw_data.coords,
        attrs=raw_data.attrs,
    )


def get_high_vegetation_type_required_variables() -> tuple[str, ...]:
    """
    获取高植被类型计算所需的变量列表

    Returns:
        变量名元组
    """
    return HIGH_VEGETATION_VARIABLE
