"""日期时间工具函数"""

from pathlib import Path

import numpy as np


def format_timestamp_filename(
    base_dir: Path,
    timestamp: np.datetime64,
    suffix: str = "png",
    utc_offset: int = 8,
) -> Path:
    """
    生成时间戳文件名（支持时区偏移）

    Args:
        base_dir: 输出目录
        timestamp: 时间戳（UTC）
        suffix: 文件后缀
        utc_offset: UTC 偏移小时数（默认 8，即东八区）
    """
    ts_utc8 = timestamp + np.timedelta64(utc_offset, "h")
    ts_str = str(ts_utc8)
    date_part, time_part = ts_str.split("T")
    year_str, month_str, day_str = date_part.split("-")
    hour_str = time_part.split(":")[0]

    filename = f"{year_str}{month_str}{day_str}{hour_str}00.{suffix}"
    return base_dir / filename


def parse_timestamp(timestamp: np.datetime64) -> dict[str, int]:
    """
    解析时间戳为组成部分

    Args:
        timestamp: numpy datetime64 时间戳

    Returns:
        包含 year, month, day, hour 的字典
    """
    ts_str = str(timestamp)
    date_part, time_part = ts_str.split("T")
    year_str, month_str, day_str = date_part.split("-")
    hour_str = time_part.split(":")[0]

    return {
        "year": int(year_str),
        "month": int(month_str),
        "day": int(day_str),
        "hour": int(hour_str),
    }


def calculate_hour_difference(
    timestamp: np.datetime64,
    base_timestamp: np.datetime64,
) -> int:
    """
    计算两个时间戳之间的小时差

    Args:
        timestamp: 目标时间戳
        base_timestamp: 基准时间戳

    Returns:
        小时差
    """
    diff = (timestamp - base_timestamp) / np.timedelta64(3600, "s")
    return int(diff)
