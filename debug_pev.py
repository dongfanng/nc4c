import xarray as xr
import numpy as np

ds = xr.open_dataset('e:/GitCodeLibrary/nc4c/data/evaporation_and_runoff/potential_evaporation.nc')
pev = ds['pev']

print(f'Variable: pev')
print(f'Units attribute: {pev.attrs.get("units")}')
print(f'GRIB_units: {pev.attrs.get("GRIB_units")}')
print(f'Long name: {pev.attrs.get("long_name")}')
print()
print(f'Raw data range:')
print(f'  Min: {float(pev.min())} ({pev.attrs.get("units")})')
print(f'  Max: {float(pev.max())} ({pev.attrs.get("units")})')
print()
print(f'After m -> mm conversion (*1000):')
print(f'  Min: {float(pev.min()) * 1000} mm')
print(f'  Max: {float(pev.max()) * 1000} mm')
print()

# Check if negative values make sense (condensation?)
print('Sample of negative values:')
neg_count = (pev.values < 0).sum()
total_count = pev.size
print(f'Negative values count: {neg_count} / {total_count} ({100*neg_count/total_count:.1f}%)')