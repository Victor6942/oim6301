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
