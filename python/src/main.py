import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from routers import connect4_router, minesweeper_router

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]

app = FastAPI()
app.include_router(connect4_router.router)
app.include_router(minesweeper_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return RedirectResponse(GITHUB_PROFILE_URL)


if os.environ.get("DEBUG", False):

    @app.get("/readme.md")
    def get_readme():
        try:
            from markdown import markdown
        except ImportError:
            return "Markdown module not installed!"

        with open("./README.out.md") as f:
            markdown_text = f.read()
        return HTMLResponse(markdown(markdown_text))
