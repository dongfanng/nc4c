"""配置模块"""

from pathlib import Path

DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"

LON_RANGE = (73.0, 135.0)
LAT_RANGE = (33.0, 53.0)

PM10 = {
    "name": "pm10",
    "data_files": [str(p) for p in sorted((DATA_DIR / "pm10_data").glob("*.nc"))],
    "output_dir": "output/pm10",
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
    "gradient": [
        (-6, "#8c510a"),
        (-2, "#d8b365"),
        (-0.1, "#f6e8c3"),
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
    "output_dir": "output/evaporation_canopy",
    "gradient": [
        (-0.5, "#8c510a"),
        (-0.1, "#d8b365"),
        (-0.001, "#f6e8c3"),
        (0, "#00000000"),
        (0.001, "#c7eae5"),
        (0.01, "#35978f"),
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
    "output_dir": "output/vegetation_transpiration",
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
    "gradient": [
        (-1.5, "#8c510a"),
        (-0.3, "#d8b365"),
        (-0.01, "#f6e8c3"),
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
}

LATENT_HEAT_FLUX = {
    "name": "surface_latent_heat_flux",
    "data_files": [
        str(DATA_DIR / "radiation_and_heat" / "surface_latent_heat_flux.nc")
    ],
    "output_dir": "output/surface_latent_heat_flux",
    "gradient": [
        (-5500000, "#8c510a"),
        (-400000, "#d8b365"),
        (-50000, "#f6e8c3"),
        (0, "#00000000"),
        (20000, "#35978f"),
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
    "latent_heat_flux": LATENT_HEAT_FLUX,
}
