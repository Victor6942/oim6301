import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import marimo as mo

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"


    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _():
    as_of = "2026-11-05"
    return (as_of,)


@app.cell
def _(ask):
    ask("SELECT count(*) AS trips FROM trips")
    return


@app.cell
def _(ask):
    ask("DESCRIBE rivers")
    return


@app.cell
def _(ask):
    ask("DESCRIBE trips")
    return


@app.cell
def _(ask):
    ask("DESCRIBE bookings")
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS joined_rows
        FROM bookings
        JOIN trips  ON trips.trip_id = bookings.trip_id
        JOIN rivers ON rivers.river_id = trips.river_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Which state brings in the most revenue?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT party_size, count(*) AS bookings,
               min(price_charged) AS lowest, max(price_charged) AS highest
        FROM bookings
        GROUP BY party_size
        ORDER BY party_size
    """)
    return


@app.cell
def _(ask):
    ask("SELECT status, count(*) AS trips FROM trips GROUP BY status")
    return


@app.cell
def _(ask):
    revenue_by_state = ask("""
        SELECT rivers.state, sum(bookings.price_charged) AS revenue
        FROM bookings
        JOIN trips  ON trips.trip_id = bookings.trip_id
        JOIN rivers ON rivers.river_id = trips.river_id
        WHERE trips.status = 'completed'
        GROUP BY rivers.state
        ORDER BY revenue DESC
    """)

    revenue_by_state
    return (revenue_by_state,)


@app.cell
def _(ask, revenue_by_state):
    sum_of_states = float(revenue_by_state["revenue"].sum())
    total_directly = float(ask("""
        SELECT sum(bookings.price_charged) AS total
        FROM bookings
        JOIN trips ON trips.trip_id = bookings.trip_id
        WHERE trips.status = 'completed'
    """)["total"][0])

    print(sum_of_states, total_directly)
    assert round(sum_of_states, 2) == round(total_directly, 2), "state totals do not add up"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting completed trips only and treating price_charged as the booking's total,
    Massachusetts brings in the most revenue at $54,880, followed by Washington at $40,500
    and Oregon at $26,220. Across all six states, completed trips brought in $169,220.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. How many fish does a trip catch on each river?
    """)
    return


@app.cell
def _(ask):
    fish_per_trip = ask("""
        SELECT rivers.name AS river,
               count(DISTINCT trips.trip_id) AS trips,
               count(catches.catch_id) AS fish,
               round(count(catches.catch_id) * 1.0 / count(DISTINCT trips.trip_id), 2) AS fish_per_trip
        FROM trips
        JOIN rivers ON rivers.river_id = trips.river_id
        LEFT JOIN catches ON catches.trip_id = trips.trip_id
        WHERE trips.status = 'completed'
        GROUP BY rivers.name
        ORDER BY fish_per_trip DESC
    """)
    fish_per_trip
    return (fish_per_trip,)


@app.cell
def _(ask, fish_per_trip):
    fish_in_result = int(fish_per_trip["fish"].sum())
    fish_directly = ask("""
        SELECT count(*) AS n FROM catches
        JOIN trips ON trips.trip_id = catches.trip_id
        WHERE trips.status = 'completed'
    """)["n"][0]
    trips_in_result = int(fish_per_trip["trips"].sum())
    print(fish_in_result, fish_directly, trips_in_result)
    assert fish_in_result == fish_directly and trips_in_result == 256
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting completed trips only, including trips that caught nothing, the Yakima River has the
    highest catch rate at 3.85 fish per trip (150 fish on 39 trips), followed by the Kennebec
    at 3.67 and the Deerfield at 3.60. The Battenkill is lowest at 3.32.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Which fly caught the most fish?
    """)
    return


@app.cell
def _(ask):
    fly_catches = ask("""
        SELECT flies.fly_id, flies.pattern_name, flies.size, flies.fly_type,
               count(*) AS fish
        FROM catches
        JOIN flies ON flies.fly_id = catches.fly_id
        GROUP BY flies.fly_id, flies.pattern_name, flies.size, flies.fly_type
        ORDER BY fish DESC
    """)
    fly_catches
    return (fly_catches,)


@app.cell
def _(ask, fly_catches):
    fish_with_fly = int(fly_catches["fish"].sum())
    fish_without_fly = ask("SELECT count(*) AS n FROM catches WHERE fly_id IS NULL")["n"][0]
    all_fish = ask("SELECT count(*) AS n FROM catches")["n"][0]

    print(fish_with_fly, fish_without_fly, all_fish)
    assert fish_with_fly + fish_without_fly == all_fish
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Leaving out the 130 catches with no fly recorded, the Hopper (size 10, a dry fly) caught the
    most fish, 66, ahead of the Egg Pattern (size 14, nymph) with 55 and the Stimulator
    (size 10, dry) with 52.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##4: the busiest month by number of trips.
    """)
    return


