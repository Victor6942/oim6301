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

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Tables
    """)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Row Counts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Row It Refuses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Answers You Already Knew
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A View
    """)
    return


if __name__ == "__main__":
    app.run()
