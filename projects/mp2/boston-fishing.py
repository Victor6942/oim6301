import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    from datetime import date, timedelta

    return


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
    return


if __name__ == "__main__":
    app.run()
