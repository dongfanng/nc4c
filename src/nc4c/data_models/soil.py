"""土壤变量计算模块"""

import xarray as xr


def calculate_soil_temperature(
    dataset: xr.Dataset,
    level: int = 1,
) -> xr.DataArray:
    """
    计算土壤温度 (指定层次)

    Args:
        dataset: 包含土壤温度变量的数据集
        level: 土壤层次 (1-4)

    Returns:
        土壤温度数据数组
    """
    var_name = f"TSOIL{level}"
    if var_name not in dataset:
        msg = f"Variable {var_name} not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset[var_name].values,
        dims=dataset[var_name].dims,
        coords=dataset[var_name].coords,
    )

    return result


def calculate_soil_moisture(
    dataset: xr.Dataset,
    level: int = 1,
) -> xr.DataArray:
    """
    计算体积土壤含水量 (指定层次)

    Args:
        dataset: 包含土壤水分变量的数据集
        level: 土壤层次 (1-4)

    Returns:
        土壤含水量数据数组
    """
    var_name = f"WSOIL{level}"
    if var_name not in dataset:
        msg = f"Variable {var_name} not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset[var_name].values,
        dims=dataset[var_name].dims,
        coords=dataset[var_name].coords,
    )

    return result


def get_soil_required_variables() -> dict[str, str]:
    """
    获取土壤变量计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "TSOIL1": "土壤温度 层1",
        "TSOIL2": "土壤温度 层2",
        "TSOIL3": "土壤温度 层3",
        "TSOIL4": "土壤温度 层4",
        "WSOIL1": "体积土壤含水量 层1",
        "WSOIL2": "体积土壤含水量 层2",
        "WSOIL3": "体积土壤含水量 层3",
        "WSOIL4": "体积土壤含水量 层4",
    }
