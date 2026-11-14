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
    return


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
