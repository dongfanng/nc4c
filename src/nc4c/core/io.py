"""核心 IO 模块"""

from __future__ import annotations

from typing import Any

import xarray as xr


def read_netcdf(
    file_paths: list[str],
    variables: list[str] | None = None,
    lon_range: list[float] | None = None,
    lat_range: list[float] | None = None,
    missing_value: float = 9.9999999e14,
) -> xr.Dataset:
    """
    读取 NetCDF 文件

    Args:
        file_paths: NetCDF 文件路径列表
        variables: 要读取的变量名列表
        lon_range: 经度范围 [min, max]
        lat_range: 纬度范围 [min, max]
        missing_value: 缺失值

    Returns:
        合并后的 xarray Dataset
    """
    datasets: list[xr.Dataset] = []

    for file_path in file_paths:
        ds = xr.open_dataset(file_path)

        if variables is not None:
            data_vars = {var: ds[var] for var in variables if var in ds}
            ds_subset = xr.Dataset(data_vars)
        else:
            ds_subset = ds

        if lon_range is not None and lat_range is not None:
            ds_subset = _crop_geographic(ds_subset, lon_range, lat_range)

        datasets.append(ds_subset)

    combined = xr.concat(datasets, dim="time")
    combined = _replace_missing(combined, missing_value=missing_value)

    return combined


def _crop_geographic(
    dataset: xr.Dataset,
    lon_range: list[float],
    lat_range: list[float],
) -> xr.Dataset:
    """
    按地理范围裁剪数据

    Args:
        dataset: 输入数据集
        lon_range: 经度范围 [min, max]
        lat_range: 纬度范围 [min, max]

    Returns:
        裁剪后的数据集
    """
    lon_min, lon_max = lon_range
    lat_min, lat_max = lat_range

    if "lon" in dataset.coords:
        dataset = dataset.sel(lon=slice(lon_min, lon_max))
    if "lat" in dataset.coords:
        dataset = dataset.sel(lat=slice(lat_min, lat_max))
    if "latitude" in dataset.coords:
        dataset = dataset.sel(latitude=slice(lat_min, lat_max))
    if "longitude" in dataset.coords:
        dataset = dataset.sel(longitude=slice(lon_min, lon_max))

    return dataset


def _replace_missing(
    dataset: xr.Dataset,
    missing_value: float,
) -> xr.Dataset:
    """
    替换缺失值为 NaN

    Args:
        dataset: 输入数据集
        missing_value: 缺失值

    Returns:
        替换后的数据集
    """
    return dataset.where(dataset != missing_value)


def get_time_range(dataset: xr.Dataset) -> tuple[Any, Any]:
    """
    获取数据集的时间范围

    Args:
        dataset: 输入数据集

    Returns:
        (开始时间, 结束时间) 元组
    """
    time_coord = dataset.coords["time"].values
    return (time_coord[0], time_coord[-1])
