import numpy as np
import pandas as pd
from taipy.gui import Markdown, notify, State

from datetime import datetime
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

anime_input = ""
data_computed = pd.DataFrame(columns=["Recommendation", "Similarity Score"])

ANIME_PAGE = Markdown(
    """
# Anime Recommendation
<br />

<|{anime_input}|input|>

<|Click|button|on_action=on_recommendation_click|>
<br />
<br />
<|{data_computed}|chart|type=bar|x=Recommendation|y=Similarity Score|title=Anime Recommendation using Taipy Core|>
"""  # noqa: E501
)

anime_df = pd.read_csv("./dataset/anime.csv")
anime_synopsis_df = pd.read_csv("./dataset/anime_with_synopsis.csv")

anime_synopsis_df = anime_synopsis_df.drop(["Name", "Score", "Genres"], axis=1)
anime_df = anime_df.merge(anime_synopsis_df, on="MAL_ID", how="outer")

anime_df = anime_df[anime_df["Episodes"] != "Unknown"]
anime_df = anime_df.reset_index()
anime_df = anime_df.drop(["index"], axis=1)
anime_df["anime_index"] = anime_df.index

anime_df[
    [
        "Score",
        "Score-10",
        "Score-9",
        "Score-8",
        "Score-7",
        "Score-6",
        "Score-5",
        "Score-4",
        "Score-3",
        "Score-2",
        "Score-1",
    ]
] = anime_df[
    [
        "Score",
        "Score-10",
        "Score-9",
        "Score-8",
        "Score-7",
        "Score-6",
        "Score-5",
        "Score-4",
        "Score-3",
        "Score-2",
        "Score-1",
    ]
].replace(
    "Unknown", 0
)

anime_df[
    [
        "Score",
        "Score-10",
        "Score-9",
        "Score-8",
        "Score-7",
        "Score-6",
        "Score-5",
        "Score-4",
        "Score-3",
        "Score-2",
        "Score-1",
    ]
] = anime_df[
    [
        "Score",
        "Score-10",
        "Score-9",
        "Score-8",
        "Score-7",
        "Score-6",
        "Score-5",
        "Score-4",
        "Score-3",
        "Score-2",
        "Score-1",
    ]
].apply(
    pd.to_numeric
)

anime_df["no_of_scores"] = (
    anime_df["Score-10"]
    + anime_df["Score-9"]
    + anime_df["Score-8"]
    + anime_df["Score-7"]
    + anime_df["Score-6"]
    + anime_df["Score-5"]
    + anime_df["Score-4"]
    + anime_df["Score-3"]
    + anime_df["Score-2"]
    + anime_df["Score-1"]
)

anime_features = anime_df[
    [
        "anime_index",
        "Name",
        "Type",
        "Episodes",
        "Aired",
        "Studios",
        "Source",
        "Genres",
    ]
]
anime_features["Episodes"] = pd.to_numeric(anime_features["Episodes"].copy())


max_episodes = anime_features["Episodes"].max()

# put episodes into categories
anime_features["Episodes"] = anime_features["Episodes"].copy().replace(1, "One Episode")
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(2, 11), "Short")
)
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(11, 15), "3M")
)
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(15, 21), "4M-5M")
)
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(21, 27), "6M")
)
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(27, 51), "Long")
)
anime_features["Episodes"] = (
    anime_features["Episodes"].copy().replace(range(51, max_episodes + 1), "Very Long")
)


lstAired = []

for date in anime_features.Aired:
    x = date.split(" to ")

    try:
        date_object = datetime.strptime(x[0], "%b %d, %Y")
    except:  # noqa: E722
        try:
            date_object = datetime.strptime(x[0], "%b, %Y")
        except:  # noqa: E722
            try:
                date_object = datetime.strptime(x[0], "%Y")
            except:  # noqa: E722
                lstAired.append(x[0])
                continue

    lstAired.append(date_object.year)

lstEra = []

for t in lstAired:
    if t == "Unknown":
        lstEra.append("Unknown")
        continue

    if t < 2000:
        lstEra.append("Very Old")
    elif t < 2005:
        lstEra.append("Old")
    elif t < 2010:
        lstEra.append("Modern")
    elif t < 2015:
        lstEra.append("Recent")
    else:
        lstEra.append("New")

anime_features["Era"] = lstEra


studio_breakdown = []

for studio in anime_features.Studios:
    studio_lst = studio.split(", ")
    studio_breakdown.append(studio_lst)

genres_breakdown = []

for genre in anime_features.Genres:
    genre_lst = genre.split(", ")
    genres_breakdown.append(genre_lst)

mlb_studio = MultiLabelBinarizer()

studio_breakdown_series = pd.Series(studio_breakdown)

studio_encoded = pd.DataFrame(
    mlb_studio.fit_transform(studio_breakdown_series),
    columns=mlb_studio.classes_,
    index=studio_breakdown_series.index,
)

studio_encoded.head()
anime_features = pd.concat([anime_features, studio_encoded], axis=1)

mlb_genre = MultiLabelBinarizer()

genre_breakdown_series = pd.Series(genres_breakdown)

genre_encoded = pd.DataFrame(
    mlb_genre.fit_transform(genre_breakdown_series),
    columns=mlb_genre.classes_,
    index=genre_breakdown_series.index,
)

anime_features = pd.concat([anime_features, genre_encoded], axis=1)


cat_variables = anime_features[["Type", "Episodes", "Source", "Era"]]
cat_dummies = pd.get_dummies(cat_variables)

anime_features = anime_features.drop(
    ["Type", "Episodes", "Aired", "Studios", "Source", "Era", "Genres"], axis=1
)
anime_features = pd.concat([anime_features, cat_dummies], axis=1)
content_variables = anime_features.drop(["Name", "anime_index"], axis=1)
cosine_sim_content = cosine_similarity(content_variables, content_variables)
indices = pd.Series(
    anime_features.index, index=anime_features["Name"]
).drop_duplicates()


def get_recommendations(title, cosine_sim) -> pd.core.series.Series:
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    anime_indices = [i[0] for i in sim_scores]

    something = anime_features["Name"].iloc[anime_indices]
    return something


def on_recommendation_click(state: State):
    try:
        recommendation = get_recommendations(state.anime_input, cosine_sim_content)
        df = recommendation.to_frame().reset_index()
        df.sort_values(
            by="index",
            inplace=True,
            ascending=False,
        )
        df.rename(
            columns={"index": "Similarity Score", "Name": "Recommendation"},
            inplace=True,
        )
        state.assign("data_computed", df)
        notify(state, "info", "Recommendations generated!")
    except:  # noqa: E722
        notify(state, "error", "Anime not found!")
