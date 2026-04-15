"""核心模块"""

from nc4c.core.base_processor import BaseDataProcessor
from nc4c.core.io import read_netcdf

__all__ = ["BaseDataProcessor", "read_netcdf"]
