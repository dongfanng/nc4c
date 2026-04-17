"""颜色映射模块"""

import matplotlib.pyplot as plt

from nc4c.utils.color_utils import create_gradient_colors


def create_colormap_and_norm(
    gradient: list[tuple[float, str]],
) -> tuple[plt.Colormap, plt.Normalize]:
    """
    根据 gradient 创建色图和归一化对象

    Args:
        gradient: 渐变列表, 每个元素为 (数值, 十六进制颜色)
                  例如 [(0, "#3D82D4"), (20, "#C8DDF6"), ...]

    Returns:
        (色图对象, 归一化对象) 元组
    """
    # Step 1: 将 gradient 转换为 256 色的颜色数组
    color_array = create_gradient_colors(gradient, n_colors=256)
    # Step 2: 创建色图 (colormap) - 将 [0,1] 映射到具体颜色
    colormap = plt.matplotlib.colors.ListedColormap(color_array)
    # Step 3: 从 gradient 首尾获取数值范围
    vmin, vmax = gradient[0][0], gradient[-1][0]
    # Step 4: 创建归一化对象 (norm) - 将实际数据值映射到 [0,1]
    norm = plt.Normalize(vmin=vmin, vmax=vmax, clip=True)
    return colormap, norm
