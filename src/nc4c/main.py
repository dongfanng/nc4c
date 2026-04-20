"""主模块 - 整合各模块生成图像"""

from nc4c.config import cfg


def main() -> None:
    """使用默认配置运行"""
    from nc4c.processors import EvaporationProcessor, PM10Processor, TemperatureProcessor

    pm10_task = PM10Processor(
        input_paths=cfg.pm10.data_files,
        output_dir=cfg.pm10.output_dir,
        gradient=cfg.pm10.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = pm10_task.run()
    # print(f"Generated {len(generated)} PM10 images in {cfg.pm10.output_dir}")

    temp_task = TemperatureProcessor(
        input_paths=cfg.t2m.data_files,
        output_dir=cfg.t2m.output_dir,
        gradient=cfg.t2m.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = temp_task.run()
    # print(f"Generated {len(generated)} temperature images in {cfg.t2m.output_dir}")

    evaporation_task = EvaporationProcessor(
        input_paths=cfg.potential_evaporation.data_files,
        output_dir=cfg.potential_evaporation.output_dir,
        gradient=cfg.potential_evaporation.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    generated = evaporation_task.run()
    print(f"Generated {len(generated)} evaporation images in {cfg.potential_evaporation.output_dir}")