@app.cell
def _(ask):
    trips_by_month = ask("""
        SELECT strftime(trip_date, '%Y-%m') AS month,
               count(*) AS trips
        FROM trips
        WHERE status = 'completed'
        GROUP BY month
        ORDER BY trips DESC, month
    """)
    trips_by_month
    return (trips_by_month,)


@app.cell
def _(trips_by_month):
    print(int(trips_by_month["trips"].sum()))
    assert int(trips_by_month["trips"].sum()) 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting completed trips by calendar month, May 2026 was the busiest with 37 trips, ahead of
    June 2026 with 32. August and October 2026 tied for third with 29 each.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Which clients haven't booked in the last 12 months, or ever?
    """)
    return


@app.cell
def _(as_of, ask):
    lapsed_clients = ask(f"""
        SELECT clients.client_id, clients.first_name, clients.last_name,
               max(trips.trip_date) AS last_trip
        FROM clients
        LEFT JOIN bookings ON bookings.client_id = clients.client_id
        LEFT JOIN trips    ON trips.trip_id = bookings.trip_id
        GROUP BY clients.client_id, clients.first_name, clients.last_name
        HAVING max(trips.trip_date) IS NULL
            OR max(trips.trip_date) < DATE '{as_of}' - INTERVAL 12 MONTH
        ORDER BY last_trip NULLS FIRST, clients.last_name
    """)
    lapsed_clients
    return (lapsed_clients,)


@app.cell
def _(as_of, ask, lapsed_clients):
    never_booked = int(lapsed_clients["last_trip"].is_null().sum())
    total_clients = ask("SELECT count(*) AS n FROM clients")["n"][0]
    active = ask(f"""
        SELECT count(DISTINCT bookings.client_id) AS n FROM bookings
        JOIN trips ON trips.trip_id = bookings.trip_id
        WHERE trips.trip_date >= DATE '{as_of}' - INTERVAL 12 MONTH
    """)["n"][0]
    print(never_booked, len(lapsed_clients), active, total_clients)
    assert never_booked == 6 and len(lapsed_clients) + active == total_clients
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the trip date as the date a client last booked, and counting back 12 months from
    2026-11-05, 6 of the 40 clients have not booked in that time, and all 6 have never booked at all:
    Noah Kim, Elena Moreau, Luis Park, Elena Reyes, Dana Sutton and Grace Walsh. No client booked
    and then lapsed, because the data covers only about 13 months.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How much does each guide earn the business, and how much do they cost?
    """)
    return


@app.cell
def _(ask):
    guide_results = ask("""
        WITH trip_revenue AS (
            SELECT trip_id, sum(price_charged) AS revenue
            FROM bookings
            GROUP BY trip_id
        )
        SELECT guides.guide_id, guides.first_name, guides.last_name,
               count(*) AS trips,
               sum(coalesce(trip_revenue.revenue, 0)) AS revenue,
               sum(trips.guide_pay) AS pay,
               sum(coalesce(trip_revenue.revenue, 0)) - sum(trips.guide_pay) AS margin
        FROM trips
        JOIN guides ON guides.guide_id = trips.guide_id
        LEFT JOIN trip_revenue ON trip_revenue.trip_id = trips.trip_id
        WHERE trips.status = 'completed'
        GROUP BY guides.guide_id, guides.first_name, guides.last_name
        ORDER BY margin DESC
    """)
    guide_results
    return (guide_results,)


