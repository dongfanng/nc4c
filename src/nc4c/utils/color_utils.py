"""颜色处理工具函数"""

import numpy as np


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    将十六进制颜色转换为 RGB 元组

    Args:
        hex_color: 十六进制颜色字符串, 如 #FF0000

    Returns:
        RGB 元组, 如 (255, 0, 0)
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """
    将 RGB 元组转换为十六进制颜色字符串

    Args:
        rgb: RGB 元组, 如 (255, 0, 0)

    Returns:
        十六进制颜色字符串, 如 #FF0000
    """
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def interpolate_color(
    color1: str,
    color2: str,
    factor: float,
) -> str:
    """
    在两个颜色之间进行线性插值

    Args:
        color1: 起始颜色 (十六进制)
        color2: 结束颜色 (十六进制)
        factor: 插值因子, 0.0 返回 color1, 1.0 返回 color2

    Returns:
        插值后的十六进制颜色
    """
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * factor)
    g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * factor)
    b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * factor)
    rgb: tuple[int, int, int] = (r, g, b)

    return rgb_to_hex(rgb)


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> tuple[int, int, int, float]:
    """
    将十六进制颜色转换为 RGBA 元组

    Args:
        hex_color: 十六进制颜色字符串
        alpha: 透明度, 0.0-1.0

    Returns:
        RGBA 元组
    """
    rgb = hex_to_rgb(hex_color)
    return (*rgb, alpha)


def create_gradient_colors(
    gradient: list[tuple[float, str]],
    n_colors: int = 256,
) -> np.ndarray:
    """
    创建渐变色数组, 用于生成色图

    根据渐变定义生成一组平滑过渡的颜色数组。
    渐变列表每个元素为 (数值, 颜色), 数值通常代表数据的阈值。

    Args:
        gradient: 渐变列表, 每个元素为 (数值, 十六进制颜色)
        n_colors: 生成的颜色数量

    Returns:
        颜色数组, 形状为 (n_colors, 4), 每行包含 RGBA 值
    """
    colors = [c for _, c in gradient]
    values = [v for v, _ in gradient]

    color_array = np.zeros((n_colors, 4))

    for i in range(n_colors):
        # 将索引 i (0 ~ n_colors-1) 映射到实际数值范围 (values[0] ~ values[-1])
        # 例如 gradient=[(-40, "#a"), (0, "#b"), (50, "#c")] 时:
        #   i=0   → t=-40  (最冷端)
        #   i=128 → t=5    (中间位置)
        #   i=255 → t=50   (最热端)
        t = values[0] + (values[-1] - values[0]) * (i / (n_colors - 1))

        for j in range(len(values) - 1):
            if values[j] <= t <= values[j + 1]:
                # 在当前区间内做线性插值
                segment_range = values[j + 1] - values[j]
                local_t = (t - values[j]) / segment_range
                interp_color = interpolate_color(colors[j], colors[j + 1], local_t)
                r, g, b, a = hex_to_rgba(interp_color)
                color_array[i] = (r / 255.0, g / 255.0, b / 255.0, a)
                break

    return color_array
