import os
from functools import partial
from pathlib import Path
from time import time

from connect4 import ColumnFull, Connect4
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, RedirectResponse

from .go_library import generate_board

GITHUB_PROFILE_URL = os.environ["GITHUB_PROFILE_URL"]
IMAGE_PATH = Path("./data/connect4.png")


last_play_time = time()
c4 = Connect4()
router = APIRouter(prefix="/connect4", on_startup=[partial(generate_board, c4)])


@router.get("/image")
def get_image():
    return FileResponse(IMAGE_PATH, headers={"Cache-Control": "no-cache, max-age=0"})


@router.get("/play")
def play(column: int = Query(title="The column ID you want to play to.", ge=0, le=6)):
    global last_play_time

    if not c4.is_over:
        try:
            c4.play(column)
        except ColumnFull:
            pass
        else:
            generate_board(c4)
            last_play_time = time()
    return RedirectResponse(f"{GITHUB_PROFILE_URL}#connect4")


@router.get("/reset")
def reset():
    if not c4.is_over and time() - last_play_time < 300:
        return RedirectResponse(f"{GITHUB_PROFILE_URL}#connect4")

    c4.reset()
    generate_board(c4)
    return RedirectResponse(f"{GITHUB_PROFILE_URL}#connect4")