@app.cell
def _(ask, guide_results):
    direct = ask("""
        SELECT count(*) AS trips,
               (SELECT sum(price_charged) FROM bookings
                JOIN trips t ON t.trip_id = bookings.trip_id
                WHERE t.status = 'completed') AS revenue,
               sum(guide_pay) AS pay
        FROM trips WHERE status = 'completed'
    """)
    print(int(guide_results["trips"].sum()), float(guide_results["revenue"].sum()), float(guide_results["pay"].sum()))
    print(int(direct["trips"][0]), float(direct["revenue"][0]), float(direct["pay"][0]))
    assert int(guide_results["trips"].sum()) == int(direct["trips"][0])
    assert round(float(guide_results["revenue"].sum()), 2) == round(float(direct["revenue"][0]), 2)
    assert round(float(guide_results["pay"].sum()), 2) == round(float(direct["pay"][0]), 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting completed trips only, with margin as revenue minus guide pay, Theo Ramsey has the
    highest margin at $31,100 from 73 trips, followed by Walt Brennan at $29,010 and Mara Lindqvist
    at $25,270. Josie Okafor is lowest at $20,940 from 51 trips. Every guide's margin is positive.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. For each fly, how many were used and how many fish did it catch?
    """)
    return


@app.cell
def _(ask):
    fly_use = ask("""
        WITH used AS (
            SELECT fly_id, sum(quantity_used) AS used
            FROM trip_flies GROUP BY fly_id
        ),
        caught AS (
            SELECT fly_id, count(*) AS fish
            FROM catches WHERE fly_id IS NOT NULL GROUP BY fly_id
        )
        SELECT flies.fly_id, flies.pattern_name, flies.size,
               coalesce(used.used, 0) AS used,
               coalesce(caught.fish, 0) AS fish,
               round(coalesce(caught.fish, 0) * 1.0 / nullif(coalesce(used.used, 0), 0), 2) AS fish_per_fly_used
        FROM flies
        LEFT JOIN used   ON used.fly_id = flies.fly_id
        LEFT JOIN caught ON caught.fly_id = flies.fly_id
        ORDER BY fish_per_fly_used DESC NULLS LAST, flies.fly_id
    """)
    fly_use
    return (fly_use,)


@app.cell
def _(ask, fly_use):
    used_direct = int(ask("SELECT sum(quantity_used) AS n FROM trip_flies")["n"][0])
    fish_direct = int(ask("SELECT count(*) AS n FROM catches WHERE fly_id IS NOT NULL")["n"][0])
    unused = int((fly_use["used"] == 0).sum())
    print(int(fly_use["used"].sum()), used_direct, int(fly_use["fish"].sum()), fish_direct, unused)
    assert int(fly_use["used"].sum()) == used_direct
    assert int(fly_use["fish"].sum()) == fish_direct 
    assert unused 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting all trips, the Stimulator (size 10) has the best catch rate at 0.50 fish per fly used
    (52 fish from 103 flies), just ahead of the Hopper (size 10) at 0.49 (66 fish from 136) and the
    Hare's Ear (size 16) at 0.47. The Hopper caught the most fish overall but was also used the most.
    Two flies were never used, so they have no rate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Which trips have more people booked than the maximum allowed?
    """)
    return


@app.cell
def _(ask):
    overbooked = ask("""
        SELECT trips.trip_id, trips.trip_date, trips.max_anglers,
               sum(bookings.party_size) AS booked
        FROM trips
        JOIN bookings ON bookings.trip_id = trips.trip_id
        GROUP BY trips.trip_id, trips.trip_date, trips.max_anglers
        HAVING sum(bookings.party_size) > trips.max_anglers
        ORDER BY trips.trip_id
    """)
    overbooked
    return (overbooked,)


