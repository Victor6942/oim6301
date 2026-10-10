# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I’m thinking about starting a business that makes dog and cat treats by dehydrating raw meat and fish byproducts that would otherwise go to waste. Each week I have limited money to buy raw material and limited dehydrator time, so I have to decide which treats to make and how many batches of each. This tool takes the raw cost, drying yield, drying time, and selling price of each treat and shows how many batches my budget and dehydrator hours allow, and how much profit that makes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Start with my inputs in one place: for each treat(For now I have 6), its raw cost per lb, Drying yield which (True weight after dyhrating),dehydrator hours per batch (each has different drying time), raw lb per batch, and selling price per bag, plus my weekly budget and my weekly dehydrator hours(which is avaliable 7am to 9am, and 1-10pm.
    2. For each treat, work out the cost of one batch, which is raw lb per batch × raw cost per lb.
    3. Work out how many bags one batch makes, using the dried yield and the bag size in oz.
    4. profit of one batch = bags × price − cost of the batch
    5. Rank the treats by profit per dehydrator hour, because drying time is my limit.
    6. Go through the treats from best to worst. For each, make as many batches as I can afford with the money left and the dehydrator hours left.
    7. Subtract the money and hours I used from both, then move to the next treat
    8. Print a table (treat, batches, bags, cost, hours, profit, with a totals row) and one sentence naming the best treat and the total profit.
    9. What does your loop carry? It carries money left and dehydrator hours left, starting at my weekly budget and my weekly hours, and each treat uses up some of them.
    10. Which check? Total money spent + money left should equal my weekly budget.”
    11. Total profit from the loop should equal total revenue minus total cost, computed separately.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # --- Limits (my assumptions) ---
    weekly_budget = 50.00      # dollars I can spend on raw meat per week
    weekly_hours = 77           # dehydrator hours: (2 + 9 hrs per day) x 7 days

    # --- Treats: one dictionary per treat ---
    # raw_cost_per_lb : what I pay per lb of raw material
    # dried_yield     : share of raw weight left after drying (0.29 = 29%)
    # hours_per_batch : dehydrator hours for one batch
    # raw_lb_per_batch: how much raw material one batch holds (assumption)
    # bag_oz          : finished ounces in one bag/pack
    # price           : selling price per bag
    treats = [
        {"name": "Beef liver 4 oz",     "raw_cost_per_lb": 2.45, "dried_yield": 0.29,
         "hours_per_batch": 10, "raw_lb_per_batch": 10, "bag_oz": 4.0, "price": 9.99},
        {"name": "Pig ear strips 6 oz", "raw_cost_per_lb": 3.69, "dried_yield": 0.38,
         "hours_per_batch": 14, "raw_lb_per_batch": 10, "bag_oz": 6.0, "price": 9.99},
        {"name": "Salmon spine 3-pack", "raw_cost_per_lb": 1.50, "dried_yield": 0.25,
         "hours_per_batch": 16, "raw_lb_per_batch": 10, "bag_oz": 2.2, "price": 8.99},
        {"name": "Fish tails 4 oz",     "raw_cost_per_lb": 1.50, "dried_yield": 0.33,
         "hours_per_batch": 10, "raw_lb_per_batch": 10, "bag_oz": 4.0, "price": 14.99},
        {"name": "Skin-wrapped spine",  "raw_cost_per_lb": 1.70, "dried_yield": 0.30,
         "hours_per_batch": 20, "raw_lb_per_batch": 10, "bag_oz": 3.0, "price": 11.99},
        {"name": "Fish skin",           "raw_cost_per_lb": 1.50, "dried_yield": 0.30,
         "hours_per_batch": 6,  "raw_lb_per_batch": 10, "bag_oz": 3.0, "price": 9.99},
    ]
    return (treats,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(treats):
    batch_info = []
    for _t in treats:
        _row = dict(_t)
        _row["batch_cost"] = _t["raw_lb_per_batch"] * _t["raw_cost_per_lb"]
        _finished_oz = _t["raw_lb_per_batch"] * _t["dried_yield"] * 16
        _row["bags_per_batch"] = int(_finished_oz // _t["bag_oz"])
        _row["batch_profit"] = _row["bags_per_batch"] * _t["price"] - _row["batch_cost"]
        _row["profit_per_hour"] = _row["batch_profit"] / _t["hours_per_batch"]
        batch_info.append(_row)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
