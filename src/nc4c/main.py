"""主模块 - 整合各模块生成图像"""

from nc4c.config import cfg


def main() -> None:
    """使用默认配置运行"""
    from nc4c.processors import (
        EvaporationCanopyProcessor,
        PotentialEvaporationProcessor,
        PM10Processor,
        TemperatureProcessor,
        TotalEvaporationProcessor,
        VegetationTranspirationProcessor,
        WindProcessor,
    )

    pm10_task = PM10Processor(
        name=cfg.pm10.name,
        input_paths=cfg.pm10.data_files,
        output_dir=cfg.pm10.output_dir,
        gradient=cfg.pm10.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = pm10_task.run()
    # print(f"Generated {len(generated)} PM10 images in {cfg.pm10.output_dir}")

    temp_task = TemperatureProcessor(
        name=cfg.t2m.name,
        input_paths=cfg.t2m.data_files,
        output_dir=cfg.t2m.output_dir,
        gradient=cfg.t2m.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = temp_task.run()
    # print(f"Generated {len(generated)} temperature images in {cfg.t2m.output_dir}")

    evaporation_canopy_task = EvaporationCanopyProcessor(
        name=cfg.evaporation_canopy.name,
        input_paths=cfg.evaporation_canopy.data_files,
        output_dir=cfg.evaporation_canopy.output_dir,
        gradient=cfg.evaporation_canopy.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = evaporation_canopy_task.run()
    # print(
    #     f"Generated {len(generated)} evaporation canopy images in {cfg.evaporation_canopy.output_dir}"
    # )

    vegetation_transpiration_task = VegetationTranspirationProcessor(
        name=cfg.vegetation_transpiration.name,
        input_paths=cfg.vegetation_transpiration.data_files,
        output_dir=cfg.vegetation_transpiration.output_dir,
        gradient=cfg.vegetation_transpiration.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = vegetation_transpiration_task.run()
    # print(f"Generated {len(generated)} vegetation transpiration images in {cfg.vegetation_transpiration.output_dir}")

    potential_evaporation_task = PotentialEvaporationProcessor(
        name=cfg.potential_evaporation.name,
        input_paths=cfg.potential_evaporation.data_files,
        output_dir=cfg.potential_evaporation.output_dir,
        gradient=cfg.potential_evaporation.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = potential_evaporation_task.run()
    # print(f"Generated {len(generated)} potential evaporation images in {cfg.potential_evaporation.output_dir}")

    total_evaporation_task = TotalEvaporationProcessor(
        name=cfg.total_evaporation.name,
        input_paths=cfg.total_evaporation.data_files,
        output_dir=cfg.total_evaporation.output_dir,
        gradient=cfg.total_evaporation.gradient,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    generated = total_evaporation_task.run()
    print(f"Generated {len(generated)} total evaporation images in {cfg.total_evaporation.output_dir}")

    wind_task = WindProcessor(
        name=cfg.wind.name,
        input_paths=cfg.wind.data_files,
        output_dir=cfg.wind.output_dir,
        lon_range=cfg.geo.lon_range,
        lat_range=cfg.geo.lat_range,
    )
    # generated = wind_task.run()
    # print(f"Generated {len(generated)} wind JSON files in {cfg.wind.output_dir}")
