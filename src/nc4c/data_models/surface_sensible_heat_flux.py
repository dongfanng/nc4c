"""表面感热通量数据计算模块"""

import xarray as xr

VARIABLE_NAME: tuple[str, ...] = ("sshf",)


def calculate_sensible_heat_flux(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = VARIABLE_NAME,
) -> xr.DataArray:
    """
    计算表面感热通量数据

    Args:
        dataset: 输入数据集
        variables: 变量名列表

    Returns:
        感热通量数据数组，单位 J/m²（每小时的累计能量）
    """
    return dataset[variables[0]]


def get_required_variables() -> tuple[str, ...]:
    """
    获取表面感热通量计算所需的变量列表

    Returns:
        变量名元组
    """
    return VARIABLE_NAME
