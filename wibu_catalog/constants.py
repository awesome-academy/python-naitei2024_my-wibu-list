# app/constaint.py
"""
SPECIAL THANKS TO:
    https://github.com/Hernan4444/MyAnimeList-Database/blob/master/data/watching_status.csv
    https://api.mangadex.org/docs/2-limitations/
"""
from enum import Enum

ITEMS_PER_PAGE = 12
ITEMS_PER_PAGE_MORE = 20
PRODUCTS_PER_PAGE_DETAIL = 4
COMMENTS_PER_PAGE_DETAIL = 5

FIELD_MAX_LENGTH_S = 1
FIELD_MAX_LENGTH_M = 20
FIELD_MAX_LENGTH_L = 255
FIELD_MAX_LENGTH_XL = 500

TOP_WATCHING_LIMIT = 5
LATEST_CONTENT_LIMIT = 10
TOP_RANKED_LIMIT = 10
AVAILABLE_SIZES = ["S", "M", "L", "XL"]

Content_category = {
    "anime": "Anime",
    "manga": "Manga",
}

# CONTENT STATUS
Manga_status = {
    # None: "None"
    1: "Reading",
    2: "Completed",
    3: "On-Hold",
    4: "Dropped",
    5: "Re-Reading",
    6: "Plan to Read",
}

Anime_status = {
    # None: "None"
    1: "Watching",
    2: "Completed",
    3: "On-Hold",
    4: "Dropped",
    5: "Re-Watching",
    6: "Plan to Watch",
}

# RATING: CONTENT RATING
Manga_rating = {
    1: "safe",
    2: "suggestive",
    3: "erotica",
    4: "pornographic",
}
Anime_rating = {
    1: "G",  # All Ages
    2: "PG",  # Children
    3: "PG-13",  # Teens 13 or older
    4: "R",  # 17+ (violence & profanity)
    5: "R+",  # Mild Nudity
    6: "R18",  # Hentai[/quote]
}

Role_dict = {
    "admin": "admin",
    "new_user": "new_user",
    "longtime_user": "longtime_user",
    "user": "user",
    "VIP": "VIP",
}

Score_dict = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
}


class ScoreEnum(Enum):
    """ In case want to display not just score"""
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
