"""总蒸发量数据计算模块"""

import xarray as xr

VARIABLE_NAME: tuple[str, ...] = ("e",)

UNIT_CONVERT: float = 1000.0


def calculate_evaporation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = VARIABLE_NAME,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算总蒸发量数据

    Args:
        dataset: 输入数据集
        variables: 变量名列表
        unit_convert: 单位转换系数 (m -> mm), 默认为 None 表示使用 UNIT_CONVERT

    Returns:
        蒸发数据数组，单位 mm
    """
    if unit_convert is None:
        unit_convert = UNIT_CONVERT

    return dataset[variables[0]] * unit_convert


def get_required_variables() -> tuple[str, ...]:
    """
    获取总蒸发量计算所需的变量列表

    Returns:
        变量名元组
    """
    return VARIABLE_NAME
