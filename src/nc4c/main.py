"""主模块 - 整合各模块生成图像"""

from nc4c.config import ALL_CONFIGS, LON_RANGE, LAT_RANGE


def create_processor(processor_class, config):
    kwargs = dict(
        input_paths=config["data_files"],
        output_dir=config["output_dir"],
        lon_range=LON_RANGE,
        lat_range=LAT_RANGE,
    )
    if "gradient" in config:
        kwargs["gradient"] = config["gradient"]
    return processor_class(name=config["name"], **kwargs)


def main() -> None:
    """使用默认配置运行"""
    from nc4c.processors import (
        EvaporationCanopyProcessor,
        PM10Processor,
        PotentialEvaporationProcessor,
        SurfaceLatentHeatFluxProcessor,
        TemperatureProcessor,
        TotalEvaporationProcessor,
        VegetationTranspirationProcessor,
        WindProcessor,
    )

    processor_map = {
        # "pm10": PM10Processor,
        # "t2m": TemperatureProcessor,
        # "evaporation_canopy": EvaporationCanopyProcessor,
        # "vegetation_transpiration": VegetationTranspirationProcessor,
        # "potential_evaporation": PotentialEvaporationProcessor,
        # "total_evaporation": TotalEvaporationProcessor,
        # "wind": WindProcessor,
        "latent_heat_flux": SurfaceLatentHeatFluxProcessor,
    }

    for key, processor_cls in processor_map.items():
        config = ALL_CONFIGS[key]
        processor = create_processor(processor_cls, config)
        generated = processor.run()
        print(
            f"Generated {len(generated)} {config['name']} images in {config['output_dir']}"
        )
