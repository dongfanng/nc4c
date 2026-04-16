"""配置模块"""

from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"


@dataclass
class GeographicConfig:
    lon_range: tuple[float, float] = (73.0, 135.0)
    lat_range: tuple[float, float] = (33.0, 53.0)


@dataclass
class PM10Config:
    data_files: list[str] = field(default_factory=lambda: [
        str(p) for p in sorted((DATA_DIR / "pm10_data").glob("*.nc"))
    ])
    output_dir: str = "output/pm10"


@dataclass
class T2MConfig:
    data_files: list[str] = field(default_factory=lambda: [
        str(DATA_DIR / "raw_met_data" / "2m_temperature.nc"),
    ])
    output_dir: str = "output/temperature"


cfg = SimpleNamespace(
    geo=GeographicConfig(),
    pm10=PM10Config(),
    t2m=T2MConfig(),
)
