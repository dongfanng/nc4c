"""数据处理器模块"""

from nc4c.processors.evaporation_processor import EvaporationProcessor
from nc4c.processors.pm10_processor import PM10Processor
from nc4c.processors.temperature_processor import TemperatureProcessor
from nc4c.processors.wind_processor import WindProcessor

__all__ = ["EvaporationProcessor", "PM10Processor", "TemperatureProcessor", "WindProcessor"]
