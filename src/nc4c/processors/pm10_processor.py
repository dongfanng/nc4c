"""PM10 数据处理器"""

from pathlib import Path

import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.pm10 import PM10_VARIABLES, calculate_pm10
from nc4c.utils.datetime_utils import format_timestamp_filename
from nc4c.visualization import (
    create_colormap_and_norm,
    render_image,
)


class PM10Processor(BaseDataProcessor):
    """PM10 图像生成处理器"""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]],
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
    ) -> None:
        """
        初始化 PM10 处理器

        Args:
            name: 处理器名称
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            gradient: 颜色渐变列表
            lon_range: 经度范围，None 时由渲染器自动从数据坐标确定
            lat_range: 纬度范围，None 时由渲染器自动从数据坐标确定
        """
        super().__init__(
            name=name, input_paths=input_paths, output_dir=output_dir, gradient=gradient
        )
        self.lon_range = lon_range
        self.lat_range = lat_range

    def get_required_variables(self) -> list[str]:
        """获取 PM10 计算所需的变量列表"""
        return list(PM10_VARIABLES)

    def load(self) -> xr.Dataset:
        """加载 NetCDF 数据"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=9.9999999e14,
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """计算 PM10 数据"""
        return calculate_pm10(
            dataset=dataset,
            variables=PM10_VARIABLES,
            unit_convert=1e9,
        )

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """生成 PM10 图像"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        assert self.gradient is not None
        colormap_obj, norm = create_colormap_and_norm(self.gradient)

        generated_files: list[Path] = []
        n_times = len(data.coords["time"])

        for time_idx in range(n_times):
            timestamp = data.coords["time"].values[time_idx]
            output_file = format_timestamp_filename(
                output_path, timestamp, minute_offset=-30
            )

            render_image(
                data=data,
                time_index=time_idx,
                output_path=output_file,
                colormap=colormap_obj,
                norm=norm,
                lon_range=self.lon_range,
                lat_range=self.lat_range,
            )
            generated_files.append(output_file)

        return generated_files
