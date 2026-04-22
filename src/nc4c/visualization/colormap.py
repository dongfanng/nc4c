"""颜色映射模块

提供色图（colormap）和归一化（normalization）工具，用于将数据值映射到颜色。

色图原理：
- 数据值 → 归一化(Normalize) → [0,1] 范围 → 色图(Colormap) → 具体颜色

两种模式：
- 连续渐变（Continuous）：数据值连续变化时使用，颜色平滑过渡
- 离散分类（Discrete）：枚举值/分类数据使用，每个值对应固定颜色
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from nc4c.utils.color_utils import create_gradient_colors


def create_colormap_and_norm(
    gradient: list[tuple[float, str]],
) -> tuple[plt.Colormap, plt.Normalize]:
    """
    根据 gradient 创建色图和归一化对象（连续渐变模式）

    适用于温度、PM10、降水等连续变化的数据。数据值越大/越小，
    对应渐变中的颜色就越深/越浅。

    Args:
        gradient: 渐变列表, 每个元素为 (数值, 十六进制颜色)
                  例如 [(0, "#3D82D4"), (20, "#C8DDF6"), ...]
                  列表应按数值从小到大排列

    Returns:
        (色图对象, 归一化对象) 元组
    """
    # 将 gradient 配置转换为 256 色数组，实现平滑颜色过渡
    color_array = create_gradient_colors(gradient, n_colors=256)
    # 创建色图，将 [0,1] 范围的值映射到具体颜色
    colormap = mcolors.ListedColormap(color_array)
    # 从 gradient 首尾获取数值范围，作为归一化的最小/最大值
    vmin, vmax = gradient[0][0], gradient[-1][0]
    # 创建归一化对象，将实际数据值映射到 [0,1] 范围
    norm = plt.Normalize(vmin=vmin, vmax=vmax, clip=True)
    return colormap, norm


def create_discrete_colormap_and_norm(
    gradient: list[tuple[float, str]],
) -> tuple[plt.Colormap, plt.Normalize]:
    """
    根据 gradient 创建色图和归一化对象（离散分类模式）

    适用于土壤类型、植被类型等枚举值数据。每个区间对应一个固定颜色，
    数值落在哪个区间就显示对应颜色。

    Args:
        gradient: 离散分类的渐变列表, 每个元素为 (类别值, 十六进制颜色)
                  例如 [(0, "#C9D8E8"), (1, "#F5DEB3"), (2, "#C8A96E"), ...]
                  类别值必须是整数，如 0, 1, 2, 3 表示不同的土壤类型

    Returns:
        (色图对象, 归一化对象) 元组
    """
    # 提取颜色列表
    colors = [c for _, c in gradient]
    # 创建色图，颜色数量等于类别数量
    colormap = mcolors.ListedColormap(colors)

    # 构建边界：每个类别值前后各取中点作为边界
    # 例如类别 [0, 1, 2] → 边界 [-0.5, 0.5, 1.5, 2.5]
    # 这样类别 0 落在 [-0.5, 0.5)，类别 1 落在 [0.5, 1.5)，以此类推
    boundaries = []
    for i, (val, _) in enumerate(gradient):
        if i == 0:
            boundaries.append(val - 0.5)
        else:
            prev_val = gradient[i - 1][0]
            boundaries.append((prev_val + val) / 2)
    boundaries.append(gradient[-1][0] + 0.5)

    # 创建离散归一化，每个区间对应一个固定颜色
    norm = mcolors.BoundaryNorm(boundaries, colormap.N, extend="neither")

    return colormap, norm
