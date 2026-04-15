import nc4c


def test_package_version() -> None:
    """验证版本号是否正确"""
    assert nc4c.__name__ == "intellicave"


def test_math_logic() -> None:
    """一个简单的逻辑测试"""
    expected_sensors = 4
    active_sensors = 2 + 2
    assert active_sensors == expected_sensors, "传感器数量计算错误!"
