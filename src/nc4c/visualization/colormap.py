"""颜色映射模块"""

from __future__ import annotations

import matplotlib.pyplot as plt

from nc4c.utils.color_utils import create_gradient_colors
from nc4c.visualization.colormap_configs import ColormapConfig


def create_colormap(
    gradient: list[tuple[float, str]] | None = None,
    config: ColormapConfig | None = None,
) -> plt.Colormap:
    """
    创建渐变色图

    Args:
        gradient: 渐变列表, 每个元素为 (数值, 十六进制颜色)
        config: ColormapConfig 配置对象, 会覆盖 gradient 参数

    Returns:
        matplotlib 色图对象
    """
    if config is not None:
        gradient = config.gradient

    if gradient is None:
        gradient = [
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

    color_array = create_gradient_colors(gradient, n_colors=256)

    return plt.matplotlib.colors.ListedColormap(color_array)


def get_norm(
    vmin: float = 0.0,
    vmax: float = 300.0,
    config: ColormapConfig | None = None,
) -> plt.Normalize:
    """
    获取颜色归一化对象

    Args:
        vmin: 最小值
        vmax: 最大值
        config: ColormapConfig 配置对象, 会覆盖 vmin 和 vmax

    Returns:
        Normalize 对象 (clip=True 裁剪超出范围的值)
    """
    if config is not None:
        vmin = config.vmin
        vmax = config.vmax

    return plt.Normalize(vmin=vmin, vmax=vmax, clip=True)


def create_colormap_and_norm(
    config: ColormapConfig,
) -> tuple[plt.Colormap, plt.Normalize]:
    """
    根据配置创建色图和归一化对象

    Args:
        config: 色图配置

    Returns:
        (色图对象, 归一化对象) 元组
    """
    colormap = create_colormap(config=config)
    norm = get_norm(config=config)
    return colormap, norm
