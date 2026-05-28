"""风场流线图像处理器"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.wind_streamlines import (
    get_u_v_arrays,
    replace_missing,
)
from nc4c.utils.datetime_utils import format_timestamp_filename

IMG_WIDTH = 4760
IMG_HEIGHT = 1536
DPI = 96

LON_MIN, LON_MAX = 73.0, 135.0
LAT_MIN, LAT_MAX = 33.0, 53.0


class WindStreamlinesProcessor(BaseDataProcessor):
    """风场流线图像生成处理器"""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]] | None = None,
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
        time_range_beijing: tuple[str, str] | None = None,
        line_color: tuple[float, float, float] = (180 / 255, 210 / 255, 255 / 255),
        density: float = 2,
        line_width: float = 1,
        maxlength: float = 1.0,
    ) -> None:
        super().__init__(
            name=name,
            input_paths=input_paths,
            output_dir=output_dir,
            gradient=gradient,
            time_range_beijing=time_range_beijing,
        )
        self.lon_range = lon_range
        self.lat_range = lat_range
        self.line_color = line_color
        self.density = density
        self.line_width = line_width
        self.maxlength = maxlength

    def get_required_variables(self) -> list[str]:
        return ["u10", "v10"]

    def load(self) -> xr.Dataset:
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=3.4028234663852886e38,
            time_range_beijing=self.time_range_beijing,
        )

    def process(self, dataset: xr.Dataset) -> tuple[xr.DataArray, xr.DataArray]:
        return get_u_v_arrays(dataset)

    def save(
        self,
        data: tuple[xr.DataArray, xr.DataArray],
        output_dir: str,
    ) -> list[Path]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        u_data, v_data = data
        n_times = len(u_data.coords["time"])
        lon = u_data.coords["lon"].values
        lat = u_data.coords["lat"].values

        fig_width_inches = IMG_WIDTH / DPI
        fig_height_inches = IMG_HEIGHT / DPI

        generated_files: list[Path] = []

        for time_idx in range(n_times):
            timestamp = u_data.coords["time"].values[time_idx]
            output_file = format_timestamp_filename(output_path, timestamp)

            u_raw = replace_missing(u_data.isel(time=time_idx).values)
            v_raw = replace_missing(v_data.isel(time=time_idx).values)

            speed = np.sqrt(u_raw**2 + v_raw**2)
            speed_max = np.percentile(speed, 95)
            speed_max = max(speed_max, 0.1)
            lw = self.line_width * (0.2 + 0.8 * speed / speed_max)

            fig, ax = plt.subplots(
                figsize=(fig_width_inches, fig_height_inches),
                dpi=DPI,
                facecolor="none",
            )

            ax.set_xlim(LON_MIN, LON_MAX)
            ax.set_ylim(LAT_MIN, LAT_MAX)
            ax.set_aspect("equal")

            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)

            ax.streamplot(
                lon,
                lat,
                u_raw,
                v_raw,
                color=self.line_color,
                density=self.density,
                linewidth=lw,
                arrowsize=0.001,
                maxlength=self.maxlength,
            )

            fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
            fig.savefig(
                str(output_file), dpi=DPI, transparent=True, pad_inches=0
            )
            plt.close(fig)

            generated_files.append(output_file)

        return generated_files
