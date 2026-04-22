"""Total precipitation calculation module"""

import xarray as xr

TP_VARIABLE: tuple[str, ...] = ("tp",)

TP_UNIT_CONVERT: float = 1000.0


def calculate_total_precipitation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = TP_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    Calculate total precipitation (m -> mm)

    Args:
        dataset: Input dataset containing tp variable
        variables: Variable names to use
        unit_convert: Unit conversion factor (m -> mm), defaults to 1000.0

    Returns:
        Total precipitation data array in mm
    """
    if unit_convert is None:
        unit_convert = TP_UNIT_CONVERT

    return dataset[variables[0]] * unit_convert


def get_tp_required_variables() -> tuple[str, ...]:
    """
    Get required variable list for total precipitation

    Returns:
        Variable name tuple
    """
    return TP_VARIABLE
