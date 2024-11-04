import asyncio
import os

from domestica import helpers
from domestica.client import Client
from domestica.utils import tools


def get_course_id(url: str) -> str:
    import re

    pattern = r"\/(\d+-[a-z0-9-]+)(?:\/|$)"
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return url.replace("/course", "").replace("/", "_")


async def main():
    # download dependencies
    await tools.download_dependencies()

    # load unprocessed urls
    urls = []
    with open("courses.txt", "r") as f:
        for line in f:
            if line.startswith("#"):
                continue

            url = line.strip()
            course_id = get_course_id(url)
            json_path = f"{course_id}.json"

            if os.path.exists(json_path):
                print(f"[ALREADY EXISTS] {json_path}")
                continue

            urls.append(url)

    async with Client(headless=False) as client:
        # verify captcha
        await client.verify_captcha(urls[0])

        # fetch courses data json

        BLOCK_SIZE = 2
        # for url in urls:
        for i in range(0, len(urls), BLOCK_SIZE):
            tasks = []
            tasks_json = []
            batch = urls[i : i + BLOCK_SIZE]

            # add tasks
            for url in batch:
                tasks.append(client.fetch_course(url))
                course_id = get_course_id(url)
                json_path = f"{course_id}.json"
                tasks_json.append(json_path)

            tasks.append(client.fetch_course(url))
            tasks_json.append(json_path)

            courses = await asyncio.gather(*tasks)
            for course, json_path in zip(courses, tasks_json):
                helpers.write_json(course.dict(), json_path)
                print(f"[SUCCESS] {json_path}")


async def regex():
    import re

    with open("courses.txt", "r") as f:
        for line in f:
            match = re.search(r"\/(\d+-[a-z0-9-]+)(?:\/|$)", line)
            if match:
                print(match.group(1))
            else:
                print("No match")


asyncio.run(main())
# asyncio.run(regex())
