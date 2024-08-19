# app/constaint.py
"""
SPECIAL THANKS TO:
    https://github.com/Hernan4444/MyAnimeList-Database/blob/master/data/watching_status.csv
    https://api.mangadex.org/docs/2-limitations/
"""
ITEMS_PER_PAGE = 10
ITEMS_PER_PAGE_MORE = 20

FIELD_MAX_LENGTH_S = 1
FIELD_MAX_LENGTH_M = 20
FIELD_MAX_LENGTH_L = 255
FIELD_MAX_LENGTH_XL = 500

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
    5: "Re-Watching",  # count as watching
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
    1: "G",      # All Ages
    2: "PG",     # Children
    3: "PG-13",  # Teens 13 or older
    4: "R",      # 17+ (violence & profanity)
    5: "R+",     # Mild Nudity
    6: "R18",    # Hentai[/quote]
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


TOP_WATCHING_LIMIT = 5
LATEST_CONTENT_LIMIT = 10
TOP_RANKED_LIMIT = 10
ITEMS_PER_PAGE = 15 
