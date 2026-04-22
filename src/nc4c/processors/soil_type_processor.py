"""Soil Type 数据处理器"""

from pathlib import Path

import numpy as np
import xarray as xr
from matplotlib.colors import BoundaryNorm, ListedColormap

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.soil_type import SOIL_TYPE_VARIABLE, calculate_soil_type
from nc4c.utils.datetime_utils import format_timestamp_filename


class SoilTypeProcessor(BaseDataProcessor):
    """土壤类型图像生成处理器"""

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
        初始化土壤类型处理器

        Args:
            name: 处理器名称
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            gradient: 分类颜色渐变列表，每对 (边界值, 颜色)
            lon_range: 经度范围
            lat_range: 纬度范围
        """
        super().__init__(
            name=name, input_paths=input_paths, output_dir=output_dir, gradient=gradient
        )
        self.lon_range = lon_range
        self.lat_range = lat_range

    def get_required_variables(self) -> list[str]:
        """获取所需变量列表"""
        return list(SOIL_TYPE_VARIABLE)

    def get_output_name(self) -> str:
        """获取输出目录名称"""
        return "soil_type"

    def load(self) -> xr.Dataset:
        """加载 NetCDF 数据"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """处理土壤类型数据"""
        return calculate_soil_type(
            dataset=dataset,
            variables=SOIL_TYPE_VARIABLE,
        )

    def _parse_gradient(self) -> tuple[list[str], list[float]]:
        """从 gradient 解析出离散颜色和边界

        将连续渐变配置转换为分级设色的离散颜色和边界数组。
        例如 gradient=[(1, '红'), (5, '绿'), (10, '蓝')] 会产生:
        - colors: ['红', '绿', '蓝']
        - bounds: [0.5, 3.0, 7.5, 10.5]

        边界计算规则:
        - 第一个边界: 第一个值 - 0.5
        - 中间边界: (前一个值 + 当前值) / 2 (相邻值的中点)
        - 最后一个边界: 最后一个值 + 0.5
        """
        if self.gradient is None:
            raise ValueError("SoilTypeProcessor requires gradient configuration")

        gradient = self.gradient
        colors: list[str] = []
        bounds: list[float] = []

        for i, (val, color) in enumerate(gradient):
            colors.append(color)
            if i == 0:
                bounds.append(val - 0.5)
            else:
                prev_val = gradient[i - 1][0]
                bounds.append((prev_val + val) / 2)
        bounds.append(gradient[-1][0] + 0.5)

        return colors, bounds

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """生成土壤类型图像"""
        from matplotlib import pyplot as plt

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        colors, bounds = self._parse_gradient()
        cmap = ListedColormap(colors)
        norm = BoundaryNorm(bounds, cmap.N)

        generated_files: list[Path] = []

        if len(data.coords["time"]) == 1:
            timestamp = data.coords["time"].values[0]
            output_file = format_timestamp_filename(output_path, timestamp)
            self._render_image(data, 0, output_file, cmap, norm)
            generated_files.append(output_file)
        else:
            n_times = len(data.coords["time"])
            for time_idx in range(n_times):
                timestamp = data.coords["time"].values[time_idx]
                output_file = format_timestamp_filename(
                    output_path, timestamp, minute_offset=-30
                )
                self._render_image(data, time_idx, output_file, cmap, norm)
                generated_files.append(output_file)

        return generated_files

    def _render_image(
        self,
        data: xr.DataArray,
        time_index: int,
        output_file: Path,
        cmap: ListedColormap,
        norm: BoundaryNorm,
    ) -> None:
        """渲染单帧图像"""
        from matplotlib import pyplot as plt

        fig = plt.figure(figsize=(11.5, 3.75), dpi=96)
        ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))

        time_data = data.isel(time=time_index)

        if self.lon_range is None and "lon" in time_data.coords:
            lon_vals = time_data.coords["lon"].values
            self.lon_range = (float(lon_vals.min()), float(lon_vals.max()))
        if self.lat_range is None and "lat" in time_data.coords:
            lat_vals = time_data.coords["lat"].values
            self.lat_range = (float(lat_vals.min()), float(lat_vals.max()))

        mesh = ax.pcolormesh(
            time_data.coords["lon"].values,
            time_data.coords["lat"].values,
            time_data.values,
            cmap=cmap,
            norm=norm,
            shading="auto",
        )

        ax.set_xlim(self.lon_range)
        ax.set_ylim(self.lat_range)
        ax.set_aspect("equal")
        ax.axis("off")

        fig.savefig(output_file, dpi=96, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
