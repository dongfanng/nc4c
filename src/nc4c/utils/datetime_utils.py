"""日期时间工具函数"""

from pathlib import Path

import numpy as np


def format_timestamp_filename(
    base_dir: Path,
    timestamp: np.datetime64,
    suffix: str = "png",
    minute_offset: int = 0,
) -> Path:
    """
    生成UTC时间戳文件名（ISO 8601格式，支持分钟偏移）

    Args:
        base_dir: 输出目录
        timestamp: 时间戳（UTC）
        suffix: 文件后缀
        minute_offset: 分钟偏移量（默认 0，PM10 数据传入 -30）

    Returns:
        格式为 YYYY-MM-DDTHH_MM_SSZ.{suffix} 的文件名（Windows 兼容）
    """
    ts_offset = timestamp + np.timedelta64(minute_offset, "m")
    ts_str = str(ts_offset)
    date_part, time_part = ts_str.split("T")
    year_str, month_str, day_str = date_part.split("-")
    hour_str, minute_str, second_str = time_part.split(":")
    second_str = second_str[:2]

    filename = f"{year_str}-{month_str}-{day_str}T{hour_str}_{minute_str}_{second_str}Z.{suffix}"
    return base_dir / filename
