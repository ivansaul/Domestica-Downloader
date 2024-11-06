import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as pl:
        browser = await pl.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(
            # "https://www.domestika.org/es/courses/category/9-diseno-web-y-app/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/3-diseno/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/20-moda/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/21-cocina/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/15-arquitectura-y-espacios/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/8-fotografia-y-video/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/18-escritura/popular?catalog_option=plus"
            # "https://www.domestika.org/es/courses/category/16-caligrafia-y-tipografia/popular?catalog_option=plus"
            "https://www.domestika.org/es/courses/category/17-marketing-y-negocios/popular?catalog_option=plus"
        )

        await page.evaluate("document.body.style.zoom='50%'")

        await asyncio.sleep(60 * 3)

        with open("source.html", "w") as f:
            f.write(await page.content())

        await browser.close()


# Ejecutar la función principal
asyncio.run(main())
