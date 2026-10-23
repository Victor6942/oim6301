import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    from datetime import date, timedelta

    return date, requests, timedelta


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # 1. The Question
    # 2. My Plan Before AI
    # 3. Inputs
    # 4. The Work
    # 5. The Answer
    # 6. How I Know These Numbers Are Right
    # 7. Working With the Agent
    # 8. Reading It Back
    # 9. Going Further
    # 10. Time Spent
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. The Question
    Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Shoreline anglers around Boston mostly fish for striped bass, and the tide matters because moving water brings the bait fish in, and the bass follow them. This tool takes the tide times and the weather forecast for the next few days and shows which tides give a good window. It helps an angler decide which day and which tide to fish, and which ones to skip because of strong wind or rain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. My Plan Before AI
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Steps:
    1. Set the inputs: ten spots (each with its tide station and coordinates), how many days ahead, and my wind and rain limits.
    2. For one spot, ask NOAA for the high and low tide times and heights.
    3. For the same spot, ask Open-Meteo for the hourly wind and rain chance.
    4. For each high tide, find the weather hours from 2 hours before to 2 hours after it.
    5. Take the highest wind and highest rain chance in that window. Mark it good if both are under my limits, otherwise skip.
    6. Repeat for all ten spots with a loop, and keep every result in a list.
    7. Print a table, then one sentence naming the best spot and time.
    8. Save the fetched records to CSV files in projects/mp2/data/.

    Functions:
    - get_tides(station, days): takes a NOAA station ID and a number of days, returns a list of tides with time, type (H or L) and height in feet.
    - get_weather(latitude, longitude, days): takes coordinates and a number of days, returns a list of hours with time, rain chance and wind in mph.

    Addresses:
    - https://api.tidesandcurrents.noaa.gov/api/prod/datagetter (tides)
    - https://api.open-meteo.com/v1/forecast (weather)

    How I will know I have every record: Open-Meteo should return days x 24 hours for each spot, and NOAA should return about 4 tides per day (2 high, 2 low).

    Section 6 check: the number of weather hours I collected for each spot should equal days x 24. I will also find one row of my table in the raw Open-Meteo reply in my browser.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Inputs
    """)
    return


@app.cell
def _():
    # Spots to check: name, coordinates for the weather, NOAA station for the tides
    spots = [
        {"name": "Boston (Castle Island)",   "latitude": 42.336, "longitude": -71.011, "station": "8443970"},
        {"name": "Salem / Marblehead",       "latitude": 42.500, "longitude": -70.860, "station": "8442645"},
        {"name": "Gloucester",               "latitude": 42.600, "longitude": -70.650, "station": "8441551"},
        {"name": "Plum Island / Newburyport","latitude": 42.800, "longitude": -70.800, "station": "8440466"},
        {"name": "Scituate",                 "latitude": 42.200, "longitude": -70.720, "station": "8445138"},
        {"name": "Plymouth",                 "latitude": 41.960, "longitude": -70.670, "station": "8446493"},
        {"name": "Cape Cod Canal (Sandwich)","latitude": 41.770, "longitude": -70.500, "station": "8447173"},
        {"name": "Chatham",                  "latitude": 41.670, "longitude": -69.950, "station": "8447435"},
        {"name": "Provincetown",             "latitude": 42.050, "longitude": -70.190, "station": "8446121"},
        {"name": "Nantucket",                "latitude": 41.285, "longitude": -70.100, "station": "8449130"},
    ]

    days = 3                 # how many days ahead to look
    max_wind_mph = 15        # skip a window if wind goes above this
    max_rain_chance = 30     # skip a window if rain chance goes above this (%)
    hours_before_high = 2    # start of the window, before high tide
    hours_after_high = 2     # end of the window, after high tide
    return (
        days,
        hours_after_high,
        hours_before_high,
        max_rain_chance,
        max_wind_mph,
        spots,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. The Work
    """)
    return


@app.cell
def _():
    import csv
    import os
    from datetime import datetime

    return csv, datetime, os


@app.cell
def _(date, requests, timedelta):
    def get_tides(station, days):
        first_day = date.today()
        last_day = first_day + timedelta(days=days - 1)
        reply = requests.get(
            "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
            params={
                "begin_date": first_day.strftime("%Y%m%d"),
                "end_date": last_day.strftime("%Y%m%d"),
                "station": station,
                "product": "predictions",
                "datum": "MLLW",
                "time_zone": "lst_ldt",
                "interval": "hilo",
                "units": "english",
                "format": "json",
            },
            timeout=10,
        )
        tides = []
        for _row in reply.json()["predictions"]:
            tides.append({"time": _row["t"], "type": _row["type"], "height_ft": float(_row["v"])})
        return tides

    return (get_tides,)


