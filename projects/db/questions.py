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


if __name__ == "__main__":
    app.run()
