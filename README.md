# Extract-data-from-Netcdf-files-to-shapefile-using-R
This repository contains an R script for extracting precipitation data from NetCDF files using a grid shapefile.  
It is designed to process **decadal rainfall datasets**, extract values at grid centroids, append temporal (dekad) identifiers, and export the results to CSV for further analysis.

---

## 📌 Features
- Reads and processes multiple NetCDF files (`ncdf4`, `raster`)
- Uses shapefile grids to spatially extract precipitation values (`sf`)
- Calculates dekadal periods from file naming conventions (`stringr`)
- Handles CRS transformations to align grid and raster data
- Outputs clean CSV with:
  - Longitude
  - Latitude
  - Precipitation values
  - Dekad identifiers
  - Original filename reference

---

## 🛠 Requirements
Ensure you have the following R packages installed:
```r
install.packages(c("ncdf4", "raster", "sf", "dplyr", "stringr"))
````

---

## 📂 Input Data

1. **NetCDF files** — Precipitation datasets named with start and end days in the format:

   ```
   some_prefix_days_<start_day>_to_<end_day>.nc
   ```
2. **Grid shapefile** — Defines the extraction points (centroids) for precipitation values.

---

## 🚀 Usage

1. Update the file paths in the script:

   ```r
   input_dir <- "path/to/netcdf/files"
   grid_shapefile <- "path/to/grid_shapefile.shp"
   output_csv <- "path/to/output.csv"
   ```
2. Run the R script.
3. The output CSV will contain precipitation values for each grid cell and dekad.

---

## 📊 Output Example

| longitude | latitude | precip | filename                  | dekad |
| --------- | -------- | ------ | ------------------------- | ----- |
| 34.112345 | 0.112345 | 5.43   | prec\_days\_1\_to\_10.nc  | D1    |
| 34.223456 | 0.223456 | 12.87  | prec\_days\_11\_to\_20.nc | D2    |

---

## 🌍 Intended Use

Ideal for:

* Hydrological modeling
* Climate change studies
* Meteorological analysis
* Agriculture-related rainfall monitoring

---

## 📜 License

This project is released under the **MIT License** – feel free to modify and adapt.

---