@app.cell
def _(requests):
    def get_weather(latitude, longitude, days):
        reply = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "precipitation_probability,wind_speed_10m",
                "wind_speed_unit": "mph",
                "timezone": "America/New_York",
                "forecast_days": days,
            },
            timeout=10,
        )
        hourly = reply.json()["hourly"]
        hours = []
        for _time, _rain, _wind in zip(hourly["time"], hourly["precipitation_probability"], hourly["wind_speed_10m"]):
            hours.append({"time": _time, "rain_chance": _rain, "wind_mph": _wind})
        return hours

    return (get_weather,)


@app.cell
def _(
    csv,
    datetime,
    days,
    get_tides,
    get_weather,
    hours_after_high,
    hours_before_high,
    max_rain_chance,
    max_wind_mph,
    os,
    spots,
    timedelta,
):
    rows = []
    weather_counts = {}
    tide_records = []
    weather_records = []

    for _spot in spots:
        _tides = get_tides(_spot["station"], days)
        _hours = get_weather(_spot["latitude"], _spot["longitude"], days)
        weather_counts[_spot["name"]] = len(_hours)

        # look up weather by its hour, like "2026-10-23T09:00"
        _by_time = {}
        for _h in _hours:
            _by_time[_h["time"]] = _h
            weather_records.append({"spot": _spot["name"], "time": _h["time"],
                                    "rain_chance": _h["rain_chance"], "wind_mph": _h["wind_mph"]})

        for _t in _tides:
            tide_records.append({"spot": _spot["name"], "time": _t["time"],
                                 "type": _t["type"], "height_ft": _t["height_ft"]})
            if _t["type"] != "H":
                continue
            # tide time "2026-10-23 09:36" -> start of that hour
            _when = datetime.strptime(_t["time"], "%Y-%m-%d %H:%M").replace(minute=0)
            _winds = []
            _rains = []
            for _offset in range(-hours_before_high, hours_after_high + 1):
                _key = (_when + timedelta(hours=_offset)).strftime("%Y-%m-%dT%H:00")
                if _key in _by_time:
                    _winds.append(_by_time[_key]["wind_mph"])
                    if _by_time[_key]["rain_chance"] is not None:
                        _rains.append(_by_time[_key]["rain_chance"])
            if len(_winds) == 0:
                continue
            _max_wind = max(_winds)
            _max_rain = max(_rains) if len(_rains) > 0 else 0
            rows.append({
                "spot": _spot["name"],
                "time": _t["time"],
                "height_ft": _t["height_ft"],
                "max_wind": _max_wind,
                "max_rain": _max_rain,
                "good": _max_wind <= max_wind_mph and _max_rain <= max_rain_chance,
            })

    # save what was fetched
    os.makedirs("projects/mp2/data", exist_ok=True)
    with open("projects/mp2/data/tides.csv", "w", newline="") as _f:
        _w = csv.DictWriter(_f, fieldnames=["spot", "time", "type", "height_ft"])
        _w.writeheader()
        _w.writerows(tide_records)
    with open("projects/mp2/data/weather.csv", "w", newline="") as _f:
        _w = csv.DictWriter(_f, fieldnames=["spot", "time", "rain_chance", "wind_mph"])
        _w.writeheader()
        _w.writerows(weather_records)

    len(rows)
    return rows, weather_counts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. The Answer
    """)
    return


@app.cell
def _(rows):
    print(f"{'Spot':<28}{'High tide':<18}{'Ft':>6}{'Wind':>7}{'Rain%':>7}  Verdict")
    for _row in rows:
        _verdict = "GOOD" if _row["good"] else "skip"
        print(f"{_row['spot']:<28}{_row['time']:<18}{_row['height_ft']:>6.1f}{_row['max_wind']:>7.1f}{_row['max_rain']:>7}  {_verdict}")
    return


@app.cell
def _(days, max_rain_chance, max_wind_mph, rows):
    best = None
    good_count = 0
    for _row in rows:
        if _row["good"]:
            good_count += 1
            if best is None or _row["max_wind"] < best["max_wind"]:
                best = _row

    if best is None:
        print(f"None of the {len(rows)} high tides in the next {days} days stay under {max_wind_mph} mph wind and {max_rain_chance}% rain, so skip fishing.")
    else:
        print(f"{good_count} of {len(rows)} high tides pass my limits. The calmest is {best['spot']} at {best['time']}, with a {best['height_ft']:.1f} ft tide, wind up to {best['max_wind']:.1f} mph and rain chance {best['max_rain']}%.")
    return (best,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(days, rows, spots, weather_counts):
    for _name in weather_counts:
        _expected = days * 24
        _got = weather_counts[_name]
        print(f"{_name:<28} weather hours: {_got}, expected {_expected}, {'OK' if _got == _expected else 'MISMATCH'}")

    print(f"high-tide windows: {len(rows)}, expected about {len(spots) * days * 2}")
    return


@app.cell
def _(best, csv, datetime, hours_after_high, hours_before_high, timedelta):
    _tide_time = datetime.strptime(best["time"], "%Y-%m-%d %H:%M")
    _start = _tide_time.replace(minute=0) - timedelta(hours=hours_before_high)
    _end = _tide_time.replace(minute=0) + timedelta(hours=hours_after_high)

    _winds_from_file = []
    with open("projects/mp2/data/weather.csv") as _f:
        for _line in csv.DictReader(_f):
            if _line["spot"] == best["spot"]:
                _hour = datetime.strptime(_line["time"], "%Y-%m-%dT%H:%M")
                if _start <= _hour <= _end:
                    _winds_from_file.append(float(_line["wind_mph"]))

    _check_wind = max(_winds_from_file)
    print(f"table says {best['max_wind']:.1f} mph, file says {_check_wind:.1f} mph, {'OK' if abs(best['max_wind'] - _check_wind) < 0.01 else 'MISMATCH'}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check 1 would have caught a spot where the weather request came back short, for example a missing day. Check 2 reads the saved file and finds the same window a different way, so it would have caught a time-matching mistake in the loop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 7. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1:What the agent gave me: My first plan used one location, Boston, with one NOAA tide station and one set of weather coordinates. The agent treated that as representative of the whole coast.

    2:What I changed: From my own experience fishing, I knew weather changes a lot from one coastal town to the next. I asked for ten popular Massachusetts shore-fishing spots instead, each with its own coordinates for the weather and its own NOAA tide station. I turned the single station and coordinates into a `spots` list in the Inputs cell (section 3), and I put the tide and weather requests inside a loop over the spots (section 4).

    3. How I knew:My table proves the change was needed. For the high tide on 2026-10-22 around 9 AM, the highest wind in the window was 12.8 mph at Plum Island, 12.1 mph at Boston, 24.9 mph at Plymouth and 28.7 mph at Nantucket. With a 15 mph limit, the same tide was GOOD at Boston and Plum Island and skip at Plymouth and Nantucket. A single-location tool would have given one answer for all ten spots, which would have been wrong for most of them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 8. Reading It Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. get_tides
    - Goes in: a tide station ID and a number of days.
    - Comes out: a list of tides, each with a time, H or L, and a height in feet.
    - One line I had to ask about: `float(_row["v"])`. NOAA sends the height as text, and float() turns it into a number.

    2. get_weather
    - Goes in: latitude, longitude and a number of days.
    - Comes out: a list of hours, each with a time, a rain chance and a wind speed in mph.
    - One line I had to ask about: `zip(...)`. Open-Meteo sends three separate lists, and zip lines them up so each hour gets one record.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 9. Going Further
    """)
    return


