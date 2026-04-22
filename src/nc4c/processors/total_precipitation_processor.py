"""Total precipitation data processor"""

from pathlib import Path

import xarray as xr

from nc4c.core import BaseDataProcessor, read_netcdf
from nc4c.data_models.total_precipitation import (
    TP_VARIABLE,
    calculate_total_precipitation,
)
from nc4c.utils.datetime_utils import format_timestamp_filename
from nc4c.visualization import create_colormap_and_norm, render_image


class TotalPrecipitationProcessor(BaseDataProcessor):
    """Total precipitation image generation processor"""

    def __init__(
        self,
        name: str,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]],
        lon_range: tuple[float, float] | None = None,
        lat_range: tuple[float, float] | None = None,
        time_range_beijing: tuple[str, str] | None = None,
    ) -> None:
        """
        Initialize TotalPrecipitation processor

        Args:
            name: Processor name
            input_paths: Input file paths
            output_dir: Output directory
            gradient: Color gradient list
            lon_range: Longitude range, None for auto-detect
            lat_range: Latitude range, None for auto-detect
            time_range_beijing: Time range (start, end) in Beijing time (UTC+8)
        """
        super().__init__(
            name=name,
            input_paths=input_paths,
            output_dir=output_dir,
            gradient=gradient,
            time_range_beijing=time_range_beijing,
        )
        self.lon_range = lon_range
        self.lat_range = lat_range

    def get_required_variables(self) -> list[str]:
        """Get required variable list"""
        return list(TP_VARIABLE)

    def load(self) -> xr.Dataset:
        """Load NetCDF data"""
        return read_netcdf(
            file_paths=self.input_paths,
            variables=self.get_required_variables(),
            lon_range=list(self.lon_range) if self.lon_range is not None else None,
            lat_range=list(self.lat_range) if self.lat_range is not None else None,
            missing_value=3.4028234663852886e38,
            time_range_beijing=self.time_range_beijing,
        )

    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """Calculate total precipitation (m -> mm)"""
        return calculate_total_precipitation(
            dataset=dataset,
            variables=TP_VARIABLE,
        )

    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """Generate total precipitation images"""
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
            )
            generated_files.append(output_file)

        return generated_files
