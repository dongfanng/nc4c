"""日期时间工具函数"""

from pathlib import Path

import numpy as np


def format_timestamp_filename(
    base_dir: Path,
    timestamp: np.datetime64,
    suffix: str = "png",
    utc_offset: int = 8,
    minute_offset: int = 0,
) -> Path:
    """
    生成时间戳文件名（支持时区偏移和分钟偏移）

    Args:
        base_dir: 输出目录
        timestamp: 时间戳（UTC）
        suffix: 文件后缀
        utc_offset: UTC 偏移小时数（默认 8，即东八区）
        minute_offset: 分钟偏移量（默认 0，PM10 数据传入 -30）

    Returns:
        格式为 YYYYMMDDHHMMSS.{suffix} 的文件名
    """
    ts_utc8 = timestamp + np.timedelta64(utc_offset, "h")
    ts_offset = ts_utc8 + np.timedelta64(minute_offset, "m")
    ts_str = str(ts_offset)
    date_part, time_part = ts_str.split("T")
    year_str, month_str, day_str = date_part.split("-")
    hour_str, minute_str, second_str = time_part.split(":")
    second_str = second_str[:2]

    filename = f"{year_str}{month_str}{day_str}{hour_str}{minute_str}{second_str}.{suffix}"
    return base_dir / filename
