import pandas as pd
from taipy.gui import State, notify, Markdown
from lib.database.init import db

ANONYMOUS_BOARD_PAGE = Markdown(
    """
# Anonymous Board
<br />
<|{board_messages}|table|show_all|class_name=w-full|width=100%|>

<br />

<|{user_message}|input|lines_shown=2|label=Post an anonymous message|on_action=post_message|class_name=w-full|>

<|Send|button|on_action=post_message|>
"""  # noqa: E501
)


def get_board_messages():
    collection = db["anonymous_board"]
    messages = list(collection.find({}))
    if not messages:
        return pd.DataFrame(columns=["Message"])

    df = pd.DataFrame(messages)
    df.pop("_id")
    df.rename(
        columns={
            "message": "Message",
            "created_at": "Posted at",
        },
        inplace=True,
    )

    return df


def post_message(state: State):
    message = state.user_message
    if not message or len(message) <= 0:
        notify(state, "Please enter a message")
        return

    collection = db["anonymous_board"]
    collection.insert_one({"message": message, "created_at": pd.Timestamp.now()})
    notify(state, "success", "Message posted!")
    state.assign("user_message", "")
    state.assign("board_messages", get_board_messages())


board_messages = get_board_messages()
user_message = ""
