"""主模块 - 整合各模块生成图像"""

from nc4c.config import ALL_CONFIGS, LON_RANGE, LAT_RANGE, TIME_RANGE_BEIJING
from nc4c.processors import (
    EvaporationCanopyProcessor,
    HighVegetationTypeProcessor,
    LAI_High_VegetationProcessor,
    LAI_Low_VegetationProcessor,
    LowVegetationTypeProcessor,
    PM10Processor,
    PotentialEvaporationProcessor,
    SnowDepthProcessor,
    SoilMoistureProcessor,
    SoilTypeProcessor,
    Stl1Processor,
    SurfaceLatentHeatFluxProcessor,
    SurfaceNetSolarRadiationProcessor,
    SurfaceSensibleHeatFluxProcessor,
    TemperatureProcessor,
    TotalEvaporationProcessor,
    TotalPrecipitationProcessor,
    VegetationTranspirationProcessor,
    WindProcessor,
)

INVARIANT_CONFIGS = {"soil_type", "high_vegetation_type", "low_vegetation_type"}


def create_processor(processor_class, config):
    kwargs: dict[str, object] = dict(
        input_paths=config["data_files"],
        output_dir=config["output_dir"],
        lon_range=LON_RANGE,
        lat_range=LAT_RANGE,
    )
    if "gradient" in config:
        kwargs["gradient"] = config["gradient"]
    if "discrete" in config:
        kwargs["discrete"] = config["discrete"]
    if config["name"] not in INVARIANT_CONFIGS:
        kwargs["time_range_beijing"] = TIME_RANGE_BEIJING
    return processor_class(name=config["name"], **kwargs)


def main() -> None:
    """使用默认配置运行"""
    processor_map = {
        "pm10": PM10Processor,
        # "t2m": TemperatureProcessor,
        # "evaporation_canopy": EvaporationCanopyProcessor,
        # "vegetation_transpiration": VegetationTranspirationProcessor,
        # "potential_evaporation": PotentialEvaporationProcessor,
        # "total_evaporation": TotalEvaporationProcessor,
        "wind": WindProcessor,
        # "latent_heat_flux": SurfaceLatentHeatFluxProcessor,
        # "net_solar_radiation": SurfaceNetSolarRadiationProcessor,
        # "sensible_heat_flux": SurfaceSensibleHeatFluxProcessor,
        "soil_type": SoilTypeProcessor,
        # "high_vegetation_type": HighVegetationTypeProcessor,
        # "low_vegetation_type": LowVegetationTypeProcessor,
        # "lai_low_vegetation": LAI_Low_VegetationProcessor,
        # "lai_high_vegetation": LAI_High_VegetationProcessor,
        # "total_precipitation": TotalPrecipitationProcessor,
        # "volumetric_soil_water_layer_1": SoilMoistureProcessor,
        # "soil_temperature_level_1": Stl1Processor,
        # "snow_depth": SnowDepthProcessor,
    }

    total_processors = len(processor_map)
    for idx, (key, processor_cls) in enumerate(processor_map.items(), start=1):
        config = ALL_CONFIGS[key]
        processor = create_processor(processor_cls, config)
        print(f"[{idx}/{total_processors}] Processing {config['name']}...")
        generated = processor.run()
        print(
            f"[{idx}/{total_processors}] Generated {len(generated)} {config['name']} images in {config['output_dir']}"
        )
