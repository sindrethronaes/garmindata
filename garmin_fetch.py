import datetime
import json
from garminconnect import Garmin

def init_api():
    api = Garmin('sthronae@online.no','Garminsjokolade12')
    api.login()
    return api

def get_dates_in_range(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    return dates

def display_json(api_call, output):
    #Format API output for better readability.

    dashed = "-" * 20
    header = f"{dashed} {api_call} {dashed}"
    footer = "-" * len(header)

    print(header)

    if isinstance(output, (int, str, dict, list)):
        print(json.dumps(output, indent=4))
    else:
        print(output)

    print(footer)

def save_to_file(data, filename):
    with open(filename, 'w') as f: 
        for line in data: 
            f.write(line + '\n')


if  __name__ == "__main__":

  start_date = datetime.date(2019, 1, 1)
  end_date = datetime.date(2024, 2, 16)

  dates_in_range = get_dates_in_range(start_date, end_date)

  api = init_api()

  lines = []

  for date in dates_in_range:
      details = api.get_stats_and_body(date)

      #stats = display_json("Getting stats and body details", details) # To get insight into return of Gamrin Api Query

      weight = details["weight"]
      
      line = f"Date: {date}, Weight: " + str(weight)
      lines.append(line)
  
  for element in lines:
      print(element)

  save_to_file(lines, 'weights.txt')
    
  
"""


start_date = datetime.date(2024, 2, 15) # Format -> (year, month, day)
end_date = datetime.date(2024, 2, 16)

activities = api.get_activities_by_date(
                start_date.isoformat(), end_date.isoformat(), 'cycling')


for activity in activities:
    activity_id = activity["activityId"]
    
    gpx_data = api.download_activity(
                        activity_id, dl_fmt=api.ActivityDownloadFormat.GPX
                    )
    output_file = f"./{str(activity_id)}.KML"
    with open(output_file, "wb") as fb:
        fb.write(gpx_data)

print("Finished....")

"""