@app.cell
def _(rows, spots):
    import folium

    fishing_map = folium.Map(location=[42.0, -70.6], zoom_start=8)

    for _spot in spots:
        _total = 0
        _good = 0
        for _row in rows:
            if _row["spot"] == _spot["name"]:
                _total += 1
                if _row["good"]:
                    _good += 1

        if _total == 0:
            _share = 0
        else:
            _share = _good / _total

        if _share >= 0.66:
            _color = "green"
        elif _share >= 0.33:
            _color = "orange"
        else:
            _color = "red"

        folium.CircleMarker(
            location=[_spot["latitude"], _spot["longitude"]],
            radius=12,
            color=_color,
            fill=True,
            fill_opacity=0.7,
            tooltip=_spot["name"],
            popup=f"{_spot['name']}: {_good} of {_total} high tides are good",
        ).add_to(fishing_map)

    fishing_map
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I put the ten fishing spots on a map using the folium library, which I added with `uv add folium`. Each circle is colored by how many of that spot's high tides pass my wind and rain limits. Green means two-thirds or more pass, orange means between a third and two-thirds, and red means fewer than a third.

    On the map, three spots are green: Boston, Plum Island and Gloucester. The other seven are orange, and none are red. Boston is the best because all 6 of its high tides pass, then Plum Island with 5 of 6, then Gloucester with 4 of 6. Every other spot passes 3 of 6. These counts are from the forecast I pulled on October 22, so they will change when the forecast changes. T
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 10. Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2
    """)
    return


if __name__ == "__main__":
    app.run()
