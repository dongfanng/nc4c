"""Soil Temperature Level 1 数据处理器"""

from pathlib import Path

import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.stl1 import STL1_VARIABLE, calculate_stl1
from nc4c.utils.datetime_utils import format_timestamp_filename
from nc4c.visualization import (
    create_colormap_and_norm,
    render_image,
)


class Stl1Processor(BaseDataProcessor):
    """土壤温度 Level 1 图像生成处理器"""

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
        初始化土壤温度 Level 1 处理器

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
        """获取所需变量列表"""
        return list(STL1_VARIABLE)

    def load(self) -> xr.Dataset:
        """加载 NetCDF 数据"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=3.4028234663852886e38,
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """计算土壤温度（K → °C）"""
        return calculate_stl1(
            dataset=dataset,
            variables=STL1_VARIABLE,
        )

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """生成土壤温度图像"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        assert self.gradient is not None
        colormap_obj, norm = create_colormap_and_norm(self.gradient)

        generated_files: list[Path] = []
        n_times = len(data.coords["time"])

        for time_idx in range(n_times):
            timestamp = data.coords["time"].values[time_idx]
            output_file = format_timestamp_filename(output_path, timestamp)

            render_image(
                data=data,
                time_index=time_idx,
                output_path=output_file,
                colormap=colormap_obj,
                norm=norm,
                lon_range=self.lon_range,
                lat_range=self.lat_range,
                interpolate=False,
            )
            generated_files.append(output_file)

        return generated_files
