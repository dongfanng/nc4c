"""主模块 - 整合各模块生成图像"""

from __future__ import annotations

from pathlib import Path

from nc4c import config
from nc4c.core import read_netcdf
from nc4c.data_models import PM10_VARIABLES, calculate_pm10
from nc4c.visualization import (
    create_colormap_and_norm,
    generate_time_filename,
    get_colormap_config,
    render_image,
)


def generate_pm10_images(
    nc_files: list[str] | str,
    output_dir: str,
) -> list[Path]:
    """
    生成所有 PM10 图像

    Args:
        nc_files: NetCDF 文件路径或路径列表
        output_dir: 输出目录

    Returns:
        生成的图像文件路径列表
    """
    if isinstance(nc_files, str):
        nc_files = [nc_files]

    _lon_range: tuple[float, float] = config.LON_RANGE
    _lat_range: tuple[float, float] = config.LAT_RANGE

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    dataset = read_netcdf(
        file_paths=nc_files,
        variables=list(PM10_VARIABLES),
        lon_range=list(_lon_range),
        lat_range=list(_lat_range),
        missing_value=9.9999999e14,
    )

    pm10_data = calculate_pm10(
        dataset=dataset,
        variables=PM10_VARIABLES,
        unit_convert=1e9,
    )

    pm10_config = get_colormap_config("pm10")
    if pm10_config is None:
        raise ValueError("Colormap config 'pm10' not found")
    colormap_obj, norm = create_colormap_and_norm(pm10_config)

    generated_files: list[Path] = []
    n_times = len(pm10_data.coords["time"])

    for time_idx in range(n_times):
        timestamp = pm10_data.coords["time"].values[time_idx]
        output_file = generate_time_filename(output_path, timestamp)

        render_image(
            data=pm10_data,
            time_index=time_idx,
            output_path=output_file,
            colormap=colormap_obj,
            norm=norm,
            lon_range=_lon_range,
            lat_range=_lat_range,
        )
        generated_files.append(output_file)

    return generated_files


def main() -> None:
    """使用默认配置运行"""
    nc_files = config.NC_FILES
    output_dir = config.OUTPUT_DIR

    generated = generate_pm10_images(
        nc_files=nc_files,
        output_dir=output_dir,
    )

    print(f"Generated {len(generated)} PM10 images in {output_dir}")
