'''
Purpose: Model the change in revenue assoicated with transitions to residential solar
User Inputs: Time horizon, solar growth rate, location, number of houses
    initial percent of houses that have solar installations, and the surface area of a residential roof
Modified: April 19, 2021 by NAR
'''
from solarModel import Region, ssa_to_solar_pen
import csv
import sys
import pandas as pd

#
# Simulation Functions
#


def annual_penetration(initial_ssa, final_ssa, time_horizon):
    """
    Generate a list containing the solar penetration for every year in the time horizon
    :param initial_ssa: Starting solar set aside percentage
    :param final_ssa: Final solar set aside percentage
    :param time_horizon: Length of time for evaluation
    :return pen_list: List containing annual solar penetrations
    """
    # Convert solar set asides to penetrations
    initial_pen = ssa_to_solar_pen(initial_ssa)
    final_pen = ssa_to_solar_pen(final_ssa)

    # Create list of target penetration rates
    pen_list = list()
    for year in range(time_horizon + 1):
        current_pen = ((final_pen - initial_pen) / time_horizon) * year + initial_pen
        pen_list.append(current_pen)

    return pen_list


def simulation_data(loc, pen_list):
    """
    Generate a pandas dataframe containing relevant time-series data for the simulation
    :param pen_list:
    :return time_data: Pandas dataframe containing the profit, number of total houses,
        number of solar houses, energy demand, and energy price for every year simulated
    """
    # Create lists to hold dataframe columns
    profits = list()
    years = list()
    houses = list()
    solar_houses = list()
    demand = list()
    prices = list()

    # Use the model to populate the columns
    year = 0
    for solar_pen in pen_list:

        # Append year and increment
        years.append(year)
        year += 1

        # Create region
        region = Region(loc, solar_pen)

        # Append profit
        now_profit = region.annual_profit
        profits.append(now_profit)

        # Append number of houses
        now_houses = region.num_houses
        houses.append(now_houses)

        # Append number of solar houses
        solar_houses.append(now_houses * solar_pen)

        # Append demand
        now_demand = region.annual_demand
        demand.append(now_demand)

        # Append utility price
        price = region.utility_price
        prices.append(price)

    # Create dataframe for simulation
    data = {'year': years,
            'profit': profits,
            'number_houses': houses,
            'solar_houses': solar_houses,
            'demand': demand,
            'price': prices}
    time_data = pd.DataFrame(data)

    return time_data


def calculate_impact(time_data):
    """
    Calculate the expected total cost since year 0 for three cost recovery mechanisms: raising fixed
        costs for all customers, raising fixed costs for solar customers, raising variable costs for
        all customers
    :param time_data: Pandas dataframe containing relevant time-series data for simulation
    :return: time_data updated to include calculated costs
    """
    # Calculate the lost profit since year 0
    time_data['profit_loss'] = time_data['profit'].iloc[0] - time_data['profit']

    # Calculate the fixed cost increase (compared to year 0) if applied to all houses
    time_data['fixed_increase_all_houses'] = time_data['profit_loss'] / time_data['number_houses']

    # Calculate the fixed cost increase (compared to year 0) if applied to only solar houses
    time_data['fixed_increase_solar_houses'] = time_data['profit_loss'] / time_data['solar_houses']

    # Calculate the variable cost increase (compared to year 0) if applied to all houses
    time_data['variable_increase'] = time_data['profit_loss'] / time_data['demand']
    time_data['variable_increase'] = time_data['variable_increase'] / time_data['price']

    return time_data


def print_csv(time_data):
    """
    Print the projects cost increases to a csv file for visualization and further evaluation
    :param time_data: Pandas dataframe containing relevant time-series data for simulation
    :return None:
    """
    # Print the year and associated cost increases to csv file
    with open('results.csv', mode='w+') as simulation_data:
        simulation_writer = csv.writer(simulation_data, delimiter=',')
        simulation_writer.writerow(time_data['year'].tolist())
        simulation_writer.writerow(time_data['fixed_increase_all_houses'].tolist())
        simulation_writer.writerow(time_data['fixed_increase_solar_houses'].tolist())
        simulation_writer.writerow(time_data['variable_increase'].tolist())


#
# Simulation Main Code
#

# Read in arguments
ssa_i = float(sys.argv[1])
ssa_t = float(sys.argv[2])
time_horizon = int(sys.argv[3])
lat = float(sys.argv[4])
lon = float(sys.argv[5])
loc = lat, lon

# Create list of annual targeted penetration rates
pen_list = annual_penetration(ssa_i, ssa_t, time_horizon)

# Create a dataframe for the simulation
time_data = simulation_data(loc, pen_list)

# Calculate impacts on consumers and add impacts to dataframe
time_data = calculate_impact(time_data)

# Print annual cost increases (when compared to year 0 costs) to csv file for visualization
print_csv(time_data)
