import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
counter = 0
df = pd.read_csv("SolarPrediction.csv")

x = []
y = []
z = []
h=[]
i=[]

d = input("Enter date: ")
m = input("Enter month number: ")

df["DateTime"] = pd.to_datetime(
    df["Data"].astype(str) + " " + df["Time"].astype(str)
)

X = df["Radiation"].mean()

for new in df["Data"]:
    if new == f"{m}/{d}/2016 12:00:00 AM":
        x.append(df["Time"].iloc[counter])
        y.append(df["Radiation"].iloc[counter])
        z.append(df["Temperature"].iloc[counter])
        h.append(df["Humidity"].iloc[counter])
        i.append(df["DateTime"].iloc[counter])
    counter += 1

x = np.array(x)
y = np.array(y)
z=np.array(z)
h=np.array(h)
i=np.array(i)
order = np.argsort(i)

i = i[order]
y = y[order]
z = z[order]
h = h[order]
x = x[order]

Rad_mean=np.mean(y)

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

ax[0].scatter(z, y, s=4, color = "orange")
ax[0].set_xlabel("Temperature")
ax[0].set_ylabel("Solar Radiation")
ax[0].set_title(f"Radiation vs Temperature on {m}/{d}/2016", fontsize = 15, fontweight = "bold", color = "Black")
ax[0].legend()


ax[1].scatter(h, y, s=4)
ax[1].set_xlabel("Humidity")
ax[1].set_ylabel("Solar Radiation")
ax[1].set_title(f"Radiation vs Humidity on {m}/{d}/2016", fontsize = 15, fontweight = "bold", color = "Black")
ax[1].legend()

ax[2].plot(i, y, color="purple", linewidth=1)
ax[2].axhline(X, color="green", linestyle="--",
              label="Overall Average")
ax[2].axhline(Rad_mean, color="red", linestyle="--",
              label="Daily Average")
ax[2].set_xlabel("Date and Time")
ax[2].set_ylabel("Solar Radiation")
ax[2].set_title("Radiation vs Time on {m}/{d}/2016", fontsize = 15, fontweight = "bold", color = "Black")
ax[2].tick_params(axis="x", rotation=45)
ax[2].legend()
fig.suptitle(f"Solar Radiation Analysis — {m}/{d}/2016", fontsize = 20, fontweight = "bold", color = "Black", family = "Arial")
plt.tight_layout()
plt.show()



df["HourMinute"] = pd.to_datetime(
    df["Time"].astype(str),
    format="%H:%M:%S",
    errors="coerce"
)
dates = sorted(df["DateTime"].dt.date.unique())

if len(dates) > 5:
    indices = np.linspace(0, len(dates) - 1, 5, dtype=int)
    selected_dates = [dates[j] for j in indices]
else:
    selected_dates = dates

fig, ax = plt.subplots(figsize=(12, 6), dpi=120)

for date in selected_dates:
    day_data = df[df["DateTime"].dt.date == date].copy()
    day_data = day_data.sort_values("DateTime")

    time_hours = (
        day_data["DateTime"].dt.hour
        + day_data["DateTime"].dt.minute / 60
        + day_data["DateTime"].dt.second / 3600
    )

    ax.plot(
        time_hours,
        day_data["Radiation"],
        linewidth=1.5,
        label=str(date)
    )

ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Solar Radiation", fontsize=12)
ax.set_title(
    "Solar Radiation Profiles Across Different Days",
    fontsize=15,
    fontweight="bold"
)

ax.set_xticks(range(0, 24, 2))
ax.grid(True, linestyle="--", alpha=0.3)
ax.legend(title="Date")
plt.tight_layout()
plt.show()
# Some days have bell curves while others show irregular patterns, indicating varying weather conditions and solar exposure.

# Two days reported average humidity above 100, which is unusual and may indicate sensor errors or extreme conditions.
daily_humidity = df.groupby("Data")["Humidity"].mean()

print("\nDays with average humidity above 100:")
print(daily_humidity[daily_humidity > 100])


#The solar radiation data shows a clear diurnal pattern, with peaks around midday and low values during the night, consistent with expected solar exposure.
df["Hour"] = df["DateTime"].dt.hour

hourly_radiation = df.groupby("Hour")["Radiation"].mean()

print("Average solar radiation by hour:")
print(hourly_radiation.round(2))

print("\nHour with highest average radiation:",
      hourly_radiation.idxmax())

print("Highest hourly average radiation:",
      round(hourly_radiation.max(), 2))

plt.figure(figsize=(10, 5))
plt.plot(hourly_radiation.index, hourly_radiation.values,
         marker="o", linewidth=2)

plt.xlabel("Hour of Day")
plt.ylabel("Average Solar Radiation")
plt.title("Average Solar Radiation by Hour",
          fontweight="bold")
plt.xticks(range(0, 24, 2))
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
#Temperature tends to show a positive correlation with solar radiation, as higher temperatures often coincide with increased sunlight. However, the relationship is not strictly linear, as other factors like cloud cover can influence radiation levels.
#two days with similar average radiation can have quite different peak radiation. This suggests that daily averages alone may hide short-lived peaks in solar intensity.


