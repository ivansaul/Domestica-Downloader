import asyncio
import os
import re

from domestica import helpers
from domestica.client import Client


def get_course_slug(url: str) -> str:
    pattern = r"\/(\d+-[a-z0-9-]+)(?:\/|$)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return url.replace("/course", "").replace("/", "_")


def load_urls() -> list[str]:
    urls = set()
    pattern = r"https:\/\/www\.domestika\.org\/[a-z]{2}\/courses\/\d+-[a-z0-9-]+"
    for source in os.listdir("source"):
        if source.endswith(".html"):
            with open(f"source/{source}", "r") as f:
                urls.update(re.findall(pattern, f.read()))
    return [f"{url}/course" for url in list(urls)]


async def fetch_data() -> None:
    # load unprocessed urls
    urls = []
    for url in load_urls():
        course_slug = get_course_slug(url)
        json_path = f"data/{course_slug}.json"

        if os.path.exists(json_path):
            print(f"[ALREADY EXISTS] {json_path}")
            continue
        urls.append(url)

    if not urls:
        return

    async with Client(headless=False) as client:
        # verify captcha
        await client.verify_captcha(urls[0])

        # fetch courses data json
        BLOCK_SIZE = 3
        # for url in urls:
        for i in range(0, len(urls), BLOCK_SIZE):
            batch = urls[i : i + BLOCK_SIZE]
            tasks = [client.fetch_course(url) for url in batch]
            courses = await asyncio.gather(*tasks, return_exceptions=True)

            for course, url in zip(courses, batch):
                if isinstance(course, Exception):
                    print(f"[ERROR] {url}")
                    continue

                course_slug = get_course_slug(url)
                json_path = f"data/{course_slug}.json"
                helpers.write_json(course.dict(), json_path)  # type: ignore
                print(f"[SUCCESS] {json_path}")


asyncio.run(fetch_data())
