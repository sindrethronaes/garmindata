import datetime
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from resting_heart_rate_original import filter_weights
import seaborn as sns

def filter_heart_rates(filename):
    heart_rates = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(', ')
        if len(parts) < 2:
            continue
        date_part = parts[0].split(': ')
        date_str = date_part[1].strip()
        heart_rate_part = parts[1].split(': ')
        heart_rate_value = heart_rate_part[1].strip()
        if heart_rate_value == "None":
            # Find the average value of the previous 30 days and the next 30 days
            start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d') - datetime.timedelta(days=30)
            end_date = datetime.datetime.strptime(date_str, '%Y-%m-%d') + datetime.timedelta(days=30)
            prev_30_days = [hr for hr in heart_rates if hr['date'] >= start_date and hr['date'] < datetime.datetime.strptime(date_str, '%Y-%m-%d')]
            avg_heart_rate = sum(hr['heart_rate'] for hr in prev_30_days) / (len(prev_30_days))
            heart_rates.append({'date': datetime.datetime.strptime(date_str, '%Y-%m-%d'), 'heart_rate': avg_heart_rate})
        else:
            heart_rates.append({'date': datetime.datetime.strptime(date_str, '%Y-%m-%d'), 'heart_rate': float(heart_rate_value)})
    return heart_rates

def plot_heart_rates(heart_rates_1):
    dates_1 = [d['date'] for d in heart_rates_1]
    heart_rates_1 = [d['heart_rate'] for d in heart_rates_1]
    df= pd.DataFrame(heart_rates_1, index=dates_1, columns=['Heart Rate 1'])
    df.plot(kind='line', color=['blue'])
    plt.xlabel('Date')
    plt.ylabel('Heart Rate')
    plt.title('Heart Rate Trend')
    plt.grid(True)
    plt.show()

def calculate_trend(heart_rates):
    dates = [d['date'] for d in heart_rates]
    heart_rates_array = np.array([d['heart_rate'] for d in heart_rates])
    
    # Fit a polynomial of degree 1 (linear) to the data
    trend = np.polyfit(range(len(heart_rates_array)), heart_rates_array, 1)
    
    # Calculate the average heart rate
    average = np.mean(heart_rates_array)
    
    # Create a dataframe for plotting
    df = pd.DataFrame(heart_rates_array, index=dates, columns=['Heart Rate'])
    
    # Plot the original data and the trend line
    plt.figure(figsize=(12, 6))
    df.plot(kind='line', color=['blue'])
    plt.plot(dates, trend[0] * np.arange(len(heart_rates_array)) + trend[1], color='red', label='Trend')
    plt.xlabel('Date')
    plt.ylabel('Heart Rate')
    plt.title('Heart Rate Trend')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return average, trend

def calculate_weight_trend(weights):
    dates = [d['date'] for d in weights]
    weight_array = np.array([d['weight'] for d in weights])
    
    # Fit a polynomial of degree 1 (linear) to the data
    trend = np.polyfit(range(len(weight_array)), weight_array, 1)
    
    # Calculate the average weight
    average = np.mean(weight_array)
    
    # Create a dataframe for plotting
    df = pd.DataFrame(weight_array, index=dates, columns=['Weight'])
    
    # Plot the original data and the trend line
    plt.figure(figsize=(12, 6))
    df.plot(kind='line', color=['blue'])
    plt.plot(dates, trend[0] * np.arange(len(weight_array)) + trend[1], color='red', label='Trend')
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.title('Weight Trend')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return average, trend

def get_dates_in_range(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    return dates

if __name__ == "__main__":
    
    filtered_heart_rates = filter_heart_rates("resting_heart_rates.txt")
    filtered_weights = filter_weights("weights.txt")

    # Plot
    #plot_heart_rates(filtered_heart_rates)
    #calculate_trend(filtered_heart_rates)
    calculate_weight_trend(filtered_weights)
    