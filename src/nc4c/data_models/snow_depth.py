"""Snow Depth calculation module"""

import xarray as xr

SNOW_DEPTH_VARIABLE: tuple[str, ...] = ("sde",)

METERS_TO_CM: float = 100.0


def calculate_snow_depth(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = SNOW_DEPTH_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    Calculate snow depth

    Converts meters to centimeters

    Args:
        dataset: Input dataset containing snow depth variable
        variables: Variable names to use
        unit_convert: Unit conversion factor, default m → cm (×100)

    Returns:
        Snow depth data array in cm
    """
    if unit_convert is None:
        unit_convert = METERS_TO_CM

    return dataset[variables[0]] * unit_convert
