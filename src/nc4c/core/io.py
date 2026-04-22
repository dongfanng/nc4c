"""核心 IO 模块"""

from __future__ import annotations

from typing import Any

import xarray as xr

_COORD_MAPPING: dict[str, list[str]] = {
    "lon": ["longitude", "lng"],
    "lat": ["latitude"],
    "time": ["valid_time", "time_counter", "forecast_time"],
}

_MISSING_VALUE_ATTRS: tuple[str, ...] = (
    "missing_value",
    "missingValue",
    "FillValue",
    "_FillValue",
    "grib_missing_value",
    "GRIB_missingValue",
)

_DEFAULT_MISSING_VALUE: float = 9.9999999e14


def read_netcdf(
    file_paths: list[str],
    variables: list[str] | None = None,
    lon_range: list[float] | None = None,
    lat_range: list[float] | None = None,
    missing_value: float | None = None,
    time_range_beijing: tuple[str, str] | None = None,
) -> xr.Dataset:
    """
    读取 NetCDF 文件

    Args:
        file_paths: NetCDF 文件路径列表
        variables: 要读取的变量名列表
        lon_range: 经度范围 [min, max]
        lat_range: 纬度范围 [min, max]
        missing_value: 缺失值，为 None 时自动从元数据读取
        time_range_beijing: 时间范围 (开始, 结束)，使用北京时间 (UTC+8)
                            格式: "YYYY-MM-DD HH:00"，例如 ("2023-03-19 00:00", "2023-03-24 23:00")

    Returns:
        合并后的 xarray Dataset
    """
    datasets: list[xr.Dataset] = []
    time_dim: str | None = None
    detected_missing: float | None = None

    for file_path in file_paths:
        ds = xr.open_dataset(file_path)

        if detected_missing is None:
            detected_missing = _detect_missing_value(ds)

        if variables is not None:
            data_vars = {var: ds[var] for var in variables if var in ds}
            ds_subset = xr.Dataset(data_vars)
        else:
            ds_subset = ds

        if lon_range is not None and lat_range is not None:
            ds_subset = _crop_geographic(ds_subset, lon_range, lat_range)

        if time_dim is None:
            time_dim = _detect_time_dim(ds_subset)

        datasets.append(ds_subset)

    combined = xr.concat(datasets, dim=time_dim)
    if time_dim != "time":
        combined = combined.rename({time_dim: "time"})
    combined = _normalize_coords(combined)

    final_missing = (
        missing_value
        if missing_value is not None
        else (
            detected_missing if detected_missing is not None else _DEFAULT_MISSING_VALUE
        )
    )
    combined = _replace_missing(combined, missing_value=final_missing)

    if time_range_beijing is not None:
        combined = _filter_by_time_beijing(combined, time_range_beijing)

    return combined


def _normalize_coords(dataset: xr.Dataset) -> xr.Dataset:
    """
    标准化坐标名称和纬度顺序

    将 longitude→lon, latitude→lat 等别名统一为标准名称
    自动将经纬度转换为升序排列
    经度范围是[-180, 180]，纬度范围是[-90, 90]

    Args:
        dataset: 输入数据集

    Returns:
        坐标名称标准化、经纬度升序排列的数据集
    """
    rename_dict = {
        alias: standard
        for standard, aliases in _COORD_MAPPING.items()
        for alias in aliases
        if alias in dataset.coords
    }
    if rename_dict:
        dataset = dataset.rename(rename_dict)
    dataset = dataset.sortby(["lon", "lat"], ascending=True)

    if "lon" in dataset.coords:
        lon_vals = dataset.coords["lon"].values
        if len(lon_vals) > 0 and lon_vals[-1] > 180:
            dataset = dataset.assign_coords(
                lon=((dataset.coords["lon"].values - 180) % 360) - 180
            )
            dataset = dataset.sortby("lon")

    return dataset


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
        lat_vals = dataset.coords["lat"].values
        if len(lat_vals) > 1:
            lat_ascending = lat_vals[0] < lat_vals[-1]
            if lat_ascending:
                dataset = dataset.sel(lat=slice(lat_min, lat_max))
            else:
                dataset = dataset.sel(lat=slice(lat_max, lat_min))
    if "latitude" in dataset.coords:
        lat_vals = dataset.coords["latitude"].values
        if len(lat_vals) > 1:
            lat_ascending = lat_vals[0] < lat_vals[-1]
            if lat_ascending:
                dataset = dataset.sel(latitude=slice(lat_min, lat_max))
            else:
                dataset = dataset.sel(latitude=slice(lat_max, lat_min))
    if "longitude" in dataset.coords:
        dataset = dataset.sel(longitude=slice(lon_min, lon_max))

    return dataset


def _detect_time_dim(dataset: xr.Dataset) -> str:
    """
    检测时间维度名称

    Args:
        dataset: 输入数据集

    Returns:
        时间维度名称
    """
    common_time_names = ("time", "valid_time", "time_counter", "forecast_time")
    for name in common_time_names:
        if name in dataset.dims:
            return name
    raise ValueError(
        f"Cannot find time dimension in dataset. Available dims: {list(dataset.dims)}"
    )


def _detect_missing_value(dataset: xr.Dataset) -> float:
    """
    从数据集的变量属性中检测缺失值

    尝试常见的缺失值属性名（missing_value, FillValue, _FillValue, grib_missing_value）
    如果都找不到，则使用默认值

    Args:
        dataset: 输入数据集

    Returns:
        缺失值
    """
    for var_name in dataset.data_vars:
        var = dataset[var_name]
        for attr in _MISSING_VALUE_ATTRS:
            if attr in var.attrs:
                return float(var.attrs[attr])
    return _DEFAULT_MISSING_VALUE


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
    return dataset.where(dataset != missing_value)  # 缺失值 → nan


def _filter_by_time_beijing(
    dataset: xr.Dataset,
    time_range_beijing: tuple[str, str],
) -> xr.Dataset:
    """
    按北京时间过滤数据

    Args:
        dataset: 输入数据集
        time_range_beijing: 时间范围 (开始, 结束)，使用北京时间 (UTC+8)
                            格式: "YYYY-MM-DD HH:00"

    Returns:
        过滤后的数据集
    """
    import numpy as np

    start_bj, end_bj = time_range_beijing
    start_utc = np.datetime64(start_bj) - np.timedelta64(8, "h")
    end_utc = np.datetime64(end_bj) - np.timedelta64(8, "h")

    time_coord = dataset.coords["time"].values
    mask = (time_coord >= start_utc) & (time_coord <= end_utc)
    return dataset.isel(time=np.where(mask)[0])


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
