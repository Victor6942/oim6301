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
    weekly_budget = 100.00      # dollars I can spend on raw meat per week
    weekly_hours = 77           # dehydrator hours: (2 + 9 hrs per day) x 7 days

    # --- Treats: one dictionary per treat ---
    # max_bags = most bags I think I could sell per week (assumption)
    treats = [
        {"name": "Beef liver 4 oz",     "raw_cost_per_lb": 2.45, "dried_yield": 0.29,
         "hours_per_batch": 10, "raw_lb_per_batch": 10, "bag_oz": 4.0,
         "price": 9.99, "max_bags": 30},
        {"name": "Pig ear strips 6 oz", "raw_cost_per_lb": 3.69, "dried_yield": 0.38,
         "hours_per_batch": 14, "raw_lb_per_batch": 10, "bag_oz": 6.0,
         "price": 9.99, "max_bags": 20},
        {"name": "Salmon spine 3-pack", "raw_cost_per_lb": 1.50, "dried_yield": 0.25,
         "hours_per_batch": 16, "raw_lb_per_batch": 10, "bag_oz": 2.2,
         "price": 8.99, "max_bags": 20},
        {"name": "Fish tails 4 oz",     "raw_cost_per_lb": 1.50, "dried_yield": 0.33,
         "hours_per_batch": 10, "raw_lb_per_batch": 10, "bag_oz": 4.0,
         "price": 14.99, "max_bags": 15},
        {"name": "Skin-wrapped spine",  "raw_cost_per_lb": 1.70, "dried_yield": 0.30,
         "hours_per_batch": 20, "raw_lb_per_batch": 10, "bag_oz": 3.0,
         "price": 11.99, "max_bags": 20},
        {"name": "Fish skin",           "raw_cost_per_lb": 1.50, "dried_yield": 0.30,
         "hours_per_batch": 6,  "raw_lb_per_batch": 10, "bag_oz": 3.0,
         "price": 9.99, "max_bags": 20},
    ]
    return treats, weekly_budget, weekly_hours


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
    return (batch_info,)


@app.cell
def _(batch_info):
    ranked = sorted(batch_info, key=lambda b: b["profit_per_hour"], reverse=True)
    return (ranked,)


