"""配置模块"""

from pathlib import Path

DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"

LON_RANGE = (73.0, 135.0)
LAT_RANGE = (33.0, 53.0)

TIME_RANGE_BEIJING: tuple[str, str] = ("2023-03-19 00:00", "2023-03-24 23:59")

PM10 = {
    "name": "PM10",
    "data_files": [str(p) for p in sorted((DATA_DIR / "pm10_data").glob("*.nc"))],
    "output_dir": "output/PM10",
    # PM10 质量浓度，单位: μg/m³
    # 数据范围: 0 ~ 300 μg/m³ (中国标准: 75=良, 150=轻度污染, 250=重度)
    "gradient": [
        (0, "#3D82D4"),
        (20, "#C8DDF6"),
        (40, "#EDE787"),
        (60, "#E8DC19"),
        (80, "#EAB939"),
        (100, "#E98F43"),
        (120, "#E15E5D"),
        (160, "#A31B56"),
        (200, "#721638"),
        (300, "#2B0001"),
    ],
}

T2M = {
    "name": "2m_temperature",
    "data_files": [str(DATA_DIR / "raw_met_data" / "2m_temperature.nc")],
    "output_dir": "output/2m_temperature",
    # 地表气温，单位: °C (原始数据为 K，需 -273.15 转换)
    # 数据范围: -40 ~ 50°C
    "gradient": [
        (-40, "#E6E6E6"),
        (-30, "#FFAAFF"),
        (-20, "#910991"),
        (-15, "#24186A"),
        (-10, "#554EB1"),
        (-5, "#3E79C6"),
        (0, "#4BB698"),
        (5, "#59D049"),
        (10, "#BEE43D"),
        (15, "#EBD735"),
        (20, "#EAA43E"),
        (25, "#E56D53"),
        (30, "#BE3066"),
        (40, "#6B1527"),
        (50, "#2B0001"),
    ],
}

POTENTIAL_EVAPORATION = {
    "name": "potential_evaporation",
    "data_files": [
        str(DATA_DIR / "evaporation_and_runoff" / "potential_evaporation.nc")
    ],
    "output_dir": "output/potential_evaporation",
    # 潜在蒸发量，单位: mm (原始数据为 m，需 ×1000 转换)
    # 负值=蒸发(放热)，正值=凝结(吸热)
    # 数据范围: -52.1 ~ 0.8 mm
    "gradient": [
        (-52, "#5D3A1A"),
        (-30, "#8c510a"),
        (-10, "#d8b365"),
        (-1, "#f6e8c3"),
        (0, "#00000000"),
        (0.001, "#c7eae5"),
        (0.8, "#35978f"),
    ],
}

EVAPORATION_CANOPY = {
    "name": "evaporation_from_the_top_of_canopy",
    "data_files": [
        str(
            DATA_DIR
            / "evaporation_and_runoff"
            / "evaporation_from_the_top_of_canopy.nc"
        )
    ],
    "output_dir": "output/evaporation_from_top_of_canopy",
    # 冠层顶部蒸发量，单位: mm (原始数据为 m，需 ×1000 转换)
    # 负值=蒸发，正值=凝结
    # 数据范围: -10.2 ~ 0.2 mm
    "gradient": [
        (-10, "#5D3A1A"),
        (-5, "#8c510a"),
        (-1, "#d8b365"),
        (-0.1, "#f6e8c3"),
        (0, "#00000000"),
        (0.001, "#c7eae5"),
        (0.2, "#35978f"),
    ],
}

VEGETATION_TRANSPIRATION = {
    "name": "evaporation_from_vegetation_transpiration",
    "data_files": [
        str(
            DATA_DIR
            / "evaporation_and_runoff"
            / "evaporation_from_vegetation_transpiration.nc"
        )
    ],
    "output_dir": "output/evaporation_from_vegetation_transpiration",
    # 植被蒸腾量，单位: mm (原始数据为 m，需 ×1000 转换)
    # 负值=蒸发，正值=凝结
    # 数据范围: -5 ~ 5 mm
    "gradient": [
        (-5, "#8c510a"),
        (-2.5, "#d8b365"),
        (-0.5, "#f6e8c3"),
        (-0.00001, "#00000000"),
        (0.00001, "#00000000"),
        (2, "#c7eae5"),
        (5, "#35978f"),
    ],
}

