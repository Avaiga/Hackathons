import pandas as pd
from taipy.gui import Gui, Markdown

CRIME_PAGE = Markdown(
    """
# Crime Rates against Transgenders
<br />
<|{crime_dataset}|chart|type=bar|x=County|y[1]=Year|y[2]=Anti-Transgender|line[1]=County|>
"""  # noqa: E501
)  # noqa: E501


def get_data(path: str):
    dataset = pd.read_csv(path)
    dataset = dataset.groupby(["County", "Year"]).sum().reset_index()
    dataset = dataset.loc[dataset["Crime Type"] == "Crimes Against Persons"]

    return dataset


crime_dataset = get_data(
    "./dataset/New_York_Hate_Crimes_by_County_and_Bias_Type_2010-2019.csv"  # noqa: E501
)
