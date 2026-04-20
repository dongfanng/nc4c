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
    dpi: int = 96,
    *,
    transparent: bool = True,
    lon_range: tuple[float, float] | None = None,
    lat_range: tuple[float, float] | None = None,
    draw_boundaries: bool = False,
    interpolate: bool = True,
    alpha: float = 0.9,
) -> None:
    """
    渲染并保存单帧热力图

    Args:
        data: 数据数组，维度 (lon, lat, time)
        time_index: 时间索引
        output_path: 输出文件路径
        colormap: 颜色映射
        norm: 归一化对象
        dpi: 分辨率
        transparent: 是否透明背景
        lon_range: 经度范围 (min, max)，未提供时使用 DataArray 坐标
        lat_range: 纬度范围 (min, max)，未提供时使用 DataArray 坐标
        draw_boundaries: 是否绘制国境线与海岸线（默认 False）
        interpolate: 是否对原始数据进行双线性插值上采样（默认 True）
        alpha: 图像透明度（0 完全透明，1 完全不透明，默认 0.1）
    """
    # 1. 取时间切片并获取 DataArray 坐标
    data_2d = data.isel(time=time_index)

    # 2. 从 DataArray 坐标获取经纬度数组
    lon_coords = data_2d.coords["lon"].values
    lat_coords = data_2d.coords["lat"].values

    # 2. 确定地理范围：优先使用手动指定值，否则从 DataArray 坐标获取
    if lon_range is not None:
        extent_lon = lon_range
    else:
        extent_lon = (float(lon_coords[0]), float(lon_coords[-1]))

    if lat_range is not None:
        extent_lat = lat_range
    else:
        extent_lat = (float(lat_coords[0]), float(lat_coords[-1]))

    # 3. 根据经纬度跨度计算画布宽高比，确保图像比例与地理范围一致
    lon_span = extent_lon[1] - extent_lon[0]
    lat_span = extent_lat[1] - extent_lat[0]
    aspect_ratio = lon_span / lat_span

    fig_height: float = 4.0  # 默认画布高度（英寸）
    fig_width = fig_height * aspect_ratio

    # 4. 创建画布，使用 PlateCarree 投影
    fig, ax = plt.subplots(
        figsize=(fig_width, fig_height),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )

    # 5. 根据 interpolate 参数决定是否上采样
    if interpolate:
        target_h, target_w = int(fig_height * dpi), int(fig_width * dpi)
        zoom_factor = max(
            target_h / data_2d.sizes["lat"], target_w / data_2d.sizes["lon"]
        )
        data_display = np.asarray(scipy_zoom(data_2d.values, zoom=zoom_factor, order=1))
    else:
        data_display = data_2d.values

    # 6. 绘制国境线与海岸线（可选）
    if draw_boundaries:
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor="gray")
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="gray")

    # 7. 将热力图数据映射到地理坐标
    ax.imshow(
        data_display,
        extent=(*extent_lon, *extent_lat),
        origin="lower",  # 由南向北递增，数组的第一行在底部
        cmap=colormap,
        norm=norm,
        alpha=alpha,  # 设置透明度
        transform=ccrs.PlateCarree(),
    )

    # 8. 隐藏坐标轴，只保留纯图像内容
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