TOTAL_EVAPORATION = {
    "name": "total_evaporation",
    "data_files": [str(DATA_DIR / "evaporation_and_runoff" / "total_evaporation.nc")],
    "output_dir": "output/total_evaporation",
    # 总蒸发量，单位: mm (原始数据为 m，需 ×1000 转换)
    # 负值=蒸发，正值=凝结
    # 数据范围: -10.5 ~ 1.8 mm
    "gradient": [
        (-10, "#5D3A1A"),
        (-5, "#8c510a"),
        (-1, "#d8b365"),
        (-0.1, "#f6e8c3"),
        (0, "#00000000"),
        (0.005, "#c7eae5"),
        (1.8, "#35978f"),
    ],
}

WIND = {
    "name": "10m_u_component_of_wind-10m_v_component_of_wind",
    "data_files": [
        str(
            DATA_DIR
            / "raw_met_data"
            / "10m_u_component_of_wind 10m_v_component_of_wind.nc"
        )
    ],
    "output_dir": "output/wind",
    # 风场数据，输出为 JSON 格式
    # u: 东西风分量 (m/s)，v: 南北风分量 (m/s)
}

WIND_STREAMLINES = {
    "name": "wind_streamlines",
    "data_files": [
        str(
            DATA_DIR
            / "raw_met_data"
            / "10m_u_component_of_wind 10m_v_component_of_wind.nc"
        )
    ],
    "output_dir": "output/wind_streamlines",
    "line_color": (0 / 255, 255 / 255, 255 / 255),
    "density": 6,
    "line_width": 1.5,
    "maxlength": 1.0,
}

LATENT_HEAT_FLUX = {
    "name": "surface_latent_heat_flux",
    "data_files": [
        str(DATA_DIR / "radiation_and_heat" / "surface_latent_heat_flux.nc")
    ],
    "output_dir": "output/surface_latent_heat_flux",
    # 表面潜热通量，单位: J/m² (每小时间隔的总能量)
    # 负值=从地表释放，正值=被地表吸收
    # 数据范围: -5500000 ~ 20000 J/m²
    "gradient": [
        (-5500000, "#8c510a"),
        (-400000, "#d8b365"),
        (-50000, "#f6e8c3"),
        (0, "#00000000"),
        (20000, "#35978f"),
    ],
}

NET_SOLAR_RADIATION = {
    "name": "surface_net_solar_radiation",
    "data_files": [
        str(DATA_DIR / "radiation_and_heat" / "surface_net_solar_radiation.nc")
    ],
    "output_dir": "output/surface_net_solar_radiation",
    # 表面净短波辐射，单位: J/m² (每小时间隔的总能量)
    # 数据范围: 0 ~ 22000000 J/m² (正值=入射，0=夜间/无辐射)
    "gradient": [
        (0, "#00000000"),
        (5000000, "#F6E8C3"),
        (10000000, "#E8DC19"),
        (15000000, "#EAB939"),
        (22000000, "#721638"),
    ],
}

SENSIBLE_HEAT_FLUX = {
    "name": "surface_sensible_heat_flux",
    "data_files": [
        str(DATA_DIR / "radiation_and_heat" / "surface_sensible_heat_flux.nc")
    ],
    "output_dir": "output/surface_sensible_heat_flux",
    # 表面感热通量，单位: J/m² (每小时间隔的总能量)
    # 负值=从地表释放到大气，正值=被地表吸收
    # 数据范围: -13000000 ~ 500000 J/m²
    "gradient": [
        (-13000000, "#8c510a"),
        (-4000000, "#d8b365"),
        (-50000, "#f6e8c3"),
        (0, "#00000000"),
        (500000, "#35978f"),
    ],
}

SOIL_TYPE = {
    "name": "soil_type",
    "data_files": [str(DATA_DIR / "invariant_data" / "soil_type.nc")],
    "output_dir": "output/soil_type",
    "discrete": True,
    # 土壤质地类型，单位: 分类 ID (无量纲)
    # FAO 土壤质地分类: 0=无数据/水体, 1=砂土, 2=壤土, 3=中细, 4=粘土, 6=有机土
    # ECMWF IFS Soil Type (FAO soil texture): 0=No data/Water, 1=Coarse(sand),
    # 2=Medium(loam), 3=Medium-fine, 4=Fine(clay), 6=Organic
    "gradient": [
        (0, "#00000000"),  # 水体 (透明)
        (1, "#F5DEB3"),  # 砂土 - 粗质、保水性低
        (2, "#C8A96E"),  # 壤土 - 中质、最主要类型
        (3, "#A0785A"),  # 中细 - 赭棕、中国广泛分布
        (4, "#7B3F00"),  # 粘土 - 细质、保水性高
        (6, "#4A5C2F"),  # 有机土 - 高持水量
    ],
}

