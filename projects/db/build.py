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

    return ask, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Tables
    """)
    return


@app.cell
def _(database, duckdb, mo):
    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE clients (
                client_id   INTEGER PRIMARY KEY,
                first_name  VARCHAR NOT NULL,
                last_name   VARCHAR NOT NULL,
                email       VARCHAR NOT NULL UNIQUE,
                phone       VARCHAR,
                join_date   DATE NOT NULL
            )
        """)
        _con.execute("""
            CREATE TABLE guides (
                guide_id       INTEGER PRIMARY KEY,
                first_name     VARCHAR NOT NULL,
                last_name      VARCHAR NOT NULL,
                license_number VARCHAR NOT NULL UNIQUE,
                hire_date      DATE NOT NULL
            )
        """)
        _con.execute("""
            CREATE TABLE rivers (
                river_id INTEGER PRIMARY KEY,
                name     VARCHAR NOT NULL,
                region   VARCHAR NOT NULL,
                state    VARCHAR NOT NULL,
                UNIQUE (name, state)
            )
        """)
        _con.execute("""
            CREATE TABLE flies (
                fly_id       INTEGER PRIMARY KEY,
                pattern_name VARCHAR NOT NULL,
                size         VARCHAR NOT NULL,
                fly_type     VARCHAR NOT NULL CHECK (fly_type IN ('dry', 'nymph', 'streamer')),
                cost         DECIMAL(6, 2) NOT NULL CHECK (cost >= 0),
                UNIQUE (pattern_name, size)
            )
        """)
        _con.execute("""
            CREATE TABLE trips (
                trip_id     INTEGER PRIMARY KEY,
                guide_id    INTEGER NOT NULL REFERENCES guides(guide_id),
                river_id    INTEGER NOT NULL REFERENCES rivers(river_id),
                trip_date   DATE NOT NULL,
                start_time  TIME NOT NULL,
                hours       DECIMAL(3, 1) NOT NULL CHECK (hours > 0),
                max_anglers INTEGER NOT NULL CHECK (max_anglers > 0),
                guide_pay   DECIMAL(8, 2) NOT NULL CHECK (guide_pay > 0),
                status      VARCHAR NOT NULL CHECK (status IN ('booked', 'completed', 'cancelled'))
            )
        """)
        _con.execute("""
            CREATE TABLE bookings (
                trip_id       INTEGER NOT NULL REFERENCES trips(trip_id),
                client_id     INTEGER NOT NULL REFERENCES clients(client_id),
                party_size    INTEGER NOT NULL CHECK (party_size >= 1),
                price_charged DECIMAL(8, 2) NOT NULL CHECK (price_charged > 0),
                PRIMARY KEY (trip_id, client_id)
            )
        """)
        _con.execute("""
            CREATE TABLE trip_flies (
                trip_id       INTEGER NOT NULL REFERENCES trips(trip_id),
                fly_id        INTEGER NOT NULL REFERENCES flies(fly_id),
                quantity_used INTEGER NOT NULL CHECK (quantity_used > 0),
                PRIMARY KEY (trip_id, fly_id)
            )
        """)
        _con.execute("""
            CREATE TABLE catches (
                catch_id INTEGER PRIMARY KEY,
                trip_id  INTEGER NOT NULL REFERENCES trips(trip_id),
                fly_id   INTEGER REFERENCES flies(fly_id),
                species  VARCHAR NOT NULL
            )
        """)
        for _table in ["clients", "guides", "rivers", "flies", "trips", "bookings", "trip_flies", "catches"]:
            _csv = mo.notebook_dir() / "data" / f"{_table}.csv"
            _con.execute(f"INSERT INTO {_table} SELECT * FROM read_csv('{_csv}', header = true)")
        _con.execute("""
            CREATE VIEW upcoming_trips AS
            SELECT t.trip_id, t.trip_date, r.name AS river, g.last_name AS guide,
                   t.max_anglers,
                   coalesce(sum(b.party_size), 0) AS booked,
                   t.max_anglers - coalesce(sum(b.party_size), 0) AS spots_left
            FROM trips t
            JOIN rivers r ON r.river_id = t.river_id
            JOIN guides g ON g.guide_id = t.guide_id
            LEFT JOIN bookings b ON b.trip_id = t.trip_id
            WHERE t.status = 'booked'
            GROUP BY t.trip_id, t.trip_date, r.name, g.last_name, t.max_anglers
        """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) FROM trips")
    return


@app.cell
def _(ask):
    ask("SELECT table_name FROM information_schema.tables ORDER BY table_name")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Look at the Data
    """)
    return


@app.cell
def _(mo):
    import polars as pl

    trips_df = pl.read_csv(mo.notebook_dir() / "data" / "trips.csv", try_parse_dates=True)
    trips_by_month = (
        trips_df
        .with_columns(pl.col("trip_date").dt.month().alias("month"))
        .group_by("month")
        .len()
        .sort("month")
    )
    trips_by_month.plot.bar(x="month", y="len")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
    SELECT 'clients' AS table_name, count(*) AS row_count FROM clients
    UNION ALL SELECT 'guides', count(*) FROM guides
    UNION ALL SELECT 'rivers', count(*) FROM rivers
    UNION ALL SELECT 'flies', count(*) FROM flies
    UNION ALL SELECT 'trips', count(*) FROM trips
    UNION ALL SELECT 'bookings', count(*) FROM bookings
    UNION ALL SELECT 'trip_flies', count(*) FROM trip_flies
    UNION ALL SELECT 'catches', count(*) FROM catches
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    with duckdb.connect(database) as _con:
        try:
            _con.execute("INSERT INTO trips VALUES (9999, 1, 1, '2026-06-01', '06:00', 6, 2, 250, 'maybe')")
        except duckdb.Error as _e:
            print(_e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Answers You Already Knew
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS trips FROM trips")
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS never_booked FROM clients WHERE client_id NOT IN (SELECT client_id FROM bookings)")
    return


@app.cell
def _(ask):
    ask("""
    SELECT t.trip_id, t.max_anglers, sum(b.party_size) AS booked
    FROM trips t JOIN bookings b ON b.trip_id = t.trip_id
    GROUP BY t.trip_id, t.max_anglers
    HAVING sum(b.party_size) > t.max_anglers
    ORDER BY t.trip_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A View
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM upcoming_trips ORDER BY trip_date")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The question: Which upcoming trips still have room for another angler? A guide service asks this every week, to decide which trips to promote and which are full.

    How it works: upcoming_trips is saved with CREATE VIEW in the cell that builds the database. It adds up the party sizes booked on each trip with status "booked" and subtracts them from `max_anglers`, so `spots_left` is always current. Anybody can ask for it by name: `SELECT * FROM upcoming_trips`. I will use it in Part B.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS overbooked FROM upcoming_trips WHERE spots_left < 0")
    return


if __name__ == "__main__":
    app.run()
