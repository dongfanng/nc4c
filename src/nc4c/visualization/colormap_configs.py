"""色图配置模块"""

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class ColormapConfig:
    """色图配置"""

    name: str
    gradient: list[tuple[float, str]]
    unit: str
    vmin: float | None = field(default=None)
    vmax: float | None = field(default=None)
    colormap_factory: Callable | None = field(default=None)

    def __post_init__(self) -> None:
        if not self.gradient:
            raise ValueError(f"[{self.name}] gradient 列表不能为空")
        if self.vmin is None:
            self.vmin = self.gradient[0][0]
        if self.vmax is None:
            self.vmax = self.gradient[-1][0]


PM10_CONFIG = ColormapConfig(
    name="PM10",
    gradient=[
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
    ],
    unit="μg/m³",
)


T2M_CONFIG = ColormapConfig(
    name="2m Temperature",
    gradient=[
        (-30, "#0000FF"),
        (-20, "#5D9CFD"),
        (-10, "#91C7F9"),
        (0, "#C9E8F7"),
        (10, "#F6FAD7"),
        (20, "#F9E5A8"),
        (30, "#F5B041"),
        (40, "#D64545"),
    ],
    unit="°C",
)


SNOW_DEPTH_CONFIG = ColormapConfig(
    name="Snow Depth",
    gradient=[
        (0, "#F7F7F7"),
        (1, "#D9D9D9"),
        (5, "#BFBFBF"),
        (10, "#8C8C8C"),
        (50, "#5E5E5E"),
        (100, "#2B2B2B"),
    ],
    unit="mm",
)


SOIL_MOISTURE_CONFIG = ColormapConfig(
    name="Soil Moisture",
    gradient=[
        (0.0, "#F5DEB3"),
        (0.1, "#DEB887"),
        (0.2, "#8B7355"),
        (0.3, "#6B8E23"),
        (0.4, "#228B22"),
        (0.5, "#006400"),
    ],
    unit="m³/m³",
)


LAI_CONFIG = ColormapConfig(
    name="Leaf Area Index",
    gradient=[
        (0, "#F5F5DC"),
        (1, "#9ACD32"),
        (3, "#228B22"),
        (5, "#006400"),
        (7, "#004040"),
    ],
    unit="m²/m²",
)


PRECIPITATION_CONFIG = ColormapConfig(
    name="Precipitation",
    gradient=[
        (0, "#F7F7F7"),
        (1, "#C8E8F7"),
        (5, "#91C7F9"),
        (10, "#5D9CFD"),
        (25, "#3D82D4"),
        (50, "#E98F43"),
        (100, "#D64545"),
        (200, "#721638"),
    ],
    unit="mm",
)


WIND_SPEED_CONFIG = ColormapConfig(
    name="Wind Speed",
    gradient=[
        (0, "#F7F7F7"),
        (5, "#C8E8F7"),
        (10, "#91C7F9"),
        (15, "#5D9CFD"),
        (20, "#3D82D4"),
        (30, "#E98F43"),
        (50, "#D64545"),
    ],
    unit="m/s",
)

# 注册所有配置
ALL_CONFIGS: dict[str, ColormapConfig] = {
    "pm10": PM10_CONFIG,
    "t2m": T2M_CONFIG,
    "snow": SNOW_DEPTH_CONFIG,
    "soil_moisture": SOIL_MOISTURE_CONFIG,
    "lai": LAI_CONFIG,
    "precipitation": PRECIPITATION_CONFIG,
    "wind": WIND_SPEED_CONFIG,
}


def get_colormap_config(name: str) -> ColormapConfig | None:
    """
    获取指定名称的色图配置

    Args:
        name: 配置名称 (如 "pm10", "t2m")

    Returns:
        色图配置, 如果不存在则返回 None
    """
    return ALL_CONFIGS.get(name.lower())