HIGH_VEGETATION_TYPE = {
    "name": "high_vegetation_type",
    "data_files": [str(DATA_DIR / "invariant_data" / "type_of_high_vegetation.nc")],
    "output_dir": "output/type_of_high_vegetation",
    "discrete": True,
    # 高植被类型，单位: GRIB Code table 4.234 (无量纲)
    # 3=常绿针叶, 4=落叶针叶, 5=落叶阔叶, 6=常绿阔叶, 18=混交林, 19=间断森林
    "gradient": [
        (0, "#00000000"),  # 无高植被 (透明)
        (3, "#228B22"),  # 常绿针叶树 - 深绿
        (4, "#90EE90"),  # 落叶针叶树 - 浅绿
        (5, "#D2691E"),  # 落叶阔叶树 - 橙棕
        (6, "#006400"),  # 常绿阔叶树 - 暗绿
        (18, "#6B8E23"),  # 混交林/林地 - 草绿
        (19, "#9ACD32"),  # 间断森林 - 黄绿
    ],
}

LOW_VEGETATION_TYPE = {
    "name": "low_vegetation_type",
    "data_files": [str(DATA_DIR / "invariant_data" / "type_of_low_vegetation.nc")],
    "output_dir": "output/type_of_low_vegetation",
    "discrete": True,
    # 低植被类型，单位: GRIB Code table 4.234 (无量纲)
    # 0=无植被, 1=农田, 2=草地, 7=高草, 9=苔原, 10=灌溉农田, 11=半荒漠, 13=沼泽, 16=常绿灌木, 17=落叶灌木
    # ECMWF GRIB Code table 4.234 - Low Vegetation (tvl):
    # 0=No vegetation, 1=Crops, 2=Grass, 7=Tall grass, 9=Tundra,
    # 10=Irrigated crops, 11=Semidesert, 13=Bogs, 16=Evergreen shrubs,
    # 17=Deciduous shrubs, 20=Water and land mixtures
    "gradient": [
        (0, "#00000000"),  # 无植被 (透明)
        (1, "#FFD700"),  # 农田/混合农业 - 黄色
        (2, "#90EE90"),  # 草地 - 浅绿
        (7, "#8B4513"),  # 高草 - 棕褐
        (9, "#8B7355"),  # 苔原 - 暗棕
        (10, "#DAA520"),  # 灌溉农田 - 金黄
        (11, "#F4A460"),  # 半荒漠 - 沙色
        (13, "#006666"),  # 沼泽/湿地 - 深蓝绿
        (16, "#355E3B"),  # 常绿灌木 - 暗绿
        (17, "#CC5500"),  # 落叶灌木 - 橙褐
        (20, "#4682B4"),  # 水陆混合 - 蓝灰
    ],
}

LAI_LOW_VEGETATION = {
    "name": "leaf_area_index_low_vegetation",
    "data_files": [
        str(DATA_DIR / "vegetation_data" / "leaf_area_index_low_vegetation.nc")
    ],
    "output_dir": "output/leaf_area_index_low_vegetation",
    # 低植被叶面积指数，单位: m²/m² (无量纲)
    # 表示单位面积上叶片单面面积，数据范围: 0 ~ 4
    "gradient": [
        (0.0, "#00000000"),
        (0.5, "#90EE90"),
        (1.0, "#32CD32"),
        (2.0, "#228B22"),
        (3.0, "#006400"),
        (4.0, "#004000"),
    ],
}

LAI_HIGH_VEGETATION = {
    "name": "leaf_area_index_high_vegetation",
    "data_files": [
        str(DATA_DIR / "vegetation_data" / "leaf_area_index_high_vegetation.nc")
    ],
    "output_dir": "output/leaf_area_index_high_vegetation",
    # 高植被叶面积指数，单位: m²/m² (无量纲)
    # 表示单位面积上叶片单面面积，数据范围: 0 ~ 6
    "gradient": [
        (0.0, "#00000000"),
        (0.5, "#90EE90"),
        (1.5, "#228B22"),
        (3.0, "#006400"),
        (4.5, "#004000"),
        (6.0, "#002800"),
    ],
}

