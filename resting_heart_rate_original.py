import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from garmin_fetch import get_dates_in_range

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
            continue
        heart_rates.append({'date': datetime.datetime.strptime(date_str, '%Y-%m-%d'), 'heart_rate': float(heart_rate_value)})
    return heart_rates

def filter_weights(filename):
    weights = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(', ')
        if len(parts) < 2:
            continue
        date_part = parts[0].split(': ')
        date_str = date_part[1].strip()
        weight_part = parts[1].split(': ')
        weight_value = weight_part[1].strip()
        if weight_value == "None":
            continue
        weights.append({'date': datetime.datetime.strptime(date_str, '%Y-%m-%d'), 'weight': float(weight_value)})
    return weights

def replace_none_hrs(heart_rates, start_date, end_date):
    new_heart_rates = []
    dates_in_range = get_dates_in_range(start_date - datetime.timedelta(days=30), end_date + datetime.timedelta(days=30))
    for date in dates_in_range:
        if date in heart_rates:
            new_heart_rates.append({'date': date, 'heart_rate': heart_rates[date]['heart_rate']})
        else:
            before_date = date - datetime.timedelta(days=30)
            after_date = date + datetime.timedelta(days=30)
            before_avg = np.mean([d['heart_rate'] for d in heart_rates if d['date'] >= before_date and d['date'] <= date])
            after_avg = np.mean([d['heart_rate'] for d in heart_rates if d['date'] >= date and d['date'] <= after_date])
            new_heart_rates.append({'date': date, 'heart_rate': (before_avg + after_avg) / 2})
    return new_heart_rates

def replace_none_weights(weights, start_date, end_date):
    new_weights = []
    dates_in_range = get_dates_in_range(start_date - datetime.timedelta(days=30), end_date + datetime.timedelta(days=30))
    for date in dates_in_range:
        if any(weight['date'] == date for weight in weights):
            # If weight data exists for this date, use it directly
            for weight in weights:
                if weight['date'] == date:
                    new_weights.append({'date': date, 'weight': weight['weight']})
                    break
        else:
            # If no weight data exists for this date, calculate average from surrounding days
            before_date = date - datetime.timedelta(days=30)
            after_date = date + datetime.timedelta(days=30)
            relevant_weights = [weight['weight'] for weight in weights if before_date <= weight['date'] <= after_date]
            if relevant_weights:
                avg_weight = np.mean(relevant_weights)
                new_weights.append({'date': date, 'weight': avg_weight})
    return new_weights

def plot_heart_rates(heart_rates_1, heart_rates_2):
    dates_1 = [d['date'] for d in heart_rates_1]
    heart_rates_1 = [d['heart_rate'] for d in heart_rates_1]
    dates_2 = [d['date'] for d in heart_rates_2]
    heart_rates_2 = [d['heart_rate'] for d in heart_rates_2]
    df_1 = pd.DataFrame(heart_rates_1, index=dates_1, columns=['Heart Rate 1'])
    df_2 = pd.DataFrame(heart_rates_2, index=dates_2, columns=['Heart Rate 2'])
    df = pd.concat([df_1, df_2], axis=1).dropna()
    df.plot(kind='line', color=['blue', 'red'])
    plt.xlabel('Date')
    plt.ylabel('Heart Rate')
    plt.title('Heart Rate Trend')
    plt.grid(True)
    plt.show()

def plot_weight(weights):
    dates= [d['date'] for d in weights]
    weights = [d['weight'] for d in weights]
    
    df = pd.DataFrame(weights, index=dates, columns=['Weight'])
    df_trend = pd.DataFrame(weights, index=dates, columns=['Weight'])
    df.plot(kind='line', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Weights')
    plt.title('Weight Change')
    plt.grid(True)
    plt.show()

def calculate_average_and_trend(filtered_heart_rates):
    heart_rates_array = np.array([d['heart_rate'] for d in filtered_heart_rates])
    average = np.mean(heart_rates_array)
    trend = np.polyfit(range(len(heart_rates_array)), heart_rates_array, 1)
    return average, trend


from statsmodels.tsa.seasonal import STL

def seasonal_component(heart_rates):
    # Create a DataFrame from heart_rates
    df = pd.DataFrame(heart_rates)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # Handle missing values and resample data to a consistent frequency
    df = df.resample('D').mean()  # Resample to daily frequency, adjust as needed

    # Perform seasonal decomposition
    try:
        stl = STL(df['heart_rate'], seasonal=13)  # You may need to adjust the seasonal period
        result = stl.fit()

        # Plot the seasonal component
        seasonal = result.seasonal
        plt.figure(figsize=(12, 6))
        plt.plot(seasonal.index, seasonal.values, label='Seasonal Component')
        plt.xlabel('Date')
        plt.ylabel('Seasonal Component')
        plt.title('Seasonal Component of Heart Rate Time Series')
        plt.legend()
        plt.grid(True)
        plt.show()

        return seasonal
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    
   
    filtered_heart_rates = filter_heart_rates("resting_heart_rates.txt")
    start_date = filtered_heart_rates[0]['date']
    end_date = filtered_heart_rates[-1]['date']
    replaced_heart_rates = replace_none_hrs(filtered_heart_rates, start_date, end_date)
    #plot_heart_rates(replaced_heart_rates, filtered_heart_rates)
    
    #seasonal_component(filtered_heart_rates)

    """
    filtered_weights = filter_weights("weights.txt")
    start_date = filtered_weights[0]['date']
    end_date = filtered_weights[-1]['date']
    new_weights = replace_none_weights(filtered_weights, start_date, end_date)
    pd.da
    plot_weight(new_weights)
    """
    
