"""数据处理器基类模块"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import xarray as xr


class BaseDataProcessor(ABC):
    """
    所有数据处理器的抽象基类

    定义数据处理的通用流程: 加载 -> 处理 -> 保存
    具体的处理器应继承此类并实现相应的抽象方法
    """

    def __init__(
        self,
        input_paths: list[str],
        output_dir: str,
        gradient: list[tuple[float, str]] | None = None,
    ) -> None:
        """
        初始化处理器

        Args:
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            gradient: 颜色渐变列表，用于创建色图
        """
        self.input_paths = input_paths
        self.output_dir = output_dir
        self.gradient = gradient

    def run(self) -> list[Path]:
        """
        执行标准处理流水线

        Returns:
            生成的输出文件路径列表
        """
        data = self.load()
        data = self.process(data)
        return self.save(data, self.output_dir)

    @abstractmethod
    def load(self) -> xr.Dataset:
        """
        加载数据

        Returns:
            加载的数据集
        """
        ...

    @abstractmethod
    def process(self, dataset: xr.Dataset) -> xr.DataArray:
        """
        处理数据

        Args:
            dataset: 输入数据集

        Returns:
            处理后的数据数组
        """
        ...

    @abstractmethod
    def save(self, data: xr.DataArray, output_dir: str) -> list[Path]:
        """
        保存数据

        Args:
            data: 处理后的数据
            output_dir: 输出目录

        Returns:
            输出文件路径列表
        """
        ...

    @abstractmethod
    def get_required_variables(self) -> list[str]:
        """
        获取所需的输入变量列表

        Returns:
            变量名列表
        """
        ...

    @abstractmethod
    def get_output_name(self) -> str:
        """
        获取输出变量名

        Returns:
            输出变量名
        """
        ...