TOTAL_PRECIPITATION = {
    "name": "total_precipitation",
    "data_files": [str(DATA_DIR / "raw_met_data" / "total_precipitation.nc")],
    "output_dir": "output/total_precipitation",
    # 总降水量，单位: mm (原始数据为 m，需 ×1000 转换)
    # 数据范围: 0 ~ 10 mm (基于 P99 分布)
    "gradient": [
        (0.0, "#00000000"),
        (0.1, "#C8E3F5"),
        (1.0, "#75B4F0"),
        (5.0, "#2E6AB3"),
        (10.0, "#1A3A6B"),
    ],
}

SOIL_MOISTURE = {
    "name": "volumetric_soil_water_layer_1",
    "data_files": [str(DATA_DIR / "raw_met_data" / "volumetric_soil_water_layer_1.nc")],
    "output_dir": "output/volumetric_soil_water_layer_1",
    # 土壤体积含水量 (0-7cm)，单位: m³/m³ 或 % (无单位)
    # 数据范围: 0 ~ 0.5 m³/m³
    "gradient": [
        (0.00, "#F5F5F5"),
        (0.05, "#E0F2FE"),
        (0.10, "#BAE6FD"),
        (0.15, "#7DD3FC"),
        (0.20, "#38BDF8"),
        (0.25, "#0EA5E9"),
        (0.30, "#0284C7"),
        (0.35, "#0369A1"),
        (0.40, "#075985"),
        (0.45, "#0C4A6E"),
        (0.50, "#082F49"),
    ],
}

SOIL_TEMPERATURE_LEVEL_1 = {
    "name": "soil_temperature_level_1",
    "data_files": [str(DATA_DIR / "raw_met_data" / "soil_temperature_level_1.nc")],
    "output_dir": "output/soil_temperature_level_1",
    # 土壤温度 (表层)，单位: °C (原始数据为 K，需 -273.15 转换)
    # 数据范围: -15 ~ 30°C
    "gradient": [
        (-15, "#2B2D6B"),
        (-5, "#3D82D4"),
        (5, "#C8DDF6"),
        (15, "#EDE787"),
        (25, "#E8DC19"),
        (30, "#E15E5D"),
    ],
}

SNOW_DEPTH = {
    "name": "snow_depth",
    "data_files": [str(DATA_DIR / "raw_met_data" / "snow_depth.nc")],
    "output_dir": "output/snow_depth",
    # 雪深，单位: cm (原始数据为 m，需 ×100 转换)
    # 数据范围: 0 ~ 200 cm
    "gradient": [
        (0, "#00000000"),
        (1, "#96CCF6AB"),
        (5, "#3280BEE8"),
        (10, "#2E57BA"),
        (15, "#5450B3"),
        (20, "#3C359C"),
        (25, "#2E2270"),
        (30, "#1A0D64"),
        (40, "#910991"),
        (50, "#B400B4"),
        (60, "#D200D2"),
        (80, "#C67FC6"),
        (100, "#E3D0E3"),
        (150, "#EBEEEE"),
        (200, "#FFFFFF"),
    ],
}

ALL_CONFIGS = {
    "pm10": PM10,
    "t2m": T2M,
    "potential_evaporation": POTENTIAL_EVAPORATION,
    "evaporation_canopy": EVAPORATION_CANOPY,
    "vegetation_transpiration": VEGETATION_TRANSPIRATION,
    "total_evaporation": TOTAL_EVAPORATION,
    "wind": WIND,
    "wind_streamlines": WIND_STREAMLINES,
    "latent_heat_flux": LATENT_HEAT_FLUX,
    "net_solar_radiation": NET_SOLAR_RADIATION,
    "sensible_heat_flux": SENSIBLE_HEAT_FLUX,
    "soil_type": SOIL_TYPE,
    "high_vegetation_type": HIGH_VEGETATION_TYPE,
    "low_vegetation_type": LOW_VEGETATION_TYPE,
    "lai_low_vegetation": LAI_LOW_VEGETATION,
    "lai_high_vegetation": LAI_HIGH_VEGETATION,
    "total_precipitation": TOTAL_PRECIPITATION,
    "volumetric_soil_water_layer_1": SOIL_MOISTURE,
    "soil_temperature_level_1": SOIL_TEMPERATURE_LEVEL_1,
    "snow_depth": SNOW_DEPTH,
}