df["DateOnly"] = df["DateTime"].dt.date

daily_stats = df.groupby("DateOnly")["Radiation"].agg(
    Daily_Maximum="max",
    Daily_Average="mean"
)

print("\nDaily Maximum and Average Solar Radiation:")
print(daily_stats.round(2).to_string())



peak_index = df["Radiation"].idxmax()
peak = df.loc[peak_index]

print("\nHighest Recorded Solar Radiation")
print("Date:", peak["DateTime"].date())
print("Time:", peak["DateTime"].strftime("%H:%M:%S"))
print("Radiation:", peak["Radiation"])
print("Temperature:", peak["Temperature"])
print("Humidity:", peak["Humidity"])
print("Wind Speed:", peak["Speed"])



date_string = peak["DateTime"].strftime("%Y-%m-%d")

sunrise = pd.to_datetime(
    date_string + " " + peak["TimeSunRise"]
)

sunset = pd.to_datetime(
    date_string + " " + peak["TimeSunSet"]
)

peak_time = peak["DateTime"]

after_sunrise = peak_time - sunrise
before_sunset = sunset - peak_time

print("\nSunrise and Sunset Analysis")
print("Sunrise:", sunrise.strftime("%H:%M:%S"))
print("Peak time:", peak_time.strftime("%H:%M:%S"))
print("Sunset:", sunset.strftime("%H:%M:%S"))

print("Time after sunrise:", after_sunrise)
print("Time before sunset:", before_sunset)

print(
    "Peak occurs after sunrise:",
    after_sunrise.total_seconds() / 3600,
    "hours"
)



top_5_days = daily_stats.sort_values(
    by="Daily_Average",
    ascending=False
).head(5)

print("\nTop 5 Days by Average Solar Radiation:")
print(top_5_days.round(2).to_string())


plt.figure(figsize=(9, 5))

plt.bar(
    top_5_days.index.astype(str),
    top_5_days["Daily_Average"]
)

plt.xlabel("Date")
plt.ylabel("Average Solar Radiation")
plt.title("Top 5 Days by Average Solar Radiation",
          fontweight="bold")

plt.xticks(rotation=30)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()



from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
df = pd.read_csv("SolarPrediction.csv")
date_part = df["Data"].astype(str).str.split().str[0]
df["DateTime"] = pd.to_datetime(
    date_part + " " + df["Time"].astype(str),
    errors="coerce"
)
df["Hour"] = (
    df["DateTime"].dt.hour
    + df["DateTime"].dt.minute / 60
)
df["DayOfYear"] = df["DateTime"].dt.dayofyear
df["HourSin"] = np.sin(2 * np.pi * df["Hour"] / 24)
df["HourCos"] = np.cos(2 * np.pi * df["Hour"] / 24)
df["YearSin"] = np.sin(
    2 * np.pi * df["DayOfYear"] / 365.25
)
df["YearCos"] = np.cos(
    2 * np.pi * df["DayOfYear"] / 365.25
)
wind = pd.to_numeric(
    df["WindDirection(Degrees)"],
    errors="coerce"
)
df["WindSin"] = np.sin(np.deg2rad(wind))
df["WindCos"] = np.cos(np.deg2rad(wind))
features = [
    "Temperature",
    "Humidity",
    "Pressure",
    "Speed",
    "HourSin",
    "HourCos",
    "YearSin",
    "YearCos",
    "WindSin",
    "WindCos"
]
target = "Radiation"
numeric_columns = [
    "Temperature",
    "Humidity",
    "Pressure",
    "Speed",
    target
]
for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )
data = df[
    features + [target, "DateTime"]
].dropna().copy()
print("Total usable observations:", len(data))
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print("\nSOLAR RADIATION PREDICTION RESULTS")
print("----------------------------------")
print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))
print("RMSE:", round(rmse, 2))
print("R-squared score:", round(r2, 4))
print("R-squared percentage:", round(r2 * 100, 2), "%")
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})
importance = importance.sort_values(
    by="Importance",
    ascending=False
)
print("\nFEATURE IMPORTANCE")
print(importance.to_string(index=False))
plt.figure(figsize=(9, 6))
plt.barh(
    importance["Feature"],
    importance["Importance"]
)
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Solar Radiation Feature Importance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(
    "solar_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.figure(figsize=(8, 6))
plt.scatter(
    y_test,
    y_pred,
    alpha=0.5,
    label="Predictions"
)
lower = min(y_test.min(), y_pred.min())
upper = max(y_test.max(), y_pred.max())
plt.plot(
    [lower, upper],
    [lower, upper],
    "k--",
    label="Perfect prediction"
)
metrics_text = (
    f"RMSE = {rmse:.2f}\n"
    f"R-squared = {r2:.4f}"
)
plt.text(
    0.05,
    0.95,
    metrics_text,
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        edgecolor="gray",
        alpha=0.9
    )
)
plt.xlabel("Actual Solar Radiation")
plt.ylabel("Predicted Solar Radiation")
plt.title("Actual vs Predicted Solar Radiation")
plt.legend()
plt.tight_layout()
plt.savefig(
    "solar_radiation_prediction.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
