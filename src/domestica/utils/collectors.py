import json
import re
from typing import Optional

from playwright.async_api import BrowserContext, Page

from ..models import Course, CourseInfo, Media, Section, Video
from ..utils import tools


async def fetch_course_info(url: str, context: BrowserContext) -> CourseInfo:
    page = await context.new_page()
    await page.goto(url)
    title = await get_course_title(page)
    stats = []
    items = page.locator(".course-content-stats .row li")
    count = await items.count()
    for i in range(count):
        text = await items.nth(i).text_content()
        if text is not None:
            clean_text = text.strip().replace("\n", " ")
            stats.append(clean_text)

    await page.close()

    return CourseInfo(
        title=title,
        stats=stats,
    )


async def get_course_title(page: Page) -> str:
    try:
        title = await page.locator("h1.course-header-new__title a").text_content()
    except TimeoutError:
        raise Exception("Could not get course title")

    if title is None:
        raise Exception("Could not get course title")
    return title


async def page_to_img(page: Page, path: Optional[str] = None) -> bytes:
    await page.emulate_media(media="screen")
    return await page.screenshot(path=path, full_page=True)


async def page_to_pdf(page: Page, path: Optional[str] = None) -> bytes:
    await page.emulate_media(media="screen")
    return await page.pdf(path=path)


async def fetch_course(url: str, context: BrowserContext) -> Course:
    page = await context.new_page()
    await page.goto(url)

    title = await get_course_title(page)

    try:
        sections_locator = page.locator("ul.units-list h4.unit-item__title a")
        sections: list[Section] = []
        for i in range(await sections_locator.count()):
            section_url = await sections_locator.nth(i).get_attribute("href")
            if section_url is None:
                raise Exception("Could not get section url")
            section = await fetch_section(section_url, context)
            sections.append(section)
    except TimeoutError:
        raise Exception("Could not get sections")
    except Exception as e:
        raise e

    # Capture content as PDF
    pdf_content_url = await tools.upload_from_bytes(
        await page_to_pdf(page),
        f"{title}_content.pdf",
    )

    return Course(
        title=title,
        sections=sections,
        assets=[
            Media(name="content", url=pdf_content_url),
        ],
    )


async def fetch_section(url: str, context: BrowserContext) -> Section:
    page = await context.new_page()
    await page.goto(url)

    # TODO: implement this
    if url.endswith("/final_project"):
        return Section(
            title="Final Project",
            videos=[],
            assets=[],
        )
    try:
        section_title = await page.locator("header.paper__header h2").text_content()
    except TimeoutError:
        raise Exception("Could not get section title")

    if section_title is None:
        raise Exception("Could not get section title")

    pattern = r"window\.__INITIAL_PROPS__ = JSON\.parse\('(.*?)'\)"
    match = re.search(pattern, await page.content())
    if not match:
        raise Exception("Could not get section content")

    json_str = match.group(1).replace("\\", "")
    json_data = json.loads(json_str)
    videos: list[Video] = []
    try:
        for video in json_data["videos"]:
            media = Video(
                title=video["video"]["title"],
                m3u8_url=video["video"]["playbackURL"],
            )
            videos.append(media)
    except KeyError:
        # TODO: improve logging
        print("Could not get section videos")

    # Capture content as PDF
    pdf_content_url = await tools.upload_from_bytes(
        await page_to_pdf(page),
        f"{section_title}_content.pdf",
    )

    await page.close()

    return Section(
        title=section_title,
        videos=videos,
        assets=[
            Media(name="content", url=pdf_content_url),
        ],
    )
