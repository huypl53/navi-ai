import sqlite3


class BaseDto:
    connection = sqlite3.connect("navi.db")

    def __init__(self) -> None:
        pass
