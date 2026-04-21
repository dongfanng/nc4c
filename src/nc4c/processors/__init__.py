"""数据处理器模块"""

from nc4c.processors.evaporation_canopy_processor import EvaporationCanopyProcessor
from nc4c.processors.potential_evaporation_processor import (
    PotentialEvaporationProcessor,
)
from nc4c.processors.pm10_processor import PM10Processor
from nc4c.processors.temperature_processor import TemperatureProcessor
from nc4c.processors.total_evaporation_processor import TotalEvaporationProcessor
from nc4c.processors.vegetation_transpiration_processor import (
    VegetationTranspirationProcessor,
)
from nc4c.processors.wind_processor import WindProcessor

__all__ = [
    "EvaporationCanopyProcessor",
    "PotentialEvaporationProcessor",
    "PM10Processor",
    "TemperatureProcessor",
    "TotalEvaporationProcessor",
    "VegetationTranspirationProcessor",
    "WindProcessor",
]
