import pandas as pd


daily_activity = pd.read_csv("data/dailyActivity_merged.csv")
sleep = pd.read_csv("data/sleepDay_merged.csv")
weight = pd.read_csv("data/weightLogInfo_merged.csv")
heart_rate = pd.read_csv("data/heartrate_seconds_merged.csv")

hourly_steps = pd.read_csv("data/hourlySteps_merged.csv")
hourly_intensity = pd.read_csv("data/hourlyIntensities_merged.csv")
hourly_calories = pd.read_csv("data/hourlyCalories_merged.csv")

minute_calories = pd.read_csv("data/minuteCaloriesNarrow_merged.csv")
minute_intensity = pd.read_csv("data/minuteIntensitiesNarrow_merged.csv")
minute_mets = pd.read_csv("data/minuteMETsNarrow_merged.csv")


print("Daily activity rows:", len(daily_activity))
print("Sleep rows before removing duplicates:", len(sleep))

sleep = sleep.drop_duplicates()

print("Sleep rows after removing duplicates:", len(sleep))
print("Weight rows:", len(weight))
print("Heart rate rows:", len(heart_rate))


hourly = pd.merge(
    hourly_steps,
    hourly_intensity,
    on=["Id", "ActivityHour"]
)

hourly = pd.merge(
    hourly,
    hourly_calories,
    on=["Id", "ActivityHour"]
)


minutely = pd.merge(
    minute_calories,
    minute_intensity,
    on=["Id", "ActivityMinute"]
)

minutely = pd.merge(
    minutely,
    minute_mets,
    on=["Id", "ActivityMinute"]
)


time_format = "%m/%d/%Y %I:%M:%S %p"

daily_activity["Date"] = pd.to_datetime(
    daily_activity["ActivityDate"], format="%m/%d/%Y"
)

sleep["Date"] = pd.to_datetime(
    sleep["SleepDay"], format=time_format
)

weight["Date"] = pd.to_datetime(
    weight["Date"], format=time_format
)

hourly["Date"] = pd.to_datetime(
    hourly["ActivityHour"], format=time_format
)

minutely["Date"] = pd.to_datetime(
    minutely["ActivityMinute"], format=time_format
)


heart_rate["Date"] = pd.to_datetime(
    heart_rate["Time"], format=time_format
)

heart_rate["Date"] = heart_rate["Date"].dt.floor("min")

minute_heart_rate = heart_rate.groupby(
    ["Id", "Date"], as_index=False
)["Value"].mean()

minute_heart_rate = minute_heart_rate.rename(
    columns={"Value": "HeartRate"}
)


print("\nDaily activity:")
print(daily_activity.head())

print("\nSleep:")
print(sleep.head())

print("\nMerged hourly data:")
print(hourly.head())
print("Rows:", len(hourly))

print("\nMerged minute data:")
print(minutely.head())
print("Rows:", len(minutely))

print("\nAverage heart rate per minute:")
print(minute_heart_rate.head())
print("Rows:", len(minute_heart_rate))