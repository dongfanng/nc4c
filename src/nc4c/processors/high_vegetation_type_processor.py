"""High Vegetation Type 数据处理器"""

from pathlib import Path

import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.high_vegetation_type import (
    HIGH_VEGETATION_VARIABLE,
    calculate_high_vegetation_type,
)
from nc4c.utils.datetime_utils import format_timestamp_filename
from nc4c.visualization import (
    create_colormap_and_norm,
    create_discrete_colormap_and_norm,
    render_image,
)


class HighVegetationTypeProcessor(BaseDataProcessor):
    """高植被类型图像生成处理器"""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]],
        discrete: bool = False,
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
    ) -> None:
        """
        初始化高植被类型处理器

        Args:
            name: 处理器名称
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            gradient: 分类颜色渐变列表，每对 (边界值, 颜色)
            discrete: 是否为离散分类模式
            lon_range: 经度范围
            lat_range: 纬度范围
        """
        super().__init__(
            name=name,
            input_paths=input_paths,
            output_dir=output_dir,
            gradient=gradient,
            discrete=discrete,
        )
        self.lon_range = lon_range
        self.lat_range = lat_range

    def get_required_variables(self) -> list[str]:
        """获取所需变量列表"""
        return list(HIGH_VEGETATION_VARIABLE)

    def get_output_name(self) -> str:
        """获取输出目录名称"""
        return "high_vegetation_type"

    def load(self) -> xr.Dataset:
        """加载 NetCDF 数据"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """处理高植被类型数据"""
        return calculate_high_vegetation_type(
            dataset=dataset,
            variables=HIGH_VEGETATION_VARIABLE,
        )

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """生成高植被类型图像"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        assert self.gradient is not None
        if self.discrete:
            colormap_obj, norm = create_discrete_colormap_and_norm(self.gradient)
        else:
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
            )
            generated_files.append(output_file)

        return generated_files
