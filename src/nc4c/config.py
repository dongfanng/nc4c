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
    name: str = "pm10"
    data_files: list[str] = field(
        default_factory=lambda: [
            str(p) for p in sorted((DATA_DIR / "pm10_data").glob("*.nc"))
        ]
    )
    output_dir: str = "output/pm10"
    unit: str = "μg/m³"
    gradient: list[tuple[int, str]] = field(
        default_factory=lambda: [
            (0, "#3D82D4"),
            (20, "#C8DDF6"),
            (40, "#EDE787"),
            (60, "#E8DC19"),
            (80, "#EAB939"),
            (100, "#E98F43"),
            (120, "#E15E5D"),
            (160, "#A31B56"),
            (200, "#721638"),
            (300, "#2B0001"),
        ]
    )


@dataclass
class T2MConfig:
    name: str = "2m_temperature"
    data_files: list[str] = field(
        default_factory=lambda: [
            str(DATA_DIR / "raw_met_data" / "2m_temperature.nc"),
        ]
    )
    output_dir: str = "output/2m_temperature"
    unit: str = "°C"
    gradient: list[tuple[int, str]] = field(
        default_factory=lambda: [
            (-40, "#E6E6E6"),
            (-30, "#FFAAFF"),
            (-20, "#910991"),
            (-15, "#24186A"),
            (-10, "#554EB1"),
            (-5, "#3E79C6"),
            (0, "#4BB698"),
            (5, "#59D049"),
            (10, "#BEE43D"),
            (15, "#EBD735"),
            (20, "#EAA43E"),
            (25, "#E56D53"),
            (30, "#BE3066"),
            (40, "#6B1527"),
            (50, "#2B0001"),
        ]
    )


@dataclass
class PotentialEvaporationConfig:
    name: str = "potential_evaporation"
    data_files: list[str] = field(
        default_factory=lambda: [
            str(DATA_DIR / "evaporation_and_runoff" / "potential_evaporation.nc"),
        ]
    )
    output_dir: str = "output/potential_evaporation"
    unit: str = "mm"
    gradient: list[tuple[int, str]] = field(
        default_factory=lambda: [
            (-50, "#8c510a"),
            (-25, "#dfc27d"),
            (-5, "#f6e8c3"),
            (0, "#f7f7f7"),
            (0.5, "#c7eae5"),
            (0.8, "#35978f"),
        ]
    )


cfg = SimpleNamespace(
    geo=GeographicConfig(),
    pm10=PM10Config(),
    t2m=T2MConfig(),
    potential_evaporation=PotentialEvaporationConfig(),
)
