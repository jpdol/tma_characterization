#########################################################################################
# File: get_asma_data.R
# Description: Implement and use a collect function for download ASMA data from ICEA API
# Author: Jean P. O. Lima
#########################################################################################

library(httr)
library(jsonlite)

# Function to query the API and save the CSV
query_api <- function(idate, fdate, c, groupby = "flight", airport = "SBGR") {
  # Build the API URL with the provided parameters
  base_url <- "http://montreal.icea.decea.mil.br:5001/api/v1/kpi/08"
  token <- "251838ea1b8ed3e289504e4490b05a050d084b0d"
  url <- paste0(base_url, 
                "?token=", token, 
                "&groupby=", groupby, 
                "&airport=", airport, 
                "&idate=", idate, 
                "&fdate=", fdate, 
                "&c=", c)
  
  # Make the GET request
  response <- GET(url)
  
  # Check if the request was successful
  if (status_code(response) == 200) {
    # Parse the JSON content from the response into a data frame
    data <- content(response, as = "text", encoding = "UTF-8")
    data_df <- fromJSON(data, flatten = TRUE)
    
    # Save the data frame into a CSV file
    file_name <- paste0("raw_data/ASMA_", airport, "_C", c, "_", groupby, ".csv")
    write.csv(data_df, file_name, row.names = FALSE)
    
    cat("The data has been saved to '", file_name, "'.\n", sep = "")
  } else {
    cat("Error accessing the API. Status code:", status_code(response), "\n")
  }
}

# Call the function for both scenarios
query_api("2024-01-01", "2024-02-01", 100)
query_api("2024-01-01", "2024-02-01", 40)

