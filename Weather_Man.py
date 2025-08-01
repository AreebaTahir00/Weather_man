import csv
from datetime import datetime
import os

RED = '\x1b[31m'  # Red Color
BLUE = '\x1b[34m' # Blue Color
RESET = '\x1b[0m' # Reset 

# This function helps to draw a horizontal bar chart
def draw_temperature_chart(file_path):
    if not os.path.exists(file_path):   # Check file path exists or not  
        print("File not found.")
        return

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)   # Read complete file
        reader.fieldnames = [name.strip() for name in reader.fieldnames]   # Make separate fields

        chart_data = []

        for row in reader:
            try:
                date_str = row.get('GST', '').strip()
                max_temp = row.get('Max TemperatureC', '').strip()   # Extract Max temperature Column
                min_temp = row.get('Min TemperatureC', '').strip()   # Extract Min temperature Column
                
                """Processes a row of weather data by checking if the date, max temperature, 
                and min temperature are present. If valid, it:
                - Parses the date from string format.
                - Extracts the day and month-year for labeling.
                - Converts temperature values to integers.
                - Appends a tuple (day, max_temp, min_temp, month_year) to the chart data list for later use in drawing the temperature bar chart.

                This ensures that only valid and complete entries are visualized."""

                if date_str and max_temp and min_temp:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    day = date.strftime("%d")
                    month_year = date.strftime("%B %Y")
                    max_temp = int(max_temp)
                    min_temp = int(min_temp)

                    chart_data.append((day, max_temp, min_temp, month_year))
            except:
                continue

    if not chart_data:
        print("No valid data to display.")
        return

    print(chart_data[0][3])  # e.g., "March 2005"
    print(f"{RED}High Temperature")
    print(f"{BLUE}Low Temperature\n")
    
    # Make a horizontal bar chart of highest and lowest temperature
    for day, max_t, min_t, _ in chart_data:
        print(f"{day} {RED}{'+' * max_t}{RESET} {max_t}C")
        print(f"{day} {BLUE}{'+' * min_t}{RESET} {min_t}C")



# This function helps to get max and min temperature from one file
def get_monthly_temp(file_path):
    max_temp = float('-inf')  # Give the negative infinity
    min_temp = float('inf')   # Give the positive infinity
    max_day = ""
    min_day = ""

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            """ Attempts to parse weather data from a row. Specifically:
            - Converts the 'GST' column to a datetime object.
            - Converts 'Max TemperatureC' and 'Min TemperatureC' to integers.
            - Updates the maximum and minimum temperatures found so far, along with
              their corresponding dates, if the current values are more extreme.

            Skips the row if any of the required fields are missing or invalid. """

            try:
                date = datetime.strptime(row['GST'], "%Y-%m-%d")
                max_t = int(row['Max TemperatureC'])
                min_t = int(row['Min TemperatureC'])

                if max_t > max_temp:
                    max_temp = max_t
                    max_day = date.strftime("%B %d")

                if min_t < min_temp:
                    min_temp = min_t
                    min_day = date.strftime("%B %d")
            except:
                continue

    return max_temp, max_day, min_temp, min_day


# This functions helps to find the average of high temperature, low temperature and humidity
def get_monthly_averages(file_path):
    max_temps = []
    min_temps = []
    humidities = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        # Strip any leading/trailing spaces from column names
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            try:
                # Ensure values exist before converting to int
                max_temp = row.get('Max TemperatureC', '').strip()
                min_temp = row.get('Min TemperatureC', '').strip()
                mean_humidity = row.get('Mean Humidity', '').strip()

                # If values exist then simply append the data in the original list
                if max_temp and min_temp and mean_humidity:
                    max_temps.append(int(max_temp))
                    min_temps.append(int(min_temp))
                    humidities.append(int(mean_humidity))
            except Exception as e:
                print(f"Skipping row due to error: {e}")
                continue

    if not max_temps or not min_temps or not humidities:
        return None, None, None
    
    # Computing the averages
    avg_max = round(sum(max_temps) / len(max_temps))
    avg_min = round(sum(min_temps) / len(min_temps))
    avg_hum = round(sum(humidities) / len(humidities))

    return avg_max, avg_min, avg_hum

# This function helps to compare all months and return final yearly result
def compare_yearly_temperatures(folder, year):
    yearly_max = float('-inf')
    yearly_min = float('inf')
    yearly_max_day = ""
    yearly_min_day = ""
    i=0
    
    for filename in os.listdir(folder):
        i=i+1          # For date in output and increasing one by one
        if filename.endswith('.txt') and year in filename:   # Checks filename ends with .txt and year is same or not
            file_path = os.path.join(folder, filename)       # Join the folder and file name to make a file path
            if i==1:
                draw_temperature_chart(file_path)            # This function is for drawing the horizontal bar chart
                print(f"\n\n -------- DAY WISE TEMPERATURE LIST---------")

            avg_max, avg_min, avg_hum = get_monthly_averages(file_path)              # This function is for getting the averages of max temp, min temp and humidity
            max_temp, max_day, min_temp, min_day = get_monthly_temp(file_path)       # This function is for getting the hightest and lowest temperature of the year

            if max_temp > yearly_max:   # Comparing hightest temperature
                yearly_max = max_temp
                yearly_max_day = max_day

            if min_temp < yearly_min:   # Comparing lowest temperature
                yearly_min = min_temp
                yearly_min_day = min_day

            if avg_max is not None:
                print (f"\n------------------------------")
                print(f"___2005-4-{i}____")
                print(f"Highest Average Temperature: {avg_max}C")
                print(f"Lowest Average Temperature: {avg_min}C")
                print(f"Average Humidity: {avg_hum}%")
              
            else:
                print("No valid data found.")

    return yearly_max, yearly_max_day, yearly_min, yearly_min_day


def main():
    folder = 'F:/04162313024 Areeba Tahir-Study/Python/Weather man/Dubai_weather'
    year = '2004'

    print("\n--- Dubai ---")

    high, high_day, low, low_day = compare_yearly_temperatures(folder, year)    #This function is for comparing yearly temperature
    print("\n\n ------------YEARLY DATA------------")
    print(f"Highest: {high}C on {high_day}")
    print(f"Lowest: {low}C on {low_day}")
    print(f"----------------------------------------")


# Run the program only if this script is executed directly
if __name__ == "__main__":
   main()