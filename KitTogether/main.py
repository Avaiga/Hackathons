from taipy.gui import Gui, notify
from src.visualize_charts import visualizing_errors
from src.parse_json import pretty_print
from taipy.gui import navigate

root_md = ""

text = ""
url = ""
data_errors = {}
data_alerts = {}

page1 = """

# Accessibility Checker 
### Enter the URL of your website to easily perform an accessibility check:

<|{text}|input|>
<|Check accessibility|button|class_name=plain|on_action=on_button_action|>

"""

def on_button_action(state):
    global url, data_errors, data_alerts
    page = "accessibilitycharts"
    state.url = state.text
    url = state.text
    try:
        json_data = pretty_print(url)
        errors_array = json_data[0]
        contrast_errors_array = json_data[1]
        alerts_array = json_data[2]

        result = visualizing_errors(errors_array, contrast_errors_array, alerts_array)
        state.data_errors = result[0]
        state.data_alerts = result[1]
        navigate(state, to=page)
    except:
        notify(state, 'error', f'The URL {state.text} is not valid. Please enter a valid URL.')

page2 = """

# Here are some statistics on the accessibility issues of <|{url}|>

## Errors (bar graph)

<|{data_errors}|chart|type=bar|x=Type of Error|y=Number of Errors|>

## Errors (pie chart)

<|{data_errors}|chart|type=pie|values=Number of Errors|label=Type of Error|>

## Alerts (bar graph)

<|{data_alerts}|chart|type=bar|x=Type of Alert|y=Number of Alerts|>

## Alerts (pie chart)

<|{data_alerts}|chart|type=pie|values=Number of Alerts|label=Type of Alert|>

"""

pages = {
     "/": root_md,
    "enterurl": page1,
    "accessibilitycharts": page2
}

Gui(pages=pages).run(use_reloader=True, port=5001)
