"""图像渲染模块"""

from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from scipy.ndimage import zoom as scipy_zoom


def render_image(
    data: xr.DataArray,
    time_index: int,
    output_path: str | Path,
    colormap: mcolors.Colormap,
    norm: mcolors.Normalize,
    width: float = 12.4,
    height: float = 4.0,
    dpi: int = 96,
    transparent: bool = True,
    lon_range: tuple[float, float] | None = None,
    lat_range: tuple[float, float] | None = None,
    draw_boundaries: bool = False,
    interpolate: bool = True,
) -> None:
    """
    渲染并保存单帧热力图

    Args:
        data: 数据数组，维度 (lon, lat, time)
        time_index: 时间索引
        output_path: 输出文件路径
        colormap: 颜色映射
        norm: 归一化对象
        width: 图像宽度
        height: 图像高度
        dpi: 分辨率
        transparent: 是否透明背景
        lon_range: 经度范围 (min, max)，未提供时使用 DataArray 坐标
        lat_range: 纬度范围 (min, max)，未提供时使用 DataArray 坐标
        draw_boundaries: 是否绘制国境线与海岸线（默认 False）
        interpolate: 是否对原始数据进行双线性插值上采样（默认 True）
    """
    fig, ax = plt.subplots(
        figsize=(width, height),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )

    # 1. 从三维数据中取出一个时间切片 -> 二维网格 (lat, lon)
    #    切片后仍保留 xarray 坐标信息
    data_2d = data.isel(time=time_index)

    # 2. 从 DataArray 坐标获取经纬度数组
    lon_coords = data_2d.coords["lon"].values
    lat_coords = data_2d.coords["lat"].values

    # 3. 若手动指定了地理范围则使用指定值（用于 regrid 后坐标与边界不一致的情况）
    extent_lon: tuple[float, float]
    extent_lat: tuple[float, float]
    if lon_range is not None:
        extent_lon = lon_range
    else:
        extent_lon = (float(lon_coords[0]), float(lon_coords[-1]))

    if lat_range is not None:
        extent_lat = lat_range
    else:
        extent_lat = (float(lat_coords[0]), float(lat_coords[-1]))

    # 4. 根据 interpolate 参数决定是否上采样
    if interpolate:
        target_h, target_w = int(height * dpi), int(width * dpi)
        zoom_factor = max(target_h / data_2d.sizes["lat"], target_w / data_2d.sizes["lon"])
        data_display = np.asarray(scipy_zoom(data_2d.values, zoom=zoom_factor, order=1))
    else:
        data_display = data_2d.values

    # 7. 绘制国境线与海岸线（可选）
    if draw_boundaries:
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor="gray")
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="gray")

    # 8. extent 将插值后的像素网格映射到地理范围
    ax.imshow(
        data_display,
        extent=(*extent_lon, *extent_lat),
        origin="lower", # 由南向北递增
        cmap=colormap,
        norm=norm,
        transform=ccrs.PlateCarree(),
    )

    # 9. 隐藏坐标轴，只保留纯图像内容
    ax.axis("off")

    # 9. 保存文件，transparent 保留透明背景
    fig.savefig(
        output_path,
        dpi=dpi,
        transparent=transparent,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close(fig)


def generate_time_filename(base_dir: Path, timestamp: np.datetime64) -> Path:
    """
    生成时间戳文件名

    Args:
        base_dir: 输出目录
        timestamp: 时间戳

    Returns:
        完整文件路径
    """
    from nc4c.utils.datetime_utils import format_timestamp_filename

    return format_timestamp_filename(base_dir, timestamp, suffix="png")
