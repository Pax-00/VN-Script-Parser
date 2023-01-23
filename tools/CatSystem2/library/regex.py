import re

regex_dict = {
    "Grisaia_no_Kajitsu": {
        "yuuji_nickname": [re.compile(r'^\$str60', re.MULTILINE), 'Yuuji'],  # Pretty sure $str60 is just Yuuji's Yujiyuji nickname
        "curved_double_quotes": [re.compile(r'“|”', re.MULTILINE), ''],  # Curved double quotes are used to denote talking over phone? Can just remove
        # "engrish_brackets": [re.compile(r'\<|\>', re.MULTILINE), ''],  # < > are used to denote engrish, can just remove
    },
    "Grisaia_no_Meikyuu": {
        "chizuru_label": [re.compile(r'^\$str122', re.MULTILINE), 'Chizuru'],  # Variable for Chizuru's name?
    },
    "Grisaia_no_Rakuen": {
        "speech_formatting": [re.compile(r'_+', re.MULTILINE), ''],  # Formatting from "I want to become a bird." speech
    },
}