@app.cell
def _(ranked, weekly_budget, weekly_hours):
    money_left = weekly_budget
    hours_left = weekly_hours
    plan = []

    for _b in ranked:
        _by_money = int(money_left // _b["batch_cost"])
        _by_hours = int(hours_left // _b["hours_per_batch"])
        _by_demand = int(_b["max_bags"] // _b["bags_per_batch"])
        _batches = min(_by_money, _by_hours, _by_demand)
        if _b["batch_profit"] <= 0:
            _batches = 0
        _cost = _batches * _b["batch_cost"]
        _hours = _batches * _b["hours_per_batch"]
        _bags = _batches * _b["bags_per_batch"]
        _revenue = _bags * _b["price"]
        plan.append({"name": _b["name"], "batches": _batches, "bags": _bags,
                     "cost": _cost, "hours": _hours,
                     "revenue": _revenue, "profit": _revenue - _cost})
        money_left = money_left - _cost
        hours_left = hours_left - _hours
    return hours_left, money_left, plan


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(plan, weekly_budget, weekly_hours):
    print(f"{'Treat':<22}{'Batches':>8}{'Bags':>7}{'Cost':>10}{'Hours':>7}{'Profit':>10}")
    print("-" * 64)
    for _p in plan:
        print(f"{_p['name']:<22}{_p['batches']:>8}{_p['bags']:>7}"
              f"{_p['cost']:>10.2f}{_p['hours']:>7}{_p['profit']:>10.2f}")
    print("-" * 64)

    total_batches = sum(_p["batches"] for _p in plan)
    total_bags = sum(_p["bags"] for _p in plan)
    total_cost = sum(_p["cost"] for _p in plan)
    total_hours = sum(_p["hours"] for _p in plan)
    total_revenue = sum(_p["revenue"] for _p in plan)
    total_profit = sum(_p["profit"] for _p in plan)
    print(f"{'TOTAL':<22}{total_batches:>8}{total_bags:>7}"
          f"{total_cost:>10.2f}{total_hours:>7}{total_profit:>10.2f}")

    _made = [_p for _p in plan if _p["batches"] > 0]
    _best = max(_made, key=lambda p: p["profit"])
    print()
    print(f"With ${weekly_budget:.0f} and {weekly_hours} dehydrator hours a week, "
          f"my best treat is {_best['name']}, and the plan earns "
          f"${total_profit:.2f} profit per week.")#
    return total_cost, total_hours, total_profit


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    change between demand and trends.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(
    hours_left,
    money_left,
    plan,
    total_cost,
    total_hours,
    total_profit,
    treats,
    weekly_budget,
    weekly_hours,
):
    # Check 1: money spent + money left should equal the weekly budget
    _sum1 = total_cost + money_left
    print(f"Check 1: spent ${total_cost:.2f} + left ${money_left:.2f} = ${_sum1:.2f}  |  budget ${weekly_budget:.2f}")
    assert abs(_sum1 - weekly_budget) < 0.01, "Check 1 FAILED: money does not add up"

    # Check 2: hours used + hours left should equal the weekly hours
    _sum2 = total_hours + hours_left
    print(f"Check 2: used {total_hours} + left {hours_left} = {_sum2}  |  weekly hours {weekly_hours}")
    assert _sum2 == weekly_hours, "Check 2 FAILED: hours do not add up"

    # Check 3: rebuild total profit a second way, straight from the inputs
    _batches_by_name = {_p["name"]: _p["batches"] for _p in plan}
    _rev2 = 0
    _cost2 = 0
    for _t in treats:
        _n = _batches_by_name[_t["name"]]
        _bags2 = int(_t["raw_lb_per_batch"] * _t["dried_yield"] * 16 // _t["bag_oz"])
        _rev2 = _rev2 + _n * _bags2 * _t["price"]
        _cost2 = _cost2 + _n * _t["raw_lb_per_batch"] * _t["raw_cost_per_lb"]
    _profit2 = _rev2 - _cost2
    print(f"Check 3: loop profit ${total_profit:.2f}  |  rebuilt from inputs ${_profit2:.2f}")
    assert abs(total_profit - _profit2) < 0.01, "Check 3 FAILED: profit does not match"

    # Check 4: no treat is made beyond what I can sell, and nothing is overspent
    for _t in treats:
        assert _batches_by_name[_t["name"]] * int(_t["raw_lb_per_batch"] * _t["dried_yield"] * 16 // _t["bag_oz"]) <= _t["max_bags"], "Check 4 FAILED: over demand"
    assert money_left >= 0 and hours_left >= 0, "Check 4 FAILED: overspent"
    print("Check 4: no treat over its sales limit, no money or hours below zero")

    print("All checks passed.")
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
    The agent first gave me a plan that spent the whole budget on one treat (fish skin: 3 batches at $50) and ignored what I could actually sell. I didn’t accept it because a one-treat table didn’t answer my question about how to split limited money and dehydrator time across a variety of products. I added a max_bags input for each treat and changed the loop so each treat is limited by whichever runs out first: money, dehydrator hours, or sales demand. The plan then used five treats. I knew it was right because I compared the table to my own expectation, and the checks in section 6 agreed (money spent plus money left equals the budget, and profit matched when rebuilt from the inputs).
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I built a planner that tells me which dehydrated pet treats to make each week, and how many batches, based on my budget, my dehydrator hours, and how many bags I can sell, and then it adds a shopping list and a schedule for when to load each batch.
    """)
    return


@app.cell
def _(plan, treats):
    home_windows = [(7, 9), (13, 24)]   # hours of the day I am home and awake

    def is_home(t):
        h = t % 24
        if h == 0:
            h = 24
        for a, b in home_windows:
            if a <= h <= b:
                return True
        return False

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def clock(t):
        return f"{day_names[int(t // 24) % 7]} {int(t % 24):02d}:00"

    _hours_by_name = {_t["name"]: _t["hours_per_batch"] for _t in treats}

    batch_list = []
    for _p in plan:
        for _i in range(_p["batches"]):
            batch_list.append(_p["name"])

    schedule = []
    free_at = 7                      # first load: Monday 7am
    for _name in batch_list:
        _dur = _hours_by_name[_name]
        _s = free_at
        while not (is_home(_s) and is_home(_s + _dur)) and _s < 168:
            _s = _s + 1
        schedule.append((_name, _s, _s + _dur))
        free_at = _s + _dur

    print("Loading schedule (load and unload only while I am home)")
    for _name, _s, _e in schedule:
        print(f"{_name:<22} load {clock(_s)}  ->  done {clock(_e)}")
    print(f"All batches finished by {clock(free_at)}, {free_at - 7} hours after the first load.")
    return


if __name__ == "__main__":
    app.run()