@app.cell
def _(overbooked):
    print(sorted(overbooked["trip_id"].to_list()))
    assert sorted(overbooked["trip_id"].to_list()) 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two trips are booked over their limit: trip 76 (2026-04-22) and trip 146 (2026-06-19). Each has
    3 people booked against a maximum of 2. No other trip is over its maximum.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Which river has the highest cancellation rate?
    """)
    return


@app.cell
def _(ask):
    cancellations = ask("""
        SELECT rivers.name AS river,
               count(*) AS trips,
               sum(CASE WHEN trips.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
               round(100.0 * sum(CASE WHEN trips.status = 'cancelled' THEN 1 ELSE 0 END) / count(*), 1) AS cancel_pct
        FROM trips
        JOIN rivers ON rivers.river_id = trips.river_id
        GROUP BY rivers.name
        ORDER BY cancel_pct DESC
    """)
    cancellations
    return (cancellations,)


@app.cell
def _(cancellations):
    print(int(cancellations["trips"].sum()), int(cancellations["cancelled"].sum()))
    assert int(cancellations["trips"].sum()) == 300 and int(cancellations["cancelled"].sum()) 

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting every trip whatever its status, the Skagit River has the highest cancellation rate at
    12.9% (4 of 31 trips), followed by the Deschutes at 11.4% (5 of 44), while the Kennebec has the
    lowest at 5.4% (2 of 37). The rates rest on small numbers, since each river has only 2 to 5
    cancellations, so the gap between rivers may not be meaningful. Across all rivers, 26 of 300 trips
    (8.7%) were cancelled.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Which upcoming trips still have open spots?
    """)
    return


@app.cell
def _(ask):
    open_trips = ask("""
        SELECT * FROM upcoming_trips
        ORDER BY spots_left DESC, trip_date
        LIMIT 10
    """)
    open_trips
    return


@app.cell
def _(ask):
    upcoming_total = len(ask("SELECT * FROM upcoming_trips"))
    booked_trips = int(ask("SELECT count(*) AS n FROM trips WHERE status = 'booked'")["n"][0])
    print(upcoming_total, booked_trips)
    assert upcoming_total == booked_trips
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 18 upcoming trips, three tie for the most open spots, 2 each: the Deschutes River on
    2026-11-21, the Battenkill on 2026-11-24 and the Yakima River on 2026-11-25. Among the ten
    shown, the two Skagit River trips on 2026-11-11 and 2026-11-13 are already full.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further
    """)
    return


@app.cell
def _(mo, revenue_by_state):
    import altair as alt
    import polars as pl

    chart_data = revenue_by_state.with_columns(pl.col("revenue").cast(pl.Float64))
    revenue_chart = mo.ui.altair_chart(
        chart_data.plot.bar(
            x=alt.X("state", sort="-y", title="State"),
            y=alt.Y("revenue", title="Revenue from completed trips (dollars)"),
        ).properties(title="Revenue by state, completed trips")
    )
    revenue_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Massachusetts leads at $54,880 and Vermont is lowest at $11,980, so the gap
    is easier to see than in the table.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What the AI gave me.** For Question 1 (revenue for each state), the AI wrote a query that
    added up price_charged for each state. It assumed price_charged was the total for the whole
    booking. It could also have been a price per angler, in which case the query would be wrong,
    because it would need to multiply by party_size.

    **What I did.** I didn't accept the assumption. I grouped the bookings by party_size and looked
    at the lowest and highest price for each. Party size 1 ran from $220 to $380 and party size 2
    from $440 to $760, exactly double. So price_charged is already the total for the booking, and
    multiplying by party_size would have counted each party twice. I kept the query as it was, and
    I wrote the choice into my answer: "treating price_charged as the booking's total
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent
    """)
    return


app._unparsable_cell(
    r"""
    4 hours.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Reading it back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Prediction: I picked "Which state brings in the most revenue?" The joins go from
    bookings to trips to rivers. Before any grouping I expect 492 rows, because bookings
    has one row per client per trip, and each booking belongs to exactly one trip, and each
    trip belongs to exactly one river. So the joins should not add or drop any rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What happened: The three joined tables gave 492 rows, the same as my prediction and
    the same as the number of rows in bookings. Each booking belongs to one trip and each
    trip to one river, so no join added or dropped rows.

    What one row means: One row of the joined result is one client's booking on one trip,
    together with the river and state where that trip was fished.
    """)
    return


if __name__ == "__main__":
    app.run()
