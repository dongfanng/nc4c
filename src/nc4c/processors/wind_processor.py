"""10米风速数据处理器 - 输出JSON格式"""

import json
from pathlib import Path

import numpy as np
import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.u_v_wind import U_VARIABLE, V_VARIABLE, get_u_v_arrays
from nc4c.utils.datetime_utils import format_timestamp_filename


def _replace_missing_values(data: list) -> list:
    """将 numpy NaN 和缺失值替换为 None"""
    result = []
    for val in data:
        if isinstance(val, float) and np.isnan(val):
            result.append(None)
        else:
            result.append(val)
    return result


class WindProcessor(BaseDataProcessor):
    """10米风速U/V分量JSON输出处理器"""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]] | None = None,
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
    ) -> None:
        """
        初始化风速处理器

        Args:
            name: 处理器名称
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            gradient: 颜色渐变列表（可选，此处理器不使用）
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
        return list(U_VARIABLE) + list(V_VARIABLE)

    def load(self) -> xr.Dataset:
        """加载 NetCDF 数据"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=3.4028234663852886e38,
        )

    def process(self, dataset: xr.Dataset) -> tuple[xr.DataArray, xr.DataArray]:
        """获取U和V风速分量"""
        return get_u_v_arrays(dataset=dataset)

    def save(
        self,
        data: tuple[xr.DataArray, xr.DataArray],
        output_dir: str,
    ) -> list[Path]:
        """
        生成风速JSON文件

        Args:
            data: (u_array, v_array) 元组
            output_dir: 输出目录

        Returns:
            生成的JSON文件路径列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        u_data, v_data = data
        n_times = len(u_data.coords["time"])

        generated_files: list[Path] = []

        for time_idx in range(n_times):
            timestamp = u_data.coords["time"].values[time_idx]

            # 保留经度和纬度到1位小数
            lon_vals = np.round(u_data.coords["lon"].values, 1)
            lat_vals = np.round(u_data.coords["lat"].values, 1)

            u_slice = u_data.isel(time=time_idx).values
            v_slice = v_data.isel(time=time_idx).values

            # flatten 顺序（默认按行展开）：纬度（外层）× 经度（内层）
            # shape (201, 621) -> 124821 个值，例：[lat0_lon0, lat0_lon1, ..., lat0_lon620, lat1_lon0, ...]
            # 使用 float() 确保保留两位小数精度
            u_flat = _replace_missing_values(
                [float(f"{v:.2f}") for v in u_slice.flatten()]
            )
            v_flat = _replace_missing_values(
                [float(f"{v:.2f}") for v in v_slice.flatten()]
            )

            # 生成时间戳字符串（用于 JSON 内容）
            output_file = format_timestamp_filename(output_path, timestamp, suffix="json")
            ts_str = output_file.stem
            date_part, time_part = ts_str.split("_")
            year, month, day = date_part.split("-")
            hour, minute, second = time_part.split("-")
            time_str = f"{year}.{month}.{day} {hour}:{minute}:{second}"

            wind_json = {
                "time": time_str,
                "longitude": lon_vals.tolist(),
                "latitude": lat_vals.tolist(),
                "u": u_flat,
                "v": v_flat,
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(wind_json, f, ensure_ascii=False)

            generated_files.append(output_file)

        return generated_files

    def run(self) -> list[Path]:
        """执行处理流水线"""
        dataset = self.load()
        data = self.process(dataset)
        return self.save(data, self.output_dir)
