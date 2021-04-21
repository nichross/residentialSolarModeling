# Residential Solar Modeling - A General Framework

## Objective

Model the impact on electricity prices of residential solar adoption 

## Methodology

The program takes as inputs the initial and target solar set-asides from the user over a specified time horizon. A solar set-aside is the percent 
of energy consumption that must come from local solar generation. The program then outputs a csv file containing and costs to consumers associated with three
different strageties to mitigate the losses to energy suppliers associated with residentiar solar adoption:
1) Increasing the fixed costs for all customers
2) Increasing the fixed costs for solar customers
3) Increasing the variable costs for all customers

### Inputs
* Initial SSA: Float specifying the starting solar set-aside
* Target SSA: Float specifying the solar set-aside targeted at the end of the time horizon
* Time Horizon: Integer specifying the number of years between the initial and target SSA
* Latitude: Float specifying the latitude of the closest TMY3 weather station to the region of interest
* Longitude: Float specifying the longitude of the closest TMY3 weather station to the region of interest

### Outputs
* Results: CSV containing each year in the time horizon and the cost per impacted customer associated with stargety 1, 2, and 3 for that year

## Program Execution


Before execution the program:

The following 3 data files need to updated and saved in the working directory for the region of interet:
1) Census Data: A csv file containing the city name, year, and number of households for multiple regions. The csv file should be updated to include the 2019 household data for the
  region then saved in the working directory. The dictionary in the get_num_houses() method should be updated to map the TYM3 station coordinates to the city name for the region.
  Census data can be found [here](https://www.census.gov/quickfacts/fact/table/US/PST045219)
2) Wholesale Energy Data: A csv file containing 2019 wholesale energy prices for various suppliers. The file should be saved in the working directory. The dictionary in the 
  get_wholesale_prices() method should be updated to map the TYM3 station coordinates to the supplier for the region of interest.
  Wholesale energy prices for other years can be found [here](https://www.eia.gov/electricity/wholesale/)
3) Utility Price Data: A csv file containing the coordinates and relevant utility data for multiple regions. The csv file should be updated to include utility price data for the
  region of interest then saved in the working directory.
  Utility price data can be found [here](https://openei.org/apps/USURDB/)

The following 2 data files need to be downloaded and saved in the working directory for the region of interet:
1) Energy Usage Data: The csv file associated with the TYM3 station closest to the region of interest should be downloaded and saved in the working directory. 
  The dictionary in the get_usage_data() method should be updated to map the TYM3 station coordinates to the data file name
  Usage data can be found [here](https://openei.org/datasets/dataset/commercial-and-residential-hourly-load-profiles-for-all-tmy3-locations-in-the-united-states)
2) Residential Solar Production Data: A csv file containing the hourly energy production of a solar equipped house as calculated by the NREL System Advisor Model (PySam).
  NREL instructions for using PySam can be found [here](https://github.com/NREL/pysam)

The data files listed above, updated for a Pittsburgh simulation, can be found in data_file section in this repository


To execute the program save sim.py and solarModel.py in the working directory and run the following command:
python3 sim.py initial_ssa target_ssa time_horizon latitude longitude

An example of a command for a Pittsburgh simulation is shown below:
python3 sim.py 0.005 0.2 6 40.5 -80.233


For testing purposes the get_num_houses() method is set to return 100. Once the updated program has been tested the get_num_houses() method should be set to return num_houses
