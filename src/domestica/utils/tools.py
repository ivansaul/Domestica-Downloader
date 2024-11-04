import asyncio
import os

import aiohttp

from ..models import Quality


async def download_m3u8_video(
    url: str,
    save_dir: str,
    quality: Quality = Quality.P1080,
    subtitle_lang: str = "en",
    output_name: str = "output",
) -> None:
    """
    Downloads a video using N_m3u8DL-RE with specific options.

    Parameters:
    - url (str): The URL of the video to be downloaded.
    - save_dir (str): The directory where the downloaded video will be saved.
    - quality (Quality): The desired video quality, e.g., Quality.P1080. Default is Quality.P1080.
    - subtitle_lang (str): The language of the subtitles desired, e.g., "en".
    - output_name (str): The name of the output file without the extension.
    """
    os.makedirs(save_dir, exist_ok=True)

    print(f"[DOWNLOADING] {output_name}", flush=True, end="")

    download_command = [
        "N_m3u8DL-RE",
        "--select-video",
        f"res='{quality.value}*':codec=hvc1:for=best",
        "--sub-format",
        "SRT",
        "--select-subtitle",
        f'lang="{subtitle_lang}":for=all',
        "--auto-subtitle-fix",
        url,
        "--save-dir",
        save_dir,
        "--save-name",
        output_name,
        "--concurrent-download",
    ]

    process = await asyncio.create_subprocess_exec(
        *download_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    await process.wait()

    if process.returncode == 0:
        print(f"\r[COMPLETED] {output_name}")
    else:
        print(f"\r[ERROR] {output_name}")


async def download_file(url: str, save_dir: str, output: str) -> None:
    """
    Downloads a file from a URL and saves it to the specified path.

    Args:
        url (str): The URL of the file to be downloaded.
        save_dir (str): The path where the file should be saved.
        output (str): The name of the output file.
    """
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, output)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(path, "wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
            else:
                raise Exception(f"Failed to download file: {url}")


async def upload_from_path(path: str) -> str:
    """
    Uploads a file to the catbox.moe service.

    Args:
        path (str): The path to the file to be uploaded.

    Returns:
        str: The response from the catbox.moe service.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist.")

    ENDPOINT = "https://catbox.moe/user/api.php"
    user_hash = "4b6585b7d61940d8b98d8e0a4"
    payload = aiohttp.FormData()
    payload.add_field("reqtype", "fileupload")
    payload.add_field("userhash", user_hash)

    with open(path, "rb") as file:
        payload.add_field(
            "fileToUpload",
            file,
            filename=os.path.basename(path),
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(ENDPOINT, data=payload) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Failed to upload file: {path}")


async def upload_from_bytes(file_data: bytes, filename: str) -> str:
    """
    Uploads a file to the catbox.moe service from bytes.

    Args:
        file_data (bytes): The file data in bytes to be uploaded.
        filename (str): The name of the file to be uploaded.

    Returns:
        str: The response from the catbox.moe service.
    """
    ENDPOINT = "https://catbox.moe/user/api.php"
    user_hash = "4b6585b7d61940d8b98d8e0a4"

    payload = aiohttp.FormData()
    payload.add_field("reqtype", "fileupload")
    payload.add_field("userhash", user_hash)
    payload.add_field(
        "fileToUpload",
        file_data,
        filename=filename,
        content_type="application/octet-stream",
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(ENDPOINT, data=payload) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Failed to upload file: {filename}")
