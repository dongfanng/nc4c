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
        LAI_High_VegetationProcessor,
        LAI_Low_VegetationProcessor,
        PM10Processor,
        PotentialEvaporationProcessor,
        SurfaceLatentHeatFluxProcessor,
        SurfaceNetSolarRadiationProcessor,
        SurfaceSensibleHeatFluxProcessor,
        TemperatureProcessor,
        TotalEvaporationProcessor,
        VegetationTranspirationProcessor,
        WindProcessor,
        SoilTypeProcessor,
        HighVegetationTypeProcessor,
        LowVegetationTypeProcessor,
        TotalPrecipitationProcessor,
        SoilMoistureProcessor,
    )

    processor_map = {
        # "pm10": PM10Processor,
        # "t2m": TemperatureProcessor,
        # "evaporation_canopy": EvaporationCanopyProcessor,
        # "vegetation_transpiration": VegetationTranspirationProcessor,
        # "potential_evaporation": PotentialEvaporationProcessor,
        # "total_evaporation": TotalEvaporationProcessor,
        # "wind": WindProcessor,
        # "latent_heat_flux": SurfaceLatentHeatFluxProcessor,
        # "net_solar_radiation": SurfaceNetSolarRadiationProcessor,
        # "sensible_heat_flux": SurfaceSensibleHeatFluxProcessor,
        # "soil_type": SoilTypeProcessor,
        # "high_vegetation_type": HighVegetationTypeProcessor,
        # "low_vegetation_type": LowVegetationTypeProcessor,
        # "lai_low_vegetation": LAI_Low_VegetationProcessor,
        # "lai_high_vegetation": LAI_High_VegetationProcessor,
        # "total_precipitation": TotalPrecipitationProcessor,
        "volumetric_soil_water_layer_1": SoilMoistureProcessor,
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
