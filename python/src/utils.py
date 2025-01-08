import os
from pathlib import Path

from fastapi import Response
from fastapi.responses import FileResponse, RedirectResponse

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]
RESOURCES_PATH = Path("./resources/")


def get_header():
    return {
        "Cache-Control": "no-cache, max-age=0",
        # "Last-Modified": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        # "ETag": etag,
    }


def png_response(img: bytes):
    """
    Maybe some optimisations could be done here.
    I'm pretty sure that the request *could* be cached but without being cached.
    Like -> if the content didn't change, don't send it again, otherwise send it.
    Also, the tiles are "shared" between the image, so maybe there is a way for the browser to reuse the same image.
    I don't want to dig more into this, but it's a thought.
    """
    # etag = hashlib.md5(img).hexdigest()
    return Response(img, media_type="image/png", headers=get_header())


def file_response(path: Path):
    return FileResponse(path, headers=get_header())


def redirect_to_readme(anchor: str = ""):
    return RedirectResponse(f"{GITHUB_PROFILE_URL}{anchor}")


def load_image(path: Path):
    with path.open("rb") as f:
        return f.read()
