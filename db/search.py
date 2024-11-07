import json
import os
import re

from tinydb import TinyDB, where
from unidecode import unidecode

from domestica.models import Course

_DB = "db.json"


def load_data() -> list[dict]:
    data = []
    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            data.append(json.load(f))
    return data


db = TinyDB(_DB)
db.insert_multiple(load_data())

keywords = ["python", "figma"]
keywords = [unidecode(keyword) for keyword in keywords]

pattern = rf"\b({'|'.join(keywords)})\b"


results = db.search(
    (where("id").matches(pattern))
    | (where("title").map(unidecode).search(pattern, flags=re.IGNORECASE))
    | (where("info").product_name.map(unidecode).search(pattern, flags=re.IGNORECASE))
)

for result in results:
    course = Course(**result)
    id = course.id
    title = course.title
    language = course.info.original_language.upper()
    print(f"[{id}][{title}][{language}]")


db.truncate()
os.remove(_DB)
