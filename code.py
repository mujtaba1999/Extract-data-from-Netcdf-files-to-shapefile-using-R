# Load required libraries
library(ncdf4)         # For reading NetCDF files
library(raster)        # For raster manipulation
library(sf)            # For handling spatial data
library(dplyr)         # For data manipulation
library(stringr)       # For string manipulation

# Set the directory containing the NetCDF files
# Set the directory containing the NetCDF files
input_dir <- "C:/Users/mujta/Documents/Intrenship/Prec/decadal_rf_cdd/2009"
#output_csv <- "precipitation_grid_data_with_dekad.csv"
grid_shapefile <- "C:/Users/mujta/Documents/DATABANK/Kenya/Shp/Busia_fishnet_300m_clip.shp"  # Path to your grid shapefile

# Load the grid shapefile using sf
grid <- st_read(grid_shapefile)

# Ensure the grid is valid
grid <- st_make_valid(grid)

# Extract centroids from polygons
centroids <- st_centroid(grid)

# Initialize an empty data frame to store the results
results <- data.frame()

# List all NetCDF files in the directory
nc_files <- list.files(input_dir, pattern = "\\.nc$", full.names = TRUE)

# Loop through each NetCDF file
for (file in nc_files) {
  # Extract dekad information from the filename
  filename <- basename(file)
  dekad_match <- str_match(filename, "_days_(\\d+)_to_(\\d+)")[, 2:3]
  start_day <- as.numeric(dekad_match[1])
  end_day <- as.numeric(dekad_match[2])
  
  # Calculate the dekad based on start_day
  dekad <- paste0("D", (start_day %/% 10) + 1)
  
  # Open the NetCDF file
  nc_data <- nc_open(file)
  
  # Extract precipitation variable (replace 'precip' with the actual variable name)
  var_name <- "precip"
  if (!(var_name %in% names(nc_data$var))) {
    stop(paste("Variable", var_name, "not found in file:", file))
  }
  
  # Read precipitation data
  precip <- raster(file, varname = var_name)
  
  # Check and reproject centroids to match raster CRS
  raster_crs <- crs(precip)
  if (!st_crs(centroids) == raster_crs) {
    centroids <- st_transform(centroids, crs = raster_crs)
  }
  
  # Extract precipitation values for the centroids
  extracted_values <- extract(precip, as(centroids, "Spatial"), df = TRUE)
  
  # Add longitude, latitude, precipitation values, and dekad to the results
  centroids_coords <- as.data.frame(st_coordinates(centroids))
  extracted_data <- cbind(centroids_coords, extracted_values)
  colnames(extracted_data)[1:2] <- c("longitude", "latitude")
  extracted_data$filename <- filename
  extracted_data$dekad <- dekad
  
  # Combine with previous results
  results <- bind_rows(results, extracted_data)
  
  # Close the NetCDF file
  nc_close(nc_data)
}
output_csv <- "C:/Users/mujta/Documents/Intrenship/Prec/decadal_rf_cdd/2009/cdd_grid_2009.csv"
# Write the results to a CSV file
write.csv(results, output_csv, row.names = FALSE)
cat("Precipitation data with dekad information saved to", output_csv, "\n")
