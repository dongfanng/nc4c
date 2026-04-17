"""Potential Evaporation 计算模块"""

import xarray as xr

PEV_VARIABLE: tuple[str, ...] = ("pev",)

PEV_UNIT_CONVERT: float = 1000.0


def calculate_evaporation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = PEV_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算潜在蒸发量 (Potential Evaporation)

    Args:
        dataset: 输入数据集
        variables: 变量名列表
        unit_convert: 单位转换系数 (m -> mm), 默认为 None

    Returns:
        蒸发量数据数组，单位 mm
    """
    if unit_convert is None:
        unit_convert = PEV_UNIT_CONVERT

    return dataset[variables[0]] * unit_convert


def calculate_potential_evaporation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = PEV_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算潜在蒸发量 (Potential Evaporation)

    Args:
        dataset: 输入数据集
        variables: 变量名列表
        unit_convert: 单位转换系数 (m -> mm), 默认为 None

    Returns:
        蒸发量数据数组，单位 mm
    """
    if unit_convert is None:
        unit_convert = PEV_UNIT_CONVERT

    return dataset[variables[0]] * unit_convert


def calculate_total_evaporation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = PEV_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算总蒸发量 (Total Evaporation)

    Args:
        dataset: 输入数据集
        variables: 变量名列表
        unit_convert: 单位转换系数 (m -> mm), 默认为 None

    Returns:
        蒸发量数据数组，单位 mm
    """
    if unit_convert is None:
        unit_convert = PEV_UNIT_CONVERT

    return dataset[variables[0]] * unit_convert


def calculate_vegetation_transpiration(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = PEV_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算植被蒸腾量 (Vegetation Transpiration)

    Args:
        dataset: 输入数据集
        variables: 变量名列表
        unit_convert: 单位转换系数 (m -> mm), 默认为 None

    Returns:
        蒸发量数据数组，单位 mm
    """
    if unit_convert is None:
        unit_convert = PEV_UNIT_CONVERT

    return dataset[variables[0]] * unit_convert
