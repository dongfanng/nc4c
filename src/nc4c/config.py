"""配置模块"""

from pathlib import Path

from nc4c.data_models.pm10 import PM10_UNIT_CONVERT

LON_RANGE: tuple[float, float] = (73.0, 135.0)
LAT_RANGE: tuple[float, float] = (33.0, 53.0)

MISSING_VALUE: float = 9.9999999e14

FIG_WIDTH: float = 12.4
FIG_HEIGHT: float = 4.0
DPI: int = 96

DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"

NC_FILES: list[str] | str = [
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230318.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230319.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230320.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230321.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230322.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230323.SUB.nc"),
    str(DATA_DIR / "pm10_data" / "MERRA2_400.tavg1_2d_aer_Nx.20230324.SUB.nc"),
]

OUTPUT_DIR: str = "output/pm10"

TIME_RANGE: list[str] = ["2023-03-19 00:00", "2023-03-24 23:00"]

ASPECT_RATIO: float = 3.1

TRANSPARENT: bool = True

UNIT_CONVERT: float = PM10_UNIT_CONVERT

TIME_OFFSET_MINUTES: int = 30
