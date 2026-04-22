"""数据处理器模块"""

from nc4c.processors.evaporation_canopy_processor import EvaporationCanopyProcessor
from nc4c.processors.high_vegetation_type_processor import HighVegetationTypeProcessor
from nc4c.processors.lai_low_vegetation_processor import LAI_Low_VegetationProcessor
from nc4c.processors.low_vegetation_type_processor import LowVegetationTypeProcessor
from nc4c.processors.potential_evaporation_processor import (
    PotentialEvaporationProcessor,
)
from nc4c.processors.pm10_processor import PM10Processor
from nc4c.processors.soil_type_processor import SoilTypeProcessor
from nc4c.processors.surface_latent_heat_flux_processor import (
    SurfaceLatentHeatFluxProcessor,
)
from nc4c.processors.surface_net_solar_radiation_processor import (
    SurfaceNetSolarRadiationProcessor,
)
from nc4c.processors.surface_sensible_heat_flux_processor import (
    SurfaceSensibleHeatFluxProcessor,
)
from nc4c.processors.temperature_processor import TemperatureProcessor
from nc4c.processors.total_evaporation_processor import TotalEvaporationProcessor
from nc4c.processors.vegetation_transpiration_processor import (
    VegetationTranspirationProcessor,
)
from nc4c.processors.wind_processor import WindProcessor

__all__ = [
    "EvaporationCanopyProcessor",
    "HighVegetationTypeProcessor",
    "LAI_Low_VegetationProcessor",
    "LowVegetationTypeProcessor",
    "PotentialEvaporationProcessor",
    "PM10Processor",
    "SoilTypeProcessor",
    "SurfaceLatentHeatFluxProcessor",
    "SurfaceNetSolarRadiationProcessor",
    "SurfaceSensibleHeatFluxProcessor",
    "TemperatureProcessor",
    "TotalEvaporationProcessor",
    "VegetationTranspirationProcessor",
    "WindProcessor",
]
