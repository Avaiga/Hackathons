import pandas as pd

from taipy.gui import notify
from datetime import date

from lib.database.init import get_collection

BMI_PAGE = """
### Your weight info needs to be entered.

<br />

<|layout|gap=1 rem|columns=3 3 3 3|

<|{weight}|number|label=Weight (KG)|class_name=w-full|>

<|{height}|number|label=Height (CM)|>

<|{date_input}|date|hover_text=Date|format=|>

<|{submit}|button|label=submit|on_action=bodyMassIndex|>

|>

<|{result}|text|>

# <|{bmi_data}|chart|x=date|y=bmi|>
"""


def get_bmi_data():
    collection = get_collection("bmi")
    data = list(collection.find({}))

    return pd.DataFrame(data)


date_input = date.today()
weight = 0
height = 0
result = 0
bmi_data = get_bmi_data()


def bodyMassIndex(state):
    if state.weight <= 0 or state.height <= 0:
        return
    result = state.weight / (state.height / 100) ** 2
    state.assign("result", result)
    db(state, state.date_input, state.weight, state.height, result)
    new_bmi_data = get_bmi_data()
    state.assign("bmi_data", new_bmi_data)


def db(state, date_input: date, weight: int, height: int, bmi: int):
    collection = get_collection("bmi")
    collection.update_one(
        {"date": date_input.strftime("%d/%m/%Y")},
        {
            "$set": {
                "date": date_input.strftime("%d/%m/%Y"),
                "weight": weight,
                "height": height,
                "bmi": bmi,
            }
        },
        upsert=True,
    )

    notify(state, "success", f"Saved BMI for {date_input}!